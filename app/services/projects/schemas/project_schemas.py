from pydantic import BaseModel, HttpUrl, Field, model_validator, field_validator
from typing import Optional, Text, List, Dict, Set
from uuid import UUID
from datetime import date, datetime
from .enums import *
from fastapi import Query


class ProjectUnitCreate(BaseModel):
    locality_id: UUID
    unit_type: UnitType
    layout_name: Optional[str]
    carpet_area_value: float
    super_area_value: float
    area_unit: AreaUnit = AreaUnit.SQFT
    bedrooms: Optional[int]
    balconies: Optional[int]
    total_units: int
    available_units: int
    base_price: float
    total_price: float
    eoi_amount: Optional[float] = 0
    floor_plan_media_url: HttpUrl
    is_active: Optional[bool] = True


class ProjectMediaCreate(BaseModel):
    type: MediaType
    content_type: ContentType = ContentType.DEFAULT
    media_url: HttpUrl
    thumbnail_url: HttpUrl
    meta_json: Optional[dict]
    sort_order: Optional[int] = 0
    is_featured: Optional[bool] = False


class ProjectBase(BaseModel):
    developer_id: UUID
    name: str
    description: Optional[str]
    locality_id: UUID
    development_stage: DevelopmentStage
    possession_date: Optional[date]
    rera_number: Optional[str]
    furnishing_status: FurnishingStatus = FurnishingStatus.NA
    is_featured: Optional[bool] = False
    badges: Optional[List[str]] = []
    project_type: ProjectType
    property_type: PropertyType
    project_size: Optional[float] = 0
    project_size_unit: Optional[str]

    @model_validator(mode='after')
    def validate_project_property_type(self):
        if self.property_type not in CATEGORY_SUBCATEGORY_MAP.get(self.project_type, []):
            raise ValueError(
                f"Subcategory '{self.property_type.value}' is not valid for category '{self.project_type.value}'"
            )
        return self


class AdditionalChargeCreate(BaseModel):
    charge_name: str
    amount_type: AmountType
    amount_value: float
    applicable_on_unit_type: Optional[str]
    is_mandatory: Optional[bool] = False


class AdditionalChargeResponse(BaseModel):
    charge_name: str
    amount_type: AmountType
    amount_value: float
    applicable_on_unit_type: Optional[str]
    is_mandatory: Optional[bool] = False
    model_config = {"from_attributes": True}


class ParkingChargeCreate(BaseModel):
    parking_type: ParkingType
    amount_type: AmountType
    amount_value: float
    unit_type: Optional[str]
    max_allowed_per_unit: Optional[int]
    is_active: Optional[bool] = True
    is_deleted: Optional[bool] = False


class ParkingChargeResponse(BaseModel):
    parking_type: ParkingType
    amount_type: AmountType
    amount_value: float
    unit_type: Optional[str]
    max_allowed_per_unit: Optional[int]
    is_active: Optional[bool] = True
    is_deleted: Optional[bool] = False

    model_config = {"from_attributes": True}


class PaymentPlanBreakupCreate(BaseModel):
    milestone: str
    percentage: float
    due_days: Optional[int]
    notes: Optional[str] = None
    model_config = {"from_attributes": True}


class PaymentPlanCreate(BaseModel):
    plan_name: str
    description: Optional[str] = None
    breakup_create: Optional[List[PaymentPlanBreakupCreate]] = []
    model_config = {"from_attributes": True}


class PaymentResponse(BaseModel):
    plan_name: str
    description: Optional[str] = None
    breakups: List[PaymentPlanBreakupCreate]

    model_config = {"from_attributes": True}


class ProjectCommissionCreate(BaseModel):
    commission_type: CommissionType
    calculation_type: CalculationType
    range_min_value: Optional[int]
    range_max_value: Optional[int]
    amount: float
    meta_json: Optional[dict] = None
    is_active: Optional[bool] = True


class ProjectCommissionResponse(BaseModel):
    commission_type: CommissionType
    calculation_type: CalculationType
    range_min_value: Optional[int]
    range_max_value: Optional[int]
    amount: float
    meta_json: Optional[dict] = None
    is_active: Optional[bool] = True
    model_config = {"from_attributes": True}


class NearbyLandmarkCreate(BaseModel):
    name: str
    type: str  # optional Enum can be created later (hospital, mall etc.)
    distance_km: Optional[float]
    location_url: Optional[HttpUrl]


class NearbyLandmarkResponse(BaseModel):
    name: str
    type: str  # optional Enum can be created later (hospital, mall etc.)
    distance_km: Optional[float]
    location_url: Optional[HttpUrl]
    model_config = {"from_attributes": True}


class Amenity(BaseModel):
    name: str
    icon_url: Optional[HttpUrl]

    model_config = {"from_attributes": True}


class ProjectAmenityCreate(BaseModel):
    amenity_id: UUID
    is_available: Optional[bool] = True


class ProjectCreateRequest(BaseModel):
    project: ProjectBase
    units: Optional[List[ProjectUnitCreate]] = []
    media: Optional[List[ProjectMediaCreate]] = []
    amenities: List[ProjectAmenityCreate] = []
    nearby_landmarks: List[NearbyLandmarkCreate] = []
    additional_charges: AdditionalChargeResponse
    commission: ProjectCommissionCreate
    parking: ParkingChargeResponse
    payment: PaymentPlanCreate


class ProjectResponse(BaseModel):
    id: UUID
    name: str
    project_type: ProjectType
    property_type: PropertyType
    development_stage: DevelopmentStage
    possession_date: Optional[date]

    model_config = {"from_attributes": True}

    @field_validator('possession_date', mode="before")
    def extract_date(cls, v: datetime):
        if isinstance(v, datetime):
            return v.date()
        return v


