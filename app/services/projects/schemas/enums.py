from enum import Enum


class DevelopmentStage(str, Enum):
    LAUNCHED = "launched"
    UNDER_CONSTRUCTION = "under_construction"


class FurnishingStatus(str, Enum):
    FULLY_FURNISHED = "fully_furnished"
    SEMI_FURNISHED = "semi_furnished"
    UNFURNISHED = "unfurnished"
    NA = "NA"


class AreaUnit(str, Enum):
    SQFT = "sqft"
    SQM = "sqm"
    ACRES = "acres"


class MediaType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    PDF = "pdf"


class ContentType(str, Enum):
    DEFAULT = "default"
    MASTER_PLAN = "master_plan"
    FLOOR_PLAN = "floor_plan"
    SITE_PLAN = "site_plan"
    BROCHURE = "brochure"


class AmountType(str, Enum):
    FIXED = "fixed"
    PER_SQFT = "per_sqft"
    PERCENTAGE = "percentage"


class CommissionType(str, Enum):
    FIXED = "fixed"
    PERCENTAGE = "percentage"


class CalculationType(str, Enum):
    FLAT = "flat"
    SLAB = "slab"


class ParkingType(str, Enum):
    OPEN = "open"
    COVERED = "covered"
    BASEMENT = "basement"


class PossessionStatus(str, Enum):
    READY_TO_MOVE = "ready_to_move"
    UNDER_CONSTRUCTION = "under_construction"


class ProjectType(str, Enum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    MIXED = "mixed"


class PropertyType(str, Enum):
    # Residential
    APARTMENT = "apartment"
    VILLA = "villa"
    ROW_HOUSE = "row House"
    PLOT = "plot"

    # Commercial
    OFFICE = "office"
    SHOP = "shop"
    WAREHOUSE = "warehouse"
    SHOWROOM = "showroom"

    # Mixed
    MIXED_USE_LAND = "mixed_use_land"
    RETAIL_RESIDENTIAL_COMPLEX = "retail_residential_complex"


class UnitType(str, Enum):
    BHK_1 = "1BHK"
    BHK_2 = "2BHK"
    BHK_3 = "3BHK"
    STUDIO = "studio"
    PENTHOUSE = "penthouse"
