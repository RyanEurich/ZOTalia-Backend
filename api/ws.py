from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Any
import json
from datetime import datetime
import asyncio

# Import your existing Supabase client and auth dependencies
from .config import supabase
from .routes.messaging import Message  # Import the Message model

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[Dict[str, Any]]] = {}
        self.channel = None
        
    async def connect(self, websocket: WebSocket, topic: str, user_id: str):
        await websocket.accept()
        if topic not in self.active_connections:
            self.active_connections[topic] = []
            
        # Store websocket connection with user_id
        self.active_connections[topic].append({
            "websocket": websocket, 
            "user_id": user_id
        })
        
        # Create subscription in Supabase
        await self.create_subscription(topic, user_id)
    
    async def disconnect(self, websocket: WebSocket, topic: str, user_id: str):
        # Find and remove the connection
        if topic in self.active_connections:
            self.active_connections[topic] = [
                conn for conn in self.active_connections[topic] 
                if conn["websocket"] != websocket
            ]
            
            # If no more connections for this topic and user, remove subscription
            if not any(conn["user_id"] == user_id for conn in self.active_connections[topic]):
                await self.remove_subscription(topic, user_id)
            
            # If no more connections for this topic, clean up
            if not self.active_connections[topic]:
                del self.active_connections[topic]
    
    async def create_subscription(self, topic: str, user_id: str):
        """Create a subscription in Supabase"""
        subscription_id = f"{user_id}:{topic}"
        
        try:
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
                supabase.table("subscription").insert(subscription_data).execute()
        except Exception as e:
            print(f"Error creating subscription: {str(e)}")
    
    async def remove_subscription(self, topic: str, user_id: str):
        """Remove a subscription from Supabase"""
        subscription_id = f"{user_id}:{topic}"
        
        try:
            supabase.table("subscription") \
                .delete() \
                .eq("subscription_id", subscription_id) \
                .execute()
        except Exception as e:
            print(f"Error removing subscription: {str(e)}")
    
    async def broadcast_message(self, message_data: Dict[str, Any], topic: str, sender_id: str = None):
        """Broadcast message to all clients connected to this topic"""
        if topic in self.active_connections:
            message_json = json.dumps(message_data)
            for connection in self.active_connections[topic]:
                # Don't send message back to the sender
                if sender_id and connection["user_id"] == sender_id:
                    continue
                try:
                    await connection["websocket"].send_text(message_json)
                except Exception as e:
                    print(f"Error sending message to client: {str(e)}")
    
    async def start_supabase_listener(self):
        """Start listening to Supabase realtime events"""
        self.channel = supabase.channel('messages-channel')
        
        # Define callback for handling messages
        async def handle_message_insert(payload):
            # Extract message data from payload
            new_message = payload.get('new', {})
            topic = new_message.get('topic')
            
            if topic and topic in self.active_connections:
                # Broadcast to connected clients
                await self.broadcast_message(new_message, topic)
        
        # Subscribe to INSERT events on the messages table
        self.channel.on(
            'postgres_changes',
            event='INSERT',
            schema='public',
            table='messages',
            callback=handle_message_insert
        )
        
        await self.channel.subscribe()
    
    async def stop_supabase_listener(self):
        """Stop the Supabase realtime listener"""
        if self.channel:
            try:
                await self.channel.unsubscribe()
            except Exception as e:
                print(f"Error unsubscribing from channel: {str(e)}")

# Create connection manager instance
manager = ConnectionManager()

# Define lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start the Supabase listener
    print("WebSocket server starting up")
    await manager.start_supabase_listener()
    yield
    # Shutdown: Close any connections or resources
    print("WebSocket server shutting down")
    await manager.stop_supabase_listener()

# Initialize FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to verify the user's token
async def verify_token(token: str):
    try:
        user = supabase.auth.get_user(token)
        if user:
            return user.user.id
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

# WebSocket endpoint for real-time messaging
@app.websocket("/ws/{topic}")
async def websocket_endpoint(websocket: WebSocket, topic: str):
    # Get token from query parameters
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=4001, reason="Authentication required")
        return
    
    try:
        # Verify token and get user_id
        user_id = await verify_token(token)
        
        await manager.connect(websocket, topic, user_id)
        
        # Send a join message
        join_message = {
            "topic": topic,
            "payload": {
                "type": "system",
                "content": f"User {user_id} has joined the chat",
                "user_id": user_id,
                "timestamp": datetime.now().isoformat()
            },
            "event": "join",
            "private": False
        }
        
        # Send join message to Supabase
        try:
            supabase.rpc(
                "send", 
                {
                    "payload": json.dumps(join_message["payload"]),
                    "event": join_message["event"],
                    "topic": join_message["topic"],
                    "private": join_message["private"]
                }
            ).execute()
        except Exception as e:
            # Fallback to direct insert
            print(f"Error using RPC send: {str(e)}")
            supabase.table("messages").insert(join_message).execute()
        
        # Listen for messages from the client
        try:
            while True:
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                # Construct the full message
                new_message = {
                    "topic": topic,
                    "payload": {
                        "content": message_data.get("content", ""),
                        "sender_id": user_id,
                        "timestamp": datetime.now().isoformat()
                    },
                    "event": message_data.get("event", "message"),
                    "extension": message_data.get("extension"),
                    "private": False
                }
                
                # Send message to Supabase
                try:
                    supabase.rpc(
                        "send", 
                        {
                            "payload": json.dumps(new_message["payload"]),
                            "event": new_message["event"],
                            "topic": new_message["topic"],
                            "extension": new_message.get("extension"),
                            "private": new_message["private"]
                        }
                    ).execute()
                except Exception as e:
                    # Fallback to direct insert
                    print(f"Error using RPC send: {str(e)}")
                    supabase.table("messages").insert(new_message).execute()
                
                # Send message back to sender immediately for faster UI update
                await websocket.send_json(new_message)
                
                # Manually broadcast to other connected clients
                # This provides faster delivery than waiting for Supabase
                await manager.broadcast_message(new_message, topic, user_id)
                
        except WebSocketDisconnect:
            await manager.disconnect(websocket, topic, user_id)
            
            # Send a leave message
            leave_message = {
                "topic": topic,
                "payload": {
                    "type": "system",
                    "content": f"User {user_id} has left the chat",
                    "user_id": user_id,
                    "timestamp": datetime.now().isoformat()
                },
                "event": "leave",
                "private": False
            }
            
            # Send leave message to Supabase
            try:
                supabase.rpc(
                    "send", 
                    {
                        "payload": json.dumps(leave_message["payload"]),
                        "event": leave_message["event"],
                        "topic": leave_message["topic"],
                        "private": leave_message["private"]
                    }
                ).execute()
            except Exception as e:
                # Fallback to direct insert
                print(f"Error using RPC send: {str(e)}")
                supabase.table("messages").insert(leave_message).execute()
            
    except HTTPException as he:
        await websocket.close(code=4001, reason=str(he.detail))
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        if websocket.client_state == WebSocket.CONNECTED:
            await websocket.close(code=1000)

# Simple health check endpoint
@app.get("/health")
async def ws_health_check():
    return {"status": "ok", "service": "websocket"}

# Required for Vercel
module_app = app