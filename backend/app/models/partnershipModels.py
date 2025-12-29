from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class Partnership(Base):
    __tablename__ = "partnerships"

    id = Column(Integer, primary_key=True, index=True)

    # Tenant gửi lời mời
    tenant_a_id = Column(Integer, ForeignKey("tenants.id"))

    # Tenant nhận lời mời
    tenant_b_id = Column(Integer, ForeignKey("tenants.id"))

    # PENDING | ACCEPTED | REJECTED
    status = Column(String(20), default="PENDING")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
