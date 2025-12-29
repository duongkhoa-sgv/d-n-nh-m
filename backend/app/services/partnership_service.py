from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.partnership import Partnership
from app.models.project_request import ProjectRequest

class PartnershipService:

    # Gửi lời mời hợp tác
    @staticmethod
    async def invite_partner(db: AsyncSession, from_tenant_id: int, to_tenant_id: int, user_id: int):
        partnership = Partnership(
            tenant_a_id=from_tenant_id,
            tenant_b_id=to_tenant_id,
            status="PENDING"
        )
        db.add(partnership)
        await db.commit()

    # Phản hồi lời mời hợp tác
    @staticmethod
    async def respond_invite(db: AsyncSession, partnership_id: int, tenant_id: int, accept: bool):
        result = await db.execute(
            select(Partnership).where(Partnership.id == partnership_id)
        )
        partnership = result.scalar_one()

        partnership.status = "ACCEPTED" if accept else "REJECTED"
        await db.commit()

    # Hủy hợp tác
    @staticmethod
    async def revoke_partnership(db: AsyncSession, partnership_id: int, tenant_id: int):
        result = await db.execute(
            select(Partnership).where(Partnership.id == partnership_id)
        )
        partnership = result.scalar_one()
        await db.delete(partnership)
        await db.commit()

    # Gửi project request
    @staticmethod
    async def send_project_request(db: AsyncSession, from_tenant_id: int, to_tenant_id: int, data: dict, user_id: int):
        request = ProjectRequest(
            from_tenant_id=from_tenant_id,
            to_tenant_id=to_tenant_id,
            title=data.get("title"),
            description=data.get("description"),
            budget=data.get("budget"),
            deadline=data.get("deadline"),
        )
        db.add(request)
        await db.commit()

    # Phản hồi project request
    @staticmethod
    async def respond_project_request(db: AsyncSession, request_id: int, tenant_id: int, status: str):
        result = await db.execute(
            select(ProjectRequest).where(ProjectRequest.id == request_id)
        )
        project_request = result.scalar_one()

        project_request.status = status
        await db.commit()

    # Danh sách đối tác
    @staticmethod
    async def get_partners(db: AsyncSession, tenant_id: int):
        result = await db.execute(
            select(Partnership).where(
                (Partnership.tenant_a_id == tenant_id) |
                (Partnership.tenant_b_id == tenant_id)
            )
        )
        return result.scalars().all()
