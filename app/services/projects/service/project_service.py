from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.services.projects.schemas.project_schemas import ProjectCreateRequest, ProjectListFilters, FullProjectResponse
from app.services.projects.repository.project_repo import (
    get_project_by_name_and_developer,
    create_project,
    create_project_units,
    create_project_media
)
from app.utils.errors import ProjectAlreadyExistsException
from app.services.projects.repository.project_repo import fetch_projects
from typing import Tuple, List


class ProjectService:
    @staticmethod
    async def create_project(payload: ProjectCreateRequest, db: AsyncSession):
        try:
            # Check if project already exists
            existing = await get_project_by_name_and_developer(payload.project.name, payload.project.developer_id, db)
            if existing:
                raise ProjectAlreadyExistsException("Project with this name already exists for this developer.")

            # Create Project
            project = await create_project(payload.project.dict(), db)

            # Create Units
            if payload.units:
                await create_project_units(project.id, payload.units, db)

            # Create Media
            if payload.media:
                await create_project_media(project.id, payload.media, db)

            return project

        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Failed to create project: " + str(e))

    async def list_projects(
        self, db: AsyncSession, filters: ProjectListFilters
    ) -> Tuple[List[FullProjectResponse], int]:
        projects, total = await fetch_projects(db, filters)
        return [FullProjectResponse.from_orm(p) for p in projects], total
