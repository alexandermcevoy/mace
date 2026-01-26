"""
Cuyahoga County Property Scraper

Main scraper module for pulling property data from Cuyahoga County's
ArcGIS REST services.
"""

import requests
import time
import logging
from typing import Optional, List, Dict, Any, Generator
from urllib.parse import urlencode

from .models import Property, PropertySearchResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CuyahogaPropertyScraper:
    """
    Scraper for Cuyahoga County property data using ArcGIS REST API.

    The scraper accesses the county's public GIS services to retrieve
    parcel and property information.
    """

    # ArcGIS REST API endpoints for Cuyahoga County
    BASE_URL = "https://gis.cuyahogacounty.us/server/rest/services"

    # Available map services with parcel data
    SERVICES = {
        "parcels_cama": f"{BASE_URL}/CCFO/APPRAISAL_PARCELS_CAMA_WGS84/MapServer",
        "parcels_historic": f"{BASE_URL}/CCFO/APPRAISAL_PARCELS_HISTORIC_WGS84/MapServer",
        "real_property": f"{BASE_URL}/CUYAHOGA_BASE/Real_Property_WGS84/MapServer",
    }

    # Layer indices within the parcels_cama service
    LAYERS = {
        "parcels": 0,  # FO_PP_CAMA - Main parcel polygons
        "addresses": 1,  # FO_AR_CAMA - Address records
        "sales": 2,  # FO_SP_CAMA - Sales/Points
    }

    # Cleveland Heights municipality identifiers
    # These are common ways the city is identified in the data
    CLEVELAND_HEIGHTS_IDENTIFIERS = [
        "CLEVELAND HEIGHTS",
        "CLEVELAND HTS",
        "CLEVELAND HTS.",
        "CLEVE HTS",
        "CLE HTS",
        "CLEVELANDHEIGHTS",
    ]

    # Cleveland Heights tax district codes (first 3 digits of parcel numbers)
    # Tax district 56x is typically Cleveland Heights
    CLEVELAND_HEIGHTS_TAX_DISTRICTS = ["561", "562", "563", "564", "565"]

    def __init__(
        self,
        timeout: int = 30,
        max_retries: int = 3,
        rate_limit_delay: float = 0.5,
    ):
        """
        Initialize the scraper.

        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            rate_limit_delay: Delay between requests in seconds
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limit_delay = rate_limit_delay
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
        })

    def _make_request(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict]:
        """
        Make a request with retry logic.

        Args:
            url: Request URL
            params: Query parameters

        Returns:
            JSON response or None on failure
        """
        params = params or {}
        params["f"] = "json"  # Always request JSON format

        for attempt in range(self.max_retries):
            try:
                response = self.session.get(
                    url,
                    params=params,
                    timeout=self.timeout,
                )
                response.raise_for_status()

                data = response.json()

                # Check for ArcGIS error response
                if "error" in data:
                    error_msg = data["error"].get("message", "Unknown error")
                    logger.error(f"ArcGIS error: {error_msg}")
                    return None

                return data

            except requests.exceptions.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff

            except ValueError as e:
                logger.error(f"JSON parse error: {e}")
                return None

        return None

    def get_service_info(self, service_name: str = "parcels_cama") -> Optional[Dict]:
        """
        Get information about a map service.

        Args:
            service_name: Name of the service (parcels_cama, parcels_historic, real_property)

        Returns:
            Service metadata dictionary
        """
        if service_name not in self.SERVICES:
            logger.error(f"Unknown service: {service_name}")
            return None

        url = self.SERVICES[service_name]
        return self._make_request(url)

    def get_layer_info(
        self,
        layer_id: int = 0,
        service_name: str = "parcels_cama",
    ) -> Optional[Dict]:
        """
        Get information about a specific layer including field definitions.

        Args:
            layer_id: Layer index within the service
            service_name: Name of the service

        Returns:
            Layer metadata including field definitions
        """
        if service_name not in self.SERVICES:
            logger.error(f"Unknown service: {service_name}")
            return None

        url = f"{self.SERVICES[service_name]}/{layer_id}"
        return self._make_request(url)

    def get_field_names(
        self,
        layer_id: int = 0,
        service_name: str = "parcels_cama",
    ) -> List[str]:
        """
        Get list of field names for a layer.

        Args:
            layer_id: Layer index within the service
            service_name: Name of the service

        Returns:
            List of field names
        """
        info = self.get_layer_info(layer_id, service_name)
        if not info or "fields" not in info:
            return []

        return [field["name"] for field in info["fields"]]

    def query_parcels(
        self,
        where_clause: str = "1=1",
        out_fields: str = "*",
        layer_id: int = 0,
        service_name: str = "parcels_cama",
        return_geometry: bool = True,
        result_offset: int = 0,
        result_record_count: int = 1000,
        order_by: Optional[str] = None,
    ) -> Optional[Dict]:
        """
        Query parcels using ArcGIS REST API.

        Args:
            where_clause: SQL WHERE clause for filtering
            out_fields: Fields to return (* for all)
            layer_id: Layer index
            service_name: Service name
            return_geometry: Whether to include geometry
            result_offset: Starting record offset
            result_record_count: Maximum records to return
            order_by: ORDER BY clause

        Returns:
            Query results dictionary
        """
        if service_name not in self.SERVICES:
            logger.error(f"Unknown service: {service_name}")
            return None

        url = f"{self.SERVICES[service_name]}/{layer_id}/query"

        params = {
            "where": where_clause,
            "outFields": out_fields,
            "returnGeometry": str(return_geometry).lower(),
            "resultOffset": result_offset,
            "resultRecordCount": result_record_count,
            "outSR": "4326",  # WGS84 for lat/lon coordinates
        }

        if order_by:
            params["orderByFields"] = order_by

        time.sleep(self.rate_limit_delay)
        return self._make_request(url, params)

    def get_cleveland_heights_properties(
        self,
        limit: Optional[int] = None,
        offset: int = 0,
        fields: Optional[List[str]] = None,
        property_class: Optional[str] = None,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        year_built_min: Optional[int] = None,
        year_built_max: Optional[int] = None,
    ) -> PropertySearchResult:
        """
        Get properties specifically in Cleveland Heights.

        This method builds a query targeting Cleveland Heights properties
        using multiple filter strategies (city name, tax district).

        Args:
            limit: Maximum number of properties to return
            offset: Starting offset for pagination
            fields: Specific fields to retrieve (None for all)
            property_class: Filter by property class (e.g., 'R' for residential)
            min_value: Minimum total market value
            max_value: Maximum total market value
            year_built_min: Minimum year built
            year_built_max: Maximum year built

        Returns:
            PropertySearchResult with matching properties
        """
        start_time = time.time()
        result = PropertySearchResult()
        result.query_params = {
            "city": "Cleveland Heights",
            "limit": limit,
            "offset": offset,
            "property_class": property_class,
            "min_value": min_value,
            "max_value": max_value,
        }

        # Build WHERE clause for Cleveland Heights
        where_parts = []

        # Try city/municipality field matching
        city_conditions = " OR ".join(
            [f"UPPER(CITY) = '{city}'" for city in self.CLEVELAND_HEIGHTS_IDENTIFIERS]
            + [f"UPPER(MUNICIPALITY) = '{city}'" for city in self.CLEVELAND_HEIGHTS_IDENTIFIERS]
        )
        where_parts.append(f"({city_conditions})")

        # Alternative: Use tax district codes
        # Uncomment if city field doesn't work:
        # tax_districts = " OR ".join(
        #     [f"PARCEL_ID LIKE '{td}%'" for td in self.CLEVELAND_HEIGHTS_TAX_DISTRICTS]
        # )
        # where_parts.append(f"({tax_districts})")

        # Add optional filters
        if property_class:
            where_parts.append(f"UPPER(CLASS) = '{property_class.upper()}'")
            where_parts.append(f"OR UPPER(PROPERTY_CLASS) = '{property_class.upper()}'")

        if min_value is not None:
            where_parts.append(f"(MKT_TOTAL >= {min_value} OR TOTAL_VALUE >= {min_value})")

        if max_value is not None:
            where_parts.append(f"(MKT_TOTAL <= {max_value} OR TOTAL_VALUE <= {max_value})")

        if year_built_min is not None:
            where_parts.append(f"(YEAR_BUILT >= {year_built_min} OR YRBUILT >= {year_built_min})")

        if year_built_max is not None:
            where_parts.append(f"(YEAR_BUILT <= {year_built_max} OR YRBUILT <= {year_built_max})")

        where_clause = " AND ".join(where_parts)

        # Determine fields to retrieve
        out_fields = ",".join(fields) if fields else "*"

        # Query the API
        batch_size = min(limit, 1000) if limit else 1000
        current_offset = offset
        all_properties = []

        while True:
            response = self.query_parcels(
                where_clause=where_clause,
                out_fields=out_fields,
                result_offset=current_offset,
                result_record_count=batch_size,
                return_geometry=True,
            )

            if not response:
                result.error = "Failed to retrieve data from ArcGIS service"
                break

            features = response.get("features", [])
            if not features:
                break

            # Convert features to Property objects
            for feature in features:
                try:
                    prop = Property.from_arcgis_feature(feature)
                    all_properties.append(prop)
                except Exception as e:
                    logger.warning(f"Failed to parse property: {e}")

            # Check if we have enough results
            if limit and len(all_properties) >= limit:
                all_properties = all_properties[:limit]
                break

            # Check for more results
            exceeded_limit = response.get("exceededTransferLimit", False)
            if not exceeded_limit or len(features) < batch_size:
                break

            current_offset += batch_size
            result.has_more = True

        result.properties = all_properties
        result.total_count = len(all_properties)
        result.search_time_seconds = time.time() - start_time

        return result

    def search_by_address(
        self,
        street_address: str,
        city: str = "Cleveland Heights",
    ) -> PropertySearchResult:
        """
        Search for a property by street address.

        Args:
            street_address: Street address to search
            city: City name (defaults to Cleveland Heights)

        Returns:
            PropertySearchResult with matching properties
        """
        start_time = time.time()
        result = PropertySearchResult()
        result.query_params = {"address": street_address, "city": city}

        # Normalize address for search
        address_upper = street_address.upper().strip()

        # Build WHERE clause
        where_clause = f"UPPER(ADDRESS) LIKE '%{address_upper}%' OR UPPER(SITUS_ADDR) LIKE '%{address_upper}%'"

        # Add city filter if specified
        if city:
            city_upper = city.upper()
            where_clause = f"({where_clause}) AND (UPPER(CITY) = '{city_upper}' OR UPPER(MUNICIPALITY) = '{city_upper}')"

        response = self.query_parcels(
            where_clause=where_clause,
            result_record_count=100,
        )

        if not response:
            result.error = "Failed to retrieve data"
            return result

        features = response.get("features", [])
        for feature in features:
            try:
                prop = Property.from_arcgis_feature(feature)
                result.properties.append(prop)
            except Exception as e:
                logger.warning(f"Failed to parse property: {e}")

        result.total_count = len(result.properties)
        result.search_time_seconds = time.time() - start_time

        return result

    def search_by_parcel_id(self, parcel_id: str) -> PropertySearchResult:
        """
        Search for a property by parcel ID (PIN).

        Args:
            parcel_id: The parcel identification number

        Returns:
            PropertySearchResult with matching property
        """
        start_time = time.time()
        result = PropertySearchResult()
        result.query_params = {"parcel_id": parcel_id}

        # Clean up parcel ID (remove dashes if present)
        parcel_clean = parcel_id.replace("-", "").strip()

        # Build WHERE clause to match various parcel ID formats
        where_clause = (
            f"PARCEL_ID = '{parcel_id}' OR "
            f"PARCEL_ID = '{parcel_clean}' OR "
            f"PIN = '{parcel_id}' OR "
            f"PIN = '{parcel_clean}' OR "
            f"PARCELPIN = '{parcel_id}' OR "
            f"PARCELPIN = '{parcel_clean}'"
        )

        response = self.query_parcels(
            where_clause=where_clause,
            result_record_count=10,
        )

        if not response:
            result.error = "Failed to retrieve data"
            return result

        features = response.get("features", [])
        for feature in features:
            try:
                prop = Property.from_arcgis_feature(feature)
                result.properties.append(prop)
            except Exception as e:
                logger.warning(f"Failed to parse property: {e}")

        result.total_count = len(result.properties)
        result.search_time_seconds = time.time() - start_time

        return result

    def search_by_owner(
        self,
        owner_name: str,
        city: Optional[str] = "Cleveland Heights",
    ) -> PropertySearchResult:
        """
        Search for properties by owner name.

        Args:
            owner_name: Owner name (partial match supported)
            city: Optional city filter

        Returns:
            PropertySearchResult with matching properties
        """
        start_time = time.time()
        result = PropertySearchResult()
        result.query_params = {"owner_name": owner_name, "city": city}

        owner_upper = owner_name.upper().strip()

        where_clause = (
            f"UPPER(OWNER) LIKE '%{owner_upper}%' OR "
            f"UPPER(OWNER_NAME) LIKE '%{owner_upper}%' OR "
            f"UPPER(OWNERNAME) LIKE '%{owner_upper}%'"
        )

        if city:
            city_upper = city.upper()
            where_clause = f"({where_clause}) AND (UPPER(CITY) = '{city_upper}' OR UPPER(MUNICIPALITY) = '{city_upper}')"

        response = self.query_parcels(
            where_clause=where_clause,
            result_record_count=500,
        )

        if not response:
            result.error = "Failed to retrieve data"
            return result

        features = response.get("features", [])
        for feature in features:
            try:
                prop = Property.from_arcgis_feature(feature)
                result.properties.append(prop)
            except Exception as e:
                logger.warning(f"Failed to parse property: {e}")

        result.total_count = len(result.properties)
        result.search_time_seconds = time.time() - start_time

        return result

    def iter_all_cleveland_heights(
        self,
        batch_size: int = 1000,
        **filters,
    ) -> Generator[Property, None, None]:
        """
        Iterator that yields all Cleveland Heights properties.

        This is useful for processing large datasets without loading
        everything into memory.

        Args:
            batch_size: Number of records to fetch per request
            **filters: Additional filters (property_class, min_value, etc.)

        Yields:
            Property objects one at a time
        """
        offset = 0

        while True:
            result = self.get_cleveland_heights_properties(
                limit=batch_size,
                offset=offset,
                **filters,
            )

            if result.error:
                logger.error(f"Error fetching properties: {result.error}")
                break

            for prop in result.properties:
                yield prop

            if len(result.properties) < batch_size or not result.has_more:
                break

            offset += batch_size

    def get_property_count(
        self,
        where_clause: str = "1=1",
        layer_id: int = 0,
        service_name: str = "parcels_cama",
    ) -> int:
        """
        Get count of properties matching a query without retrieving all data.

        Args:
            where_clause: SQL WHERE clause
            layer_id: Layer index
            service_name: Service name

        Returns:
            Count of matching records
        """
        if service_name not in self.SERVICES:
            return 0

        url = f"{self.SERVICES[service_name]}/{layer_id}/query"

        params = {
            "where": where_clause,
            "returnCountOnly": "true",
        }

        response = self._make_request(url, params)
        if response:
            return response.get("count", 0)
        return 0

    def close(self):
        """Close the session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
