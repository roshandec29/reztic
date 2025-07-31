from fastapi import APIRouter, Depends
from app.db.connection import get_db
from app.services.geolocation.schemas import LocalityFilters
from app.services.geolocation.service.geolocation_service import GeolocationService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["geolocation"], prefix="/api/v1")


@router.get("/localities")
async def get_localities(
        request: LocalityFilters = Depends(),
        db: AsyncSession = Depends(get_db)
):
    geo_service = GeolocationService(db)
    response = await geo_service.get_localities(request)

    return response
