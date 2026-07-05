from pydantic import BaseModel
from typing import Optional


class ArtworkCreate(BaseModel):
    title: str
    technique: str
    price: int
    description: Optional[str] = None
    image_url: str
    avito_id: Optional[str] = None


class ArtworkUpdate(BaseModel):
    title: Optional[str] = None
    technique: Optional[str] = None
    price: Optional[int] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_available: Optional[int] = None


class ArtworkResponse(BaseModel):
    id: int
    title: str
    technique: str
    price: int
    description: Optional[str]
    image_url: str
    avito_id: Optional[str]
    is_available: int

    class Config:
        from_attributes = True


class ContactForm(BaseModel):
    name: str
    email: str
    message: str
    artwork_id: Optional[int] = None