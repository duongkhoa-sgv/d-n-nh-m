from pydantic import BaseModel, Field
from datetime import datetime


class TenantBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    code: str = Field(..., min_length=2, max_length=50)
    is_active: bool = True


class TenantCreate(TenantBase):
    pass


class TenantUpdate(BaseModel):
    name: str | None = None
    is_active: bool | None = None


class TenantOut(TenantBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
