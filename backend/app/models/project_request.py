from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class ProjectRequest(Base):
    __tablename__ = "project_requests"

    id = Column(Integer, primary_key=True, index=True)

    from_tenant_id = Column(Integer, ForeignKey("tenants.id"))
    to_tenant_id = Column(Integer, ForeignKey("tenants.id"))

    title = Column(String(255))
    description = Column(Text)

    budget = Column(Integer)
    deadline = Column(DateTime)

    # PENDING | ACCEPTED | REJECTED | NEGOTIATING
    status = Column(String(20), default="PENDING")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