class ProjectListFilters(BaseModel):
    search: Optional[str] = None
    development_stage: Optional[DevelopmentStage] = None
    locality_id: Optional[UUID] = None
    developer_id: Optional[UUID] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    project_type: Optional[ProjectType] = None
    property_type: Optional[PropertyType] = None
    unit_type: Optional[List[UnitType]] = Query(default=None)
    bedrooms: Optional[List[str]] = Query(default=None)
    balconies: Optional[List[str]] = Query(default=None)
    is_featured: Optional[bool] = None
    badges: Optional[List[str]] = None
    possession_date: Optional[int] = None
    sort_by: Optional[str] = "created_at"  # created_at, starting_price
    sort_order: Optional[str] = "desc"  # asc or desc
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)


class ProjectMediaResponse(BaseModel):
    id: UUID
    type: MediaType
    content_type: ContentType
    media_url: HttpUrl
    thumbnail_url: HttpUrl
    meta_json: Optional[dict] = None
    sort_order: Optional[int] = 0
    is_featured: Optional[bool] = False

    model_config = {"from_attributes": True}


class ProjectUnitResponse(BaseModel):
    id: UUID
    locality_id: UUID
    unit_type: UnitType
    layout_name: Optional[str]
    carpet_area_value: float
    super_area_value: float
    area_unit: AreaUnit
    bedrooms: Optional[int]
    balconies: Optional[int]
    total_units: int
    available_units: int
    base_price: float
    total_price: float
    eoi_amount: Optional[float] = 0
    floor_plan_media_url: HttpUrl
    is_active: Optional[bool] = True

    model_config = {"from_attributes": True}


class FullProjectResponse(BaseModel):
    id: UUID
    name: str
    project_type: ProjectType
    property_type: PropertyType
    development_stage: DevelopmentStage
    possession_date: Optional[date]
    starting_price: Optional[float]
    is_featured: Optional[bool]
    badges: Optional[List[str]]
    created_at: Optional[date]

    # Nested
    # units: List[ProjectUnitResponse] = []
    media: List[ProjectMediaResponse] = []
    # amenities: List[Amenity] = []
    # nearby_landmarks: List[NearbyLandmarkResponse] = []
    # additional_charges: AdditionalChargeResponse
    # commissions: ProjectCommissionCreate
    # parking: ParkingChargeResponse
    # payment_plan: PaymentResponse

    locality: Optional[str]
    full_address: Optional[str] = ""

    model_config = {
        "from_attributes": True
    }

    @field_validator('possession_date', mode="before")
    def extract_date(cls, v: datetime):
        if isinstance(v, datetime):
            return v.date()
        return v

    @field_validator('created_at', mode="before")
    def extract_created_date(cls, v: datetime):
        if isinstance(v, datetime):
            return v.date()
        return v

    @field_validator("locality", mode="before")
    def extract_locality_name(cls, v):
        if isinstance(v, dict):
            return v.get("name")
        elif hasattr(v, "name"):
            return v.name
        return v

    @field_validator("full_address", mode="before")
    def extract_full_address(cls, v):
        if isinstance(v, dict):
            return v.get("full_address")
        elif hasattr(v, "full_address"):
            return v.full_address
        return v


class LocalityResponse(BaseModel):
    name: str
    latitude: float
    longitude: float

    model_config = {"from_attributes": True}


class ProjectDetailResponse(BaseModel):
    id: UUID
    name: str
    description: Text
    project_type: ProjectType
    property_type: PropertyType
    development_stage: DevelopmentStage
    configuration: Optional[Set[str]] = Set
    project_size: Optional[float] = 0
    project_size_unit: Optional[str]
    unit_size_range: Optional[List[int]] = []
    possession_date: Optional[date]
    starting_price: Optional[float]
    total_units: Optional[int] = 0
    is_featured: Optional[bool]
    badges: Optional[List[str]]
    created_at: Optional[date]
    updated_at: Optional[date]

    # Nested
    units: List[ProjectUnitResponse] = []
    media: List[ProjectMediaResponse] = []
    all_amenities: List[Dict] = []
    nearby_landmarks: List[NearbyLandmarkResponse] = []
    additional_charges: List[AdditionalChargeResponse] = []
    commissions: List[ProjectCommissionResponse] = []
    parking: List[ParkingChargeResponse] = []
    payment_plan: List[PaymentResponse] = []
    locality: Optional[LocalityResponse] = Dict
    full_address: Optional[str] = ""

    model_config = {
        "from_attributes": True
    }

    @field_validator('possession_date', mode="before")
    def extract_date(cls, v: datetime):
        if isinstance(v, datetime):
            return v.date()
        return v

    @field_validator('created_at', mode="before")
    def extract_created_date(cls, v: datetime):
        if isinstance(v, datetime):
            return v.date()
        return v

    @field_validator('updated_at', mode="before")
    def extract_updated_date(cls, v: datetime):
        if isinstance(v, datetime):
            return v.date()
        return v

    # @field_validator("locality", mode="before")
    # def extract_locality_name(cls, v):
    #     if isinstance(v, dict):
    #         return v.get("name")
    #     elif hasattr(v, "name"):
    #         return v.name
    #     return v

    @field_validator("full_address", mode="before")
    def extract_full_address(cls, v):
        if isinstance(v, dict):
            return v.get("full_address")
        elif hasattr(v, "full_address"):
            return v.full_address
        return v


class PaginatedProjectListResponse(BaseModel):
    total: int
    page: int
    limit: int
    projects: List[FullProjectResponse]
