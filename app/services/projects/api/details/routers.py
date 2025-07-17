from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from app.db.connection import get_db
from uuid import UUID
from app.services.projects.service.project_service import ProjectService

router = APIRouter(prefix="/api/v1/project", tags=["projects"])


@router.get("/details/{project_id}")
async def get_projects(
    project_id: UUID, db: AsyncSession = Depends(get_db)
):
    try:
        project_detail = await ProjectService(db).get_project_details(project_id)
        return project_detail
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": 500, "msg": "Failed to fetch projects", "error": str(e)}
        )
