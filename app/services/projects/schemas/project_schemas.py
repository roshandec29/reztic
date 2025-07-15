from pydantic import BaseModel, HttpUrl, Field, model_validator, field_validator
from typing import Optional, List, Dict
from uuid import UUID
from datetime import date, datetime
from enum import Enum


class Category(str, Enum):
    RESIDENTIAL = "Residential"
    COMMERCIAL = "Commercial"
    MIXED = "Mixed"


class SubCategory(str, Enum):
    # Residential
    APARTMENT = "Apartment"
    VILLA = "Villa"
    ROW_HOUSE = "Row House"
    PLOT = "Plot"

    # Commercial
    OFFICE = "Office"
    SHOP = "Shop"
    WAREHOUSE = "Warehouse"
    SHOWROOM = "Showroom"

    # Mixed
    MIXED_USE_LAND = "Mixed Use Land"
    RETAIL_RESIDENTIAL_COMPLEX = "Retail + Residential Complex"


CATEGORY_SUBCATEGORY_MAP: Dict[Category, List[SubCategory]] = {
    Category.RESIDENTIAL: [
        SubCategory.APARTMENT,
        SubCategory.VILLA,
        SubCategory.ROW_HOUSE,
        SubCategory.PLOT,
    ],
    Category.COMMERCIAL: [
        SubCategory.OFFICE,
        SubCategory.SHOP,
        SubCategory.WAREHOUSE,
        SubCategory.SHOWROOM,
    ],
    Category.MIXED: [
        SubCategory.MIXED_USE_LAND,
        SubCategory.RETAIL_RESIDENTIAL_COMPLEX,
    ],
}


class ProjectUnitCreate(BaseModel):
    locality_id: UUID
    category: Category
    subcategory: SubCategory
    unit_type: str
    size_sqft: int
    total_units: int
    available_units: int
    price: float

    @model_validator(mode='after')
    def validate_category_subcategory(self):
        if self.subcategory not in CATEGORY_SUBCATEGORY_MAP.get(self.category, []):
            raise ValueError(
                f"Subcategory '{self.subcategory.value}' is not valid for category '{self.category.value}'"
            )
        return self


class ProjectMediaCreate(BaseModel):
    type: str  # "image", "video", "pdf"
    media_url: HttpUrl
    meta_json: Optional[dict]
    is_featured: Optional[bool] = False


class ProjectBase(BaseModel):
    developer_id: UUID
    name: str
    description: Optional[str]
    locality_id: UUID
    status: str
    possession_date: Optional[date]
    project_type: Optional[str]
    rera_number: Optional[str]
    starting_price: Optional[float]
    price_range: Optional[dict]
    commission_structure: Optional[dict]
    is_featured: Optional[bool] = False
    badges: Optional[List[str]] = []


class ProjectCreateRequest(BaseModel):
    project: ProjectBase
    units: Optional[List[ProjectUnitCreate]] = []
    media: Optional[List[ProjectMediaCreate]] = []


class ProjectResponse(BaseModel):
    id: UUID
    name: str
    status: str
    possession_date: Optional[date]
    starting_price: float

    model_config = {
        "from_attributes": True
    }

    @field_validator('possession_date', mode="before")
    def extract_date(cls, v: datetime):
        if isinstance(v, datetime):
            return v.date()
        return v


class ProjectListFilters(BaseModel):
    search: Optional[str] = None
    status: Optional[str] = None
    locality_id: Optional[UUID] = None
    developer_id: Optional[UUID] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    is_featured: Optional[bool] = None
    badges: Optional[List[str]] = None
    sort_by: Optional[str] = "created_at"  # created_at, starting_price
    sort_order: Optional[str] = "desc"  # asc or desc
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)


class ProjectMediaResponse(BaseModel):
    id: UUID
    type: str
    media_url: HttpUrl
    meta_json: Optional[dict]
    is_featured: Optional[bool]

    model_config = {
        "from_attributes": True
    }


class ProjectUnitResponse(BaseModel):
    id: UUID
    locality_id: UUID
    category: str
    unit_type: str
    size_sqft: int
    total_units: int
    available_units: int
    price: float

    model_config = {
        "from_attributes": True
    }


class FullProjectResponse(BaseModel):
    id: UUID
    name: str
    status: str
    possession_date: Optional[date]
    starting_price: Optional[float]
    is_featured: Optional[bool]
    badges: Optional[List[str]]
    created_at: Optional[date]

    # Nested
    units: List[ProjectUnitResponse] = []
    media: List[ProjectMediaResponse] = []

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


class PaginatedProjectListResponse(BaseModel):
    total: int
    page: int
    limit: int
    projects: List[FullProjectResponse]
