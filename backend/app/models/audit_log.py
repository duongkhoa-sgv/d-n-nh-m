from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    tenant_id = Column(Integer, nullable=True)
    user_id = Column(Integer, nullable=True)

    action = Column(String(255))
    endpoint = Column(String(255))
    method = Column(String(10))
    status_code = Column(Integer)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
