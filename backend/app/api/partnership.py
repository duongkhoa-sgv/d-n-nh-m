from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import get_current_user
from app.core.tenant_context import get_current_tenant
from app.core.rbac import require_permission
from app.services.partnership_service import PartnershipService

router = APIRouter(prefix="/partnerships", tags=["Partnership"])

@router.post("/invite/{target_tenant_id}")
async def invite_partner(
    target_tenant_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    tenant=Depends(get_current_tenant),
):
    require_permission(user, "partnership:create")
    await PartnershipService.invite_partner(db, tenant.id, target_tenant_id, user.id)
    return {"message": "Invitation sent"}
