from pydantic import BaseModel
from uuid import uuid4, UUID
from datetime import datetime
from typing import List, Optional

class ProfileSchema(BaseModel):
    #don't need id when creating profile since supabase auto generates uuid
    id: Optional[UUID] = None
    updated_at: Optional[datetime] = None
    username: str = None
    full_name: str = None
    avatar_url: str = None
    website: str = None
    is_employed: bool = None
    #don't worry about this rn
    expo_notifcation_token: Optional[str] = None
    age: int = None
    phone_number: str = None
    profile_email: str = None

    


class EmployerSchema(BaseModel):
    id: Optional[UUID] = None
    created_at: Optional[datetime] = None 
    updated_at: Optional[datetime] = None
    company_name: str = None
    company_logo: str = None
    website: str = None
    phone_number: str = None
    email: str = None
    is_verified: bool = None
    is_active: bool = None
    is_premium: bool = None
    is_featured: bool = None
    is_approved: bool = None
    is_suspended: bool = None
    is_deleted: bool = None
    is_banned: bool = None
    is_blocked: bool = None
    is_private: bool = None
    is_public: bool = None
    is_protected: bool = None
    is_confidential: bool = None
    is_internal: bool = None
    is_external: bool = None
    is_confirmed: bool = None
    is_pending: bool = None
    is_rejected: bool = None
    is_accepted: bool = None
    is_invited: bool = None
    is_applied: bool = None
    is_hired: bool = None
    is_fired: bool = None
    is_resigned: bool = None
    is_retired: bool = None
    is_promoted: bool = None
    is_demoted: bool