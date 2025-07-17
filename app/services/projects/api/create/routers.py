from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_db
from app.services.projects.schemas.project_schemas import ProjectCreateRequest, ProjectResponse
from app.services.projects.service.project_service import ProjectService
from app.utils.errors import ProjectAlreadyExistsException

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])


@router.post("/create", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: ProjectCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        project = await ProjectService(db).create_project(payload)
        await db.commit()
        await db.refresh(project)
        return project
    except ProjectAlreadyExistsException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"status": e.status_code, "msg": e.detail}
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )
