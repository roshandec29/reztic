from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class LocalityFilters(BaseModel):
    area_name: Optional[str] = None
    city_name: Optional[str] = None
    locality_id: Optional[UUID] = None
    city_id: Optional[UUID] = None
    country_id: Optional[UUID] = None
    area_id: Optional[UUID] = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)
