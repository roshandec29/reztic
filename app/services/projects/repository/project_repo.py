from app.services.projects.models.project_models import Project, ProjectUnit, ProjectMedia
from app.services.geolocation.models.geolocation_models import Area, City, State
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, func, desc, asc
from app.services.projects.schemas.project_schemas import ProjectListFilters
from sqlalchemy.orm import selectinload, joinedload
from app.services.geolocation.models.geolocation_models import Locality
from uuid import UUID


async def get_project_by_name_and_developer(name: str, developer_id: UUID, db: AsyncSession):
    result = await db.execute(
        select(Project).where(Project.name == name, Project.developer_id == developer_id)
    )
    return result.scalar_one_or_none()


async def create_project(data: dict, db: AsyncSession) -> Project:
    project = Project(**data)
    db.add(project)
    await db.flush()  # Keep project.id available
    return project


async def create_project_units(project_id, units_data, db: AsyncSession):
    for unit in units_data:
        db.add(ProjectUnit(project_id=project_id, **unit.dict()))
    await db.flush()


async def create_project_media(project_id, media_data, db: AsyncSession):
    for media in media_data:
        db.add(ProjectMedia(project_id=project_id, **media.dict()))
    await db.flush()


async def fetch_projects(session: AsyncSession, filters: ProjectListFilters):
    query = select(Project).join(Project.locality).options(
        joinedload(Project.locality)
        .joinedload(Locality.area)
        .joinedload(Area.city)
        .joinedload(City.state)
        .joinedload(State.country),
        selectinload(Project.units),
        selectinload(Project.media)
    )

    # Text search
    if filters.search:
        pattern = f"%{filters.search.lower()}%"
        query = query.where(
            or_(
                func.lower(Project.name).like(pattern),
                func.lower(Locality.name).like(pattern)
            )
        )

    # Filters
    if filters.status:
        query = query.where(Project.status == filters.status)
    if filters.locality_id:
        query = query.where(Project.locality_id == filters.locality_id)
    if filters.developer_id:
        query = query.where(Project.developer_id == filters.developer_id)
    if filters.is_featured is not None:
        query = query.where(Project.is_featured == filters.is_featured)
    if filters.min_price:
        query = query.where(Project.starting_price >= filters.min_price)
    if filters.max_price:
        query = query.where(Project.starting_price <= filters.max_price)
    if filters.badges:
        for badge in filters.badges:
            query = query.where(badge == func.any(Project.badges))

    # Sorting
    sort_column = getattr(Project, filters.sort_by, Project.created_at)
    if filters.sort_order == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    # Pagination
    offset = (filters.page - 1) * filters.limit
    query = query.offset(offset).limit(filters.limit)

    results = await session.execute(query)
    projects = results.scalars().all()

    # Total count (for frontend pagination info)
    count_query = select(func.count()).select_from(Project)
    total_result = await session.execute(count_query)
    total_count = total_result.scalar()

    return projects, total_count


async def get_project_detail_id(session: AsyncSession, project_id: UUID):

    query = select(Project).where(Project.id == project_id).options(
        joinedload(Project.locality)
        .joinedload(Locality.area)
        .joinedload(Area.city)
        .joinedload(City.state)
        .joinedload(State.country),
        selectinload(Project.units),
        selectinload(Project.media)
    )

    response = await session.execute(query)
    project_detail = response.scalars().first()

    return project_detail
