from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.tenant import TenantCreate, TenantUpdate, TenantOut
from app.models.tenant import Tenant
from app.core.security import get_current_user
from app.core.rbac import require_platform_admin

router = APIRouter(prefix="/tenants", tags=["Tenant"])


@router.post(
    "/",
    response_model=TenantOut,
    dependencies=[Depends(require_platform_admin)]
)
def create_tenant(
    data: TenantCreate,
    db: Session = Depends(get_db)
):
    if db.query(Tenant).filter(Tenant.code == data.code).first():
        raise HTTPException(400, "Tenant code already exists")

    tenant = Tenant(**data.model_dump())
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant


@router.get(
    "/",
    response_model=list[TenantOut],
    dependencies=[Depends(require_platform_admin)]
)
def get_all_tenants(db: Session = Depends(get_db)):
    return db.query(Tenant).all()


@router.get("/{tenant_id}", response_model=TenantOut)
def get_tenant(
    tenant_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    tenant = db.get(Tenant, tenant_id)
    if not tenant:
        raise HTTPException(404, "Tenant not found")
    return tenant


@router.put("/{tenant_id}", response_model=TenantOut)
def update_tenant(
    tenant_id: int,
    data: TenantUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    tenant = db.get(Tenant, tenant_id)
    if not tenant:
        raise HTTPException(404, "Tenant not found")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(tenant, k, v)

    db.commit()
    db.refresh(tenant)
    return tenant


@router.delete(
    "/{tenant_id}",
    dependencies=[Depends(require_platform_admin)]
)
def delete_tenant(
    tenant_id: int,
    db: Session = Depends(get_db)
):
    tenant = db.get(Tenant, tenant_id)
    if not tenant:
        raise HTTPException(404, "Tenant not found")

    db.delete(tenant)
    db.commit()
    return {"message": "Tenant deleted"}
