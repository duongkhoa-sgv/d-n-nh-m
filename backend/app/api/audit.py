from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import get_current_user
from app.core.tenant_context import get_current_tenant
from app.core.rbac import require_permission
from app.services.audit_service import AuditService

router = APIRouter(prefix="/audit", tags=["Audit"])

@router.get("/")
async def get_audit_logs(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    tenant=Depends(get_current_tenant),
):
    require_permission(user, "audit:view")
    return await AuditService.get_logs(db, tenant.id)
