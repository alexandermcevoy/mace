"""
Export utilities for Cuyahoga County property data.
"""

import csv
import json
from typing import List, Optional, TextIO
from pathlib import Path
from datetime import datetime

from .models import Property, PropertySearchResult


class PropertyExporter:
    """Export property data to various formats."""

    # Default fields to export (in order)
    DEFAULT_FIELDS = [
        "parcel_id",
        "address",
        "city",
        "state",
        "zip_code",
        "owner_name",
        "property_class",
        "land_use",
        "year_built",
        "bedrooms",
        "bathrooms",
        "living_area_sqft",
        "lot_size_sqft",
        "market_value_land",
        "market_value_building",
        "market_value_total",
        "assessed_value",
        "annual_taxes",
        "last_sale_date",
        "last_sale_price",
        "latitude",
        "longitude",
    ]

    @classmethod
    def to_csv(
        cls,
        properties: List[Property],
        output_path: str,
        fields: Optional[List[str]] = None,
        include_header: bool = True,
    ) -> str:
        """
        Export properties to CSV file.

        Args:
            properties: List of Property objects
            output_path: Path for output CSV file
            fields: List of fields to include (None for defaults)
            include_header: Whether to include header row

        Returns:
            Path to created file
        """
        fields = fields or cls.DEFAULT_FIELDS
        path = Path(output_path)

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")

            if include_header:
                writer.writeheader()

            for prop in properties:
                row = prop.to_dict()
                writer.writerow(row)

        return str(path)

    @classmethod
    def to_csv_stream(
        cls,
        properties: List[Property],
        output: TextIO,
        fields: Optional[List[str]] = None,
        include_header: bool = True,
    ) -> None:
        """
        Export properties to CSV stream (file-like object).

        Args:
            properties: List of Property objects
            output: File-like object to write to
            fields: List of fields to include
            include_header: Whether to include header row
        """
        fields = fields or cls.DEFAULT_FIELDS
        writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")

        if include_header:
            writer.writeheader()

        for prop in properties:
            row = prop.to_dict()
            writer.writerow(row)

    @classmethod
    def to_json(
        cls,
        properties: List[Property],
        output_path: str,
        pretty: bool = True,
        include_metadata: bool = True,
    ) -> str:
        """
        Export properties to JSON file.

        Args:
            properties: List of Property objects
            output_path: Path for output JSON file
            pretty: Whether to format JSON with indentation
            include_metadata: Whether to include export metadata

        Returns:
            Path to created file
        """
        path = Path(output_path)

        data = {
            "properties": [p.to_dict() for p in properties],
        }

        if include_metadata:
            data["metadata"] = {
                "export_date": datetime.now().isoformat(),
                "total_count": len(properties),
                "source": "Cuyahoga County Property Scraper",
            }

        with open(path, "w", encoding="utf-8") as f:
            if pretty:
                json.dump(data, f, indent=2)
            else:
                json.dump(data, f)

        return str(path)

    @classmethod
    def to_jsonl(
        cls,
        properties: List[Property],
        output_path: str,
    ) -> str:
        """
        Export properties to JSON Lines format (one JSON object per line).

        This format is useful for streaming and processing large datasets.

        Args:
            properties: List of Property objects
            output_path: Path for output JSONL file

        Returns:
            Path to created file
        """
        path = Path(output_path)

        with open(path, "w", encoding="utf-8") as f:
            for prop in properties:
                f.write(json.dumps(prop.to_dict()) + "\n")

        return str(path)

    @classmethod
    def to_geojson(
        cls,
        properties: List[Property],
        output_path: str,
    ) -> str:
        """
        Export properties to GeoJSON format.

        Properties without coordinates will be skipped.

        Args:
            properties: List of Property objects
            output_path: Path for output GeoJSON file

        Returns:
            Path to created file
        """
        path = Path(output_path)

        features = []
        for prop in properties:
            if prop.latitude is not None and prop.longitude is not None:
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [prop.longitude, prop.latitude],
                    },
                    "properties": {
                        k: v
                        for k, v in prop.to_dict().items()
                        if k not in ("latitude", "longitude", "retrieved_at")
                    },
                }
                features.append(feature)

        geojson = {
            "type": "FeatureCollection",
            "features": features,
            "metadata": {
                "export_date": datetime.now().isoformat(),
                "total_count": len(features),
                "source": "Cuyahoga County Property Scraper",
            },
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(geojson, f, indent=2)

        return str(path)

    @classmethod
    def export_search_result(
        cls,
        result: PropertySearchResult,
        output_path: str,
        format: str = "csv",
    ) -> str:
        """
        Export a PropertySearchResult to file.

        Args:
            result: PropertySearchResult object
            output_path: Base path for output file
            format: Output format (csv, json, jsonl, geojson)

        Returns:
            Path to created file
        """
        properties = result.properties

        if format == "csv":
            return cls.to_csv(properties, output_path)
        elif format == "json":
            return cls.to_json(properties, output_path)
        elif format == "jsonl":
            return cls.to_jsonl(properties, output_path)
        elif format == "geojson":
            return cls.to_geojson(properties, output_path)
        else:
            raise ValueError(f"Unsupported format: {format}")


def generate_filename(
    prefix: str = "cleveland_heights_properties",
    format: str = "csv",
    include_timestamp: bool = True,
) -> str:
    """
    Generate a filename for export.

    Args:
        prefix: Filename prefix
        format: File format/extension
        include_timestamp: Whether to include timestamp

    Returns:
        Generated filename
    """
    if include_timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.{format}"
    return f"{prefix}.{format}"
