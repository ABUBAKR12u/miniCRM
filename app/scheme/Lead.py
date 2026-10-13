from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CreateLead(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    source: Optional[str] = None
    note: Optional[str] = None


class UpdateLead(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    source: Optional[str] = None
    note: Optional[str] = None
    status: Optional[str] = None


class ResponseLead(BaseModel):
    id: int
    name: str
    phone: Optional[str]
    email: Optional[str]
    source: Optional[str]
    note: Optional[str]
    status: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class LeadListResponse(BaseModel):
    total: int
    page: int
    pages: int
    items: list[ResponseLead]


class ActivityResponse(BaseModel):
    id: int
    lead_id: int
    action: str
    detail: Optional[str]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


class DashboardResponse(BaseModel):
    total: int
    new: int
    contacted: int
    qualified: int
    won: int
    lost: int
