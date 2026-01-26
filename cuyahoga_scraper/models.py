"""
Data models for Cuyahoga County property data.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, List
from datetime import datetime
import json


@dataclass
class Property:
    """Represents a property record from Cuyahoga County."""

    # Core identifiers
    parcel_id: str
    address: str
    city: str = "CLEVELAND HEIGHTS"
    state: str = "OH"
    zip_code: Optional[str] = None

    # Owner information
    owner_name: Optional[str] = None
    owner_address: Optional[str] = None
    owner_city: Optional[str] = None
    owner_state: Optional[str] = None
    owner_zip: Optional[str] = None

    # Property characteristics
    property_class: Optional[str] = None
    land_use: Optional[str] = None
    year_built: Optional[int] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    total_rooms: Optional[int] = None
    living_area_sqft: Optional[int] = None
    lot_size_sqft: Optional[int] = None
    lot_size_acres: Optional[float] = None
    stories: Optional[float] = None

    # Valuation
    market_value_land: Optional[float] = None
    market_value_building: Optional[float] = None
    market_value_total: Optional[float] = None
    assessed_value: Optional[float] = None

    # Tax information
    tax_district: Optional[str] = None
    school_district: Optional[str] = None
    annual_taxes: Optional[float] = None

    # Sale history
    last_sale_date: Optional[str] = None
    last_sale_price: Optional[float] = None

    # Geographic data
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    census_tract: Optional[str] = None

    # Metadata
    data_source: str = "Cuyahoga County ArcGIS"
    retrieved_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        """Convert property to dictionary."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert property to JSON string."""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_arcgis_feature(cls, feature: dict) -> "Property":
        """Create Property from ArcGIS feature attributes."""
        attrs = feature.get("attributes", {})
        geometry = feature.get("geometry", {})

        # Map ArcGIS fields to Property fields
        # Field names based on typical Cuyahoga County CAMA data
        return cls(
            parcel_id=attrs.get("PARCEL_ID") or attrs.get("PIN") or attrs.get("PARCELPIN") or "",
            address=cls._build_address(attrs),
            city=attrs.get("CITY") or attrs.get("MUNICIPALITY") or "CLEVELAND HEIGHTS",
            zip_code=attrs.get("ZIP") or attrs.get("ZIP_CODE"),
            owner_name=attrs.get("OWNER") or attrs.get("OWNER_NAME") or attrs.get("OWNERNAME"),
            owner_address=attrs.get("OWNER_ADDR") or attrs.get("MAIL_ADDR"),
            owner_city=attrs.get("OWNER_CITY") or attrs.get("MAIL_CITY"),
            owner_state=attrs.get("OWNER_STATE") or attrs.get("MAIL_STATE"),
            owner_zip=attrs.get("OWNER_ZIP") or attrs.get("MAIL_ZIP"),
            property_class=attrs.get("CLASS") or attrs.get("PROPERTY_CLASS") or attrs.get("PROPCLASS"),
            land_use=attrs.get("LAND_USE") or attrs.get("LANDUSE") or attrs.get("USE_CODE"),
            year_built=cls._safe_int(attrs.get("YEAR_BUILT") or attrs.get("YRBUILT")),
            bedrooms=cls._safe_int(attrs.get("BEDROOMS") or attrs.get("BEDS")),
            bathrooms=cls._safe_float(attrs.get("BATHROOMS") or attrs.get("BATHS") or attrs.get("FULLBATHS")),
            total_rooms=cls._safe_int(attrs.get("TOTAL_ROOMS") or attrs.get("ROOMS")),
            living_area_sqft=cls._safe_int(attrs.get("LIVING_AREA") or attrs.get("SQFT") or attrs.get("TOTAL_SQFT")),
            lot_size_sqft=cls._safe_int(attrs.get("LOT_SIZE") or attrs.get("LOTSQFT")),
            lot_size_acres=cls._safe_float(attrs.get("ACRES") or attrs.get("LOT_ACRES")),
            stories=cls._safe_float(attrs.get("STORIES") or attrs.get("NUM_STORIES")),
            market_value_land=cls._safe_float(attrs.get("MKT_LAND") or attrs.get("LAND_VALUE")),
            market_value_building=cls._safe_float(attrs.get("MKT_BLDG") or attrs.get("BLDG_VALUE") or attrs.get("IMPR_VALUE")),
            market_value_total=cls._safe_float(attrs.get("MKT_TOTAL") or attrs.get("TOTAL_VALUE") or attrs.get("APPRTOT")),
            assessed_value=cls._safe_float(attrs.get("ASSESSED") or attrs.get("ASSESSED_VALUE")),
            tax_district=attrs.get("TAX_DIST") or attrs.get("TAXDIST"),
            school_district=attrs.get("SCHOOL_DIST") or attrs.get("SCHOOLDIST"),
            annual_taxes=cls._safe_float(attrs.get("ANNUAL_TAX") or attrs.get("TAXES")),
            last_sale_date=attrs.get("SALE_DATE") or attrs.get("SALEDATE"),
            last_sale_price=cls._safe_float(attrs.get("SALE_PRICE") or attrs.get("SALEPRICE")),
            latitude=geometry.get("y"),
            longitude=geometry.get("x"),
            census_tract=attrs.get("CENSUS_TRACT") or attrs.get("TRACT"),
        )

    @staticmethod
    def _build_address(attrs: dict) -> str:
        """Build full address from components."""
        parts = []

        # Try full address first
        if attrs.get("ADDRESS") or attrs.get("FULL_ADDRESS") or attrs.get("SITUS_ADDR"):
            return attrs.get("ADDRESS") or attrs.get("FULL_ADDRESS") or attrs.get("SITUS_ADDR")

        # Build from components
        house_num = attrs.get("HOUSE_NUM") or attrs.get("HSE_NUM") or attrs.get("LOCADDR")
        street = attrs.get("STREET") or attrs.get("STREET_NAME") or attrs.get("LOCSTREET")
        street_suffix = attrs.get("SUFFIX") or attrs.get("STREET_SUFFIX") or ""

        if house_num:
            parts.append(str(house_num))
        if street:
            parts.append(street)
        if street_suffix:
            parts.append(street_suffix)

        return " ".join(parts) if parts else "Unknown"

    @staticmethod
    def _safe_int(value) -> Optional[int]:
        """Safely convert value to int."""
        if value is None:
            return None
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _safe_float(value) -> Optional[float]:
        """Safely convert value to float."""
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None


@dataclass
class PropertySearchResult:
    """Results from a property search query."""

    properties: List[Property] = field(default_factory=list)
    total_count: int = 0
    query_params: dict = field(default_factory=dict)
    search_time_seconds: float = 0.0
    has_more: bool = False
    error: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "properties": [p.to_dict() for p in self.properties],
            "total_count": self.total_count,
            "query_params": self.query_params,
            "search_time_seconds": self.search_time_seconds,
            "has_more": self.has_more,
            "error": self.error,
        }

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
