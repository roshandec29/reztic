from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from app.db.connection import get_db
from app.services.projects.schemas.project_schemas import ProjectListFilters, PaginatedProjectListResponse
from app.services.projects.service.project_service import ProjectService

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])


@router.get("/list")
async def get_projects(
    filters: ProjectListFilters = Depends(),
    db: AsyncSession = Depends(get_db),
):
    try:
        projects, total = await ProjectService().list_projects(db, filters)
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
