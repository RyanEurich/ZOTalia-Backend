from pydantic import BaseModel
from uuid import uuid4, UUID
from datetime import datetime
from typing import List, Optional

class ProfileSchema(BaseModel):
    id: Optional[UUID] = None
    created_at: Optional[datetime] = None 
    updated_at: Optional[datetime] = None
    username: str = None
    full_name: str = None
    avatar_url: str = None
    website: str = None
    is_employed: bool = None
    expo_notifcation_token: Optional[str] = None
    age: int = None
    phone_number: str = None
    profile_email: str = None


