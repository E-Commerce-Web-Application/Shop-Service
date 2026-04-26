from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID


class ShopBase(BaseModel):
    name: str
    description: str
    email: EmailStr
    phone: str
    location: str


class ShopCreate(ShopBase):
    owner_id: UUID


class ShopRead(ShopBase):
    id: UUID
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ShopUpdate(ShopBase):
    name: Optional[str] = None
    description: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None


class ShopReviewCreate(BaseModel):
    shop_id: UUID
    user_id: UUID
    rating: int
    comment: str
