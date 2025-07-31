from app.services.projects.models.project_models import Project, ProjectUnit, ProjectMedia, ProjectCommission
from app.services.projects.models.other_models import ProjectAmenity, ParkingCharge, NearbyLandmark
from app.services.projects.models.payment_plan_models import PaymentPlan, PaymentPlanBreakup, AdditionalCharge
from app.services.geolocation.models.geolocation_models import Area, City, State
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, func, desc, asc, extract
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


async def create_project_amenities(project_id, amenities, db: AsyncSession):
    for amenity in amenities:
        db.add(ProjectAmenity(project_id=project_id, **amenity.dict()))


async def create_project_payment(project_id, payment, db: AsyncSession):
    payment_plan= PaymentPlan(project_id=project_id, plan_name=payment.plan_name, description=payment.description)
    db.add(payment_plan)
    await db.flush()
    payment_plan_id = payment_plan.id
    for breakup in payment.breakup_create:
        db.add(PaymentPlanBreakup(payment_plan_id=payment_plan_id, **breakup.dict()))


async def create_project_additional_charges(project_id, charges, db: AsyncSession):
    db.add(AdditionalCharge(project_id=project_id, **charges.dict()))


async def create_project_commission(project_id, commission, db: AsyncSession):
    db.add(ProjectCommission(project_id=project_id, **commission.dict()))


async def create_project_parking(project_id, parking, db: AsyncSession):
    db.add(ParkingCharge(project_id=project_id, **parking.dict()))


async def create_project_nearby_landmarks(project_id, landmarks, db: AsyncSession):
    for nl in landmarks:
        db.add(NearbyLandmark(project_id=project_id, **nl.dict()))


async def fetch_projects(session: AsyncSession, filters: ProjectListFilters):
    query = select(Project).join(Project.locality).options(
        joinedload(Project.locality)
        .joinedload(Locality.area)
        .joinedload(Area.city)
        .joinedload(City.state)
        .joinedload(State.country),
        selectinload(Project.units),
        selectinload(Project.media),
        selectinload(Project.nearby_landmarks),
        selectinload(Project.additional_charges),
        selectinload(Project.parking),
        selectinload(Project.payment_plan),
        selectinload(Project.commissions),
        selectinload(Project.amenities).joinedload(ProjectAmenity.amenity)
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

    unit_subquery = select(ProjectUnit.project_id).where(
        and_(
            ProjectUnit.unit_type.in_(filters.unit_type) if filters.unit_type else True,
            ProjectUnit.bedrooms.in_(filters.bedrooms) if filters.bedrooms else True,
            ProjectUnit.balconies.in_(filters.balconies) if filters.balconies else True,
            ProjectUnit.base_price >= filters.min_price if filters.min_price else True,
            ProjectUnit.base_price <= filters.max_price if filters.max_price else True,
        )
    ).distinct()

    # Filters
    if filters.development_stage:
        query = query.where(Project.development_stage == filters.development_stage)
    if filters.project_type:
        query = query.where(Project.project_type == filters.project_type)
    if filters.property_type:
        query = query.where(Project.property_type == filters.property_type)
    if filters.possession_date:
        query = query.where(extract("year", Project.possession_date) == filters.possession_date)
    if filters.locality_id:
        query = query.where(Project.locality_id == filters.locality_id)
    if filters.developer_id:
        query = query.where(Project.developer_id == filters.developer_id)
    if filters.is_featured is not None:
        query = query.where(Project.is_featured == filters.is_featured)
    if filters.unit_type or filters.bedrooms or filters.balconies or filters.min_price or filters.max_price:
        query = query.where(Project.id.in_(unit_subquery))
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

    query = select(Project).join(Project.locality).where(Project.id == project_id).options(
        joinedload(Project.locality)
        .joinedload(Locality.area)
        .joinedload(Area.city)
        .joinedload(City.state)
        .joinedload(State.country),
        selectinload(Project.units),
        selectinload(Project.media),
        selectinload(Project.nearby_landmarks),
        selectinload(Project.additional_charges),
        selectinload(Project.parking),
        selectinload(Project.payment_plan).joinedload(PaymentPlan.breakups),
        selectinload(Project.commissions),
        selectinload(Project.amenities).joinedload(ProjectAmenity.amenity)
    )

    response = await session.execute(query)
    project_detail = response.scalars().first()

    return project_detail
