from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from app.db.connection import get_db
from app.services.projects.schemas.project_schemas import ProjectListFilters
from app.services.projects.service.project_service import ProjectService
from typing import Optional, List
from app.services.projects.schemas.enums import UnitType

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])


@router.get("/list")
async def get_projects(
    bedrooms: Optional[List[int]] = Query(default=None),
    unit_type: Optional[List[UnitType]] = Query(default=None),
    balconies: Optional[List[int]] = Query(default=None),
    filters: ProjectListFilters = Depends(),
    db: AsyncSession = Depends(get_db),
):
    try:
        filters.bedrooms = bedrooms
        filters.balconies = balconies
        filters.unit_type = unit_type
        projects, total = await ProjectService(db).list_projects(filters)
        return {
            "projects": projects,
            "total": total,
            "page": filters.page,
            "limit": filters.limit,
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": 500, "msg": "Failed to fetch projects", "error": str(e)}
        )
