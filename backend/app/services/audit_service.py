from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.audit_log import AuditLog

class AuditService:

    # Ghi log mỗi khi có hành động quan trọng
    @staticmethod
    async def log(request, status_code: int):
        db: AsyncSession = request.state.db

        audit = AuditLog(
            tenant_id=getattr(request.state, "tenant_id", None),
            user_id=getattr(request.state, "user_id", None),
            action=request.url.path,
            endpoint=str(request.url),
            method=request.method,
            status_code=status_code,
        )

        db.add(audit)
        await db.commit()

    # Lấy audit log theo tenant
    @staticmethod
    async def get_logs(db: AsyncSession, tenant_id: int, action=None, user_id=None):
        query = select(AuditLog).where(AuditLog.tenant_id == tenant_id)

        if action:
            query = query.where(AuditLog.action == action)
        if user_id:
            query = query.where(AuditLog.user_id == user_id)

        result = await db.execute(query)
        return result.scalars().all()

    # Admin xem toàn bộ log
    @staticmethod
    async def get_system_logs(db: AsyncSession):
        result = await db.execute(select(AuditLog))
        return result.scalars().all()
