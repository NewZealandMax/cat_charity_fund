from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User
from app.services.push_investment import push_investment


class CRUDDonation(CRUDBase):

    async def create(
        self, 
        obj_in,
        session: AsyncSession,
        user: User
    ):
        obj_in_data = obj_in.dict()
        obj_in_data['user_id'] = user.id
        donation = self.model(**obj_in_data)
        setattr(donation, 'invested_amount', 0)
        session.add(donation)
        await push_investment(donation, session)
        await session.commit()
        await session.refresh(donation)
        return donation

    async def get_user_donations(
        self,
        session: AsyncSession,
        user: User
    ) -> List[Donation]:
        donations = await session.execute(
            select(self.model).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
