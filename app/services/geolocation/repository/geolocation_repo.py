from app.services.geolocation.models.geolocation_models import Area, City, State, Locality
from app.services.geolocation.schemas import LocalityFilters
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_localities(filters: LocalityFilters, db: AsyncSession):
    result = await db.execute(
        select(Locality).where(Locality.name == filters.locality_id)
    )
    return result.scalar_one_or_none()
