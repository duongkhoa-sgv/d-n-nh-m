from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.security import get_current_user
from app.core.rbac import require_permission

router = APIRouter(prefix="/users", tags=["Users"])


# =====================================================
# Helper: kiểm tra quyền truy cập tenant
# =====================================================
def check_tenant_access(current_user: User, tenant_id: int):
    if current_user.tenant_id != tenant_id and not current_user.is_platform_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied for this tenant"
        )


# region 1. Tạo user mới (Create User)
# Quyền: user:create
# Vai trò: Tenant Admin / PM
@router.post(
    "",
    response_model=UserResponse,
    dependencies=[Depends(require_permission("user:create"))]
)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_tenant_access(current_user, payload.tenant_id)

    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    role = db.query(Role).filter(Role.id == payload.role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    user = User(
        email=payload.email,
        full_name=payload.full_name,
        tenant_id=payload.tenant_id,
        role_id=payload.role_id,
        is_active=True
    )
    user.set_password(payload.password)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
# endregion


# region 2. Lấy danh sách user theo tenant (List Users)
# Quyền: user:view
# Vai trò: Admin / PM / BA
@router.get(
    "",
    response_model=List[UserResponse],
    dependencies=[Depends(require_permission("user:view"))]
)
def list_users(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_tenant_access(current_user, tenant_id)
    return db.query(User).filter(User.tenant_id == tenant_id).all()
# endregion


# region 3. Lấy chi tiết user (Get User Detail)
# Quyền: user:view
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(require_permission("user:view"))]
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    check_tenant_access(current_user, user.tenant_id)
    return user
# endregion


# region 4. Cập nhật user (Update User)
# Quyền: user:update
# Vai trò: Admin / PM
@router.put(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(require_permission("user:update"))]
)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    check_tenant_access(current_user, user.tenant_id)

    if payload.full_name is not None:
        user.full_name = payload.full_name
    if payload.role_id is not None:
        user.role_id = payload.role_id
    if payload.is_active is not None:
        user.is_active = payload.is_active

    db.commit()
    db.refresh(user)
    return user
# endregion


# region 5. Đổi mật khẩu user (Change Password)
# Quyền: user:update
@router.put(
    "/{user_id}/password",
    dependencies=[Depends(require_permission("user:update"))]
)
def change_password(
    user_id: int,
    new_password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    check_tenant_access(current_user, user.tenant_id)

    user.set_password(new_password)
    db.commit()
    return {"message": "Password updated successfully"}
# endregion


# region 6. Vô hiệu hoá user (Soft Delete)
# Quyền: user:delete
# Vai trò: Admin / PM
@router.delete(
    "/{user_id}",
    dependencies=[Depends(require_permission("user:delete"))]
)
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    check_tenant_access(current_user, user.tenant_id)

    user.is_active = False
    db.commit()
    return {"message": "User deactivated"}
# endregion
