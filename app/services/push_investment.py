from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def push_investment(
    donation: Donation,
    session: AsyncSession
):
    projects = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == False  # noqa
        ).order_by(CharityProject.id)
    )
    for project in projects.scalars().all():
        project_remainder = project.full_amount - project.invested_amount
        donation_remainder = donation.full_amount - donation.invested_amount
        invest_sum = min(project_remainder, donation_remainder)
        project.invested_amount += invest_sum
        if project.invested_amount == project.full_amount:
            project.fully_invested = True
            project.close_date = datetime.now()
        donation.invested_amount += invest_sum
        if donation.invested_amount == donation.full_amount:
            donation.fully_invested = True
            donation.close_date = datetime.now()
            break
