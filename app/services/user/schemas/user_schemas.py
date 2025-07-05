from pydantic import BaseModel, EmailStr, constr, Field
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, constr
from datetime import date


class UserRegisterRequest(BaseModel):
    first_name: constr(min_length=1, max_length=50)
    last_name: constr(min_length=1, max_length=50)
    email: EmailStr
    phone: constr(pattern=r'^\+91\d{10}$')
    password: constr(min_length=8)
    dob: Optional[date]  # ISO8601 string (e.g. 1990-01-01)
    gender: Optional[str] = Field(None, pattern="^(Male|Female|Other)$")
    company_id: Optional[UUID]
    languages: Optional[List[str]] = []

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "+919365618318",
                "password": "StrongPass123@",
                "dob": "1990-05-15",
                "gender": "Male",
                "company_id": "c245e5a4-99b8-4c34-ae83-3b993f660001",
                "languages": ["English", "Hindi"]
            }
        }


class OTPRequest(BaseModel):
    phone: str


class VerifyOTPRequest(BaseModel):
    phone: constr(min_length=10, max_length=15)
    otp: constr(min_length=6, max_length=6)
