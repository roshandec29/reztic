from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.services.projects.schemas.project_schemas import ProjectCreateRequest, ProjectListFilters, FullProjectResponse,\
        ProjectDetailResponse

from app.services.projects.repository.project_repo import (
    get_project_by_name_and_developer,
    create_project,
    create_project_units,
    create_project_media,
    create_project_payment,
    create_project_additional_charges,
    create_project_commission,
    create_project_parking,
    create_project_amenities,
    create_project_nearby_landmarks
)
from app.utils.errors import ProjectAlreadyExistsException, ProjectNotFound
from app.services.projects.repository.project_repo import fetch_projects, get_project_detail_id
from typing import Tuple, List, Dict
from uuid import UUID


class ProjectService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_project(self, payload: ProjectCreateRequest):
        try:
            # Check if project already exists
            existing = await get_project_by_name_and_developer(payload.project.name, payload.project.developer_id, self.db)
            if existing:
                raise ProjectAlreadyExistsException("Project with this name already exists for this developer.")

            # Create Project
            project = await create_project(payload.project.dict(), self.db)

            # Create Units
            if payload.units:
                await create_project_units(project.id, payload.units, self.db)

            # Create Media
            if payload.media:
                await create_project_media(project.id, payload.media, self.db)

            if payload.amenities:
                await create_project_amenities(project.id, payload.amenities, self.db)

            if payload.nearby_landmarks:
                await create_project_nearby_landmarks(project.id, payload.nearby_landmarks, self.db)

            if payload.parking:
                await create_project_parking(project.id, payload.parking, self.db)

            if payload.commission:
                await create_project_commission(project.id, payload.commission, self.db)

            if payload.additional_charges:
                await create_project_additional_charges(project.id, payload.additional_charges, self.db)

            if payload.payment:
                await create_project_payment(project.id, payload.payment, self.db)

            return project

        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail="Failed to create project: " + str(e))

    async def list_projects(
        self, filters: ProjectListFilters
    ) -> Tuple[List[FullProjectResponse], int]:
        projects, total = await fetch_projects(self.db, filters)
        response = []

        for p in projects:
            p.full_address = p.locality.full_address

            if p.units:
                starting_price = p.units[0].base_price
                for unit in p.units:
                    p.starting_price = starting_price if unit.base_price > starting_price else unit.base_price
            response.append(FullProjectResponse.from_orm(p))

        return response, total

    async def get_project_details(self, project_id: UUID) -> ProjectDetailResponse:
        project = await get_project_detail_id(self.db, project_id)

        if not project:
            raise ProjectNotFound("Project with this id doesn't exists.")

        if project.units:
            project.total_units = len(project.units)
            starting_price = project.units[0].base_price
            configuration = set()
            min_super_area = float('inf')
            max_super_area = 0
            for unit in project.units:
                project.starting_price = starting_price if unit.base_price > starting_price else unit.base_price
                configuration.add(unit.unit_type)
                min_super_area = min_super_area if unit.super_area_value > min_super_area else unit.super_area_value
                max_super_area = max_super_area if unit.super_area_value < max_super_area else unit.super_area_value

            project.configuration = configuration
            project.unit_size_range = [min_super_area, max_super_area]

        project.all_amenities = [
            {
                "name": pa.amenity.name,
                "icon_url": pa.amenity.icon_url
            }
            for pa in project.amenities
            if pa.is_available and pa.amenity and pa.amenity.is_active
        ]
        project.full_address = project.locality.full_address

        return ProjectDetailResponse.from_orm(project)


