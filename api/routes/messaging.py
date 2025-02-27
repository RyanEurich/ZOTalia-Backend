from contextlib import asynccontextmanager
from fastapi import APIRouter, HTTPException, status, FastAPI
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import json
from datetime import datetime
import uuid

# Import the existing Supabase client
from api.config import supabase

# Create a router for messaging functionality
router = APIRouter(prefix="/messaging", tags=["messaging"])

# Pydantic models
class Message(BaseModel):
    topic: str
    payload: Dict[str, Any]
    event: Optional[str] = None
    extension: Optional[str] = None
    private: bool = False

    # For compatibility with FastAPI's JSON serialization
    def dict(self, *args, **kwargs):
        return {
            "topic": self.topic,
            "payload": self.payload,
            "event": self.event,
            "extension": self.extension,
            "private": self.private
        }

# Define the actual function implementations
# Then attach them to the router

async def get_topics():
    try:
        # Get distinct topics from messages table
        response = supabase.rpc(
            "get_distinct_topics"
        ).execute()
        
        # If the RPC doesn't exist, fallback to a direct query
        if not response.data:
            response = supabase.table("messages").select("topic").execute()
            topics = list(set(item["topic"] for item in response.data if "topic" in item))
        else:
            topics = [item["topic"] for item in response.data if "topic" in item]
            
        return {"topics": topics}
    except Exception as e:
        # Fallback to direct query if RPC fails
        try:
            response = supabase.table("messages").select("topic").execute()
            topics = list(set(item["topic"] for item in response.data if "topic" in item))
            return {"topics": topics}
        except Exception as inner_e:
            raise HTTPException(status_code=500, detail=str(inner_e))

async def get_topic_messages(topic: str):
    try:
        # Get messages for a specific topic
        response = supabase.table("messages") \
            .select("*") \
            .eq("topic", topic) \
            .is_("private", "false") \
            .order("inserted_at") \
            .execute()
            
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def send_message(message: Message):
    try:
        # Format the message for Supabase
        message_data = message.dict()
        
        # Use Supabase's built-in send function via RPC if available
        try:
            response = supabase.rpc(
                "send", 
                {
                    "payload": json.dumps(message_data["payload"]),
                    "event": message_data["event"] or "message",
                    "topic": message_data["topic"],
                    "extension": message_data["extension"],
                    "private": message_data["private"]
                }
            ).execute()
            
            if getattr(response, 'error', None):
                # Fallback to direct insert
                response = supabase.table("messages").insert(message_data).execute()
        except:
            # Fallback to direct insert
            response = supabase.table("messages").insert(message_data).execute()
            
        return response.data[0] if response.data else {"status": "sent"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def create_subscription(topic: str, user_id: str):
    try:
        # Generate a unique subscription_id that combines user and topic
        subscription_id = f"{user_id}:{topic}"
        
        # Check if subscription already exists
        response = supabase.table("subscription").select("*") \
            .eq("subscription_id", subscription_id) \
            .execute()
            
        if not response.data:
            # Create new subscription
            subscription_data = {
                "subscription_id": subscription_id,
                "entity": "messages",
                "filters": {"topic": topic},
                "claims": {"user_id": user_id},
                "claims_role": "authenticated"
            }
            response = supabase.table("subscription").insert(subscription_data).execute()
            
        return {"status": "success", "subscription_id": subscription_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def remove_subscription(topic: str, user_id: str):
    try:
        subscription_id = f"{user_id}:{topic}"
        
        response = supabase.table("subscription") \
            .delete() \
            .eq("subscription_id", subscription_id) \
            .execute()
            
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Now attach the functions to the router
router.get("/topics/")(get_topics)
router.get("/topics/{topic}/messages/")(get_topic_messages)
router.post("/messages/", status_code=status.HTTP_201_CREATED)(send_message)
router.post("/subscriptions/")(create_subscription)
router.delete("/subscriptions/{topic}/{user_id}")(remove_subscription)

# Expose the Supabase client for reuse in other modules
def get_supabase_client():
    return supabase