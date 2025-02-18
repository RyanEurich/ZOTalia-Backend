from pydantic import BaseModel, field_serializer

class UserCredentials(BaseModel):
    email: str
    password: str