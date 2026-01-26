#!/usr/bin/env python3
"""
Command-line interface for Cuyahoga County Property Scraper.

Usage:
    python -m cuyahoga_scraper.cli [command] [options]

Examples:
    # Get all Cleveland Heights properties
    python -m cuyahoga_scraper.cli fetch --output properties.csv

    # Search by address
    python -m cuyahoga_scraper.cli search --address "123 Main St"

    # Search by parcel ID
    python -m cuyahoga_scraper.cli search --parcel "561-01-001"

    # Search by owner name
    python -m cuyahoga_scraper.cli search --owner "Smith"

    # Get properties with filters
    python -m cuyahoga_scraper.cli fetch --property-class R --min-value 100000 --output residential.csv
"""

import argparse
import sys
import logging
from pathlib import Path

from .scraper import CuyahogaPropertyScraper
from .export import PropertyExporter, generate_filename


def setup_logging(verbose: bool = False):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def cmd_fetch(args):
    """Fetch Cleveland Heights properties."""
    print(f"Fetching Cleveland Heights properties...")

    with CuyahogaPropertyScraper(
        timeout=args.timeout,
        rate_limit_delay=args.delay,
    ) as scraper:
        result = scraper.get_cleveland_heights_properties(
            limit=args.limit,
            property_class=args.property_class,
            min_value=args.min_value,
            max_value=args.max_value,
            year_built_min=args.year_min,
            year_built_max=args.year_max,
        )

    if result.error:
        print(f"Error: {result.error}", file=sys.stderr)
        return 1

    print(f"Found {result.total_count} properties in {result.search_time_seconds:.2f}s")

    if result.properties:
        # Determine output path
        output_path = args.output or generate_filename(
            prefix="cleveland_heights_properties",
            format=args.format,
        )

        # Export data
        exported = PropertyExporter.export_search_result(
            result,
            output_path,
            format=args.format,
        )
        print(f"Exported to: {exported}")

    return 0


def cmd_search(args):
    """Search for properties."""
    with CuyahogaPropertyScraper(
        timeout=args.timeout,
        rate_limit_delay=args.delay,
    ) as scraper:
        if args.address:
            print(f"Searching by address: {args.address}")
            result = scraper.search_by_address(
                args.address,
                city="Cleveland Heights" if not args.all_cities else None,
            )
        elif args.parcel:
            print(f"Searching by parcel ID: {args.parcel}")
            result = scraper.search_by_parcel_id(args.parcel)
        elif args.owner:
            print(f"Searching by owner: {args.owner}")
            result = scraper.search_by_owner(
                args.owner,
                city="Cleveland Heights" if not args.all_cities else None,
            )
        else:
            print("Error: Must specify --address, --parcel, or --owner", file=sys.stderr)
            return 1

    if result.error:
        print(f"Error: {result.error}", file=sys.stderr)
        return 1

    print(f"Found {result.total_count} properties in {result.search_time_seconds:.2f}s")

    if result.properties:
        # Print summary
        for prop in result.properties:
            print(f"\n--- {prop.parcel_id} ---")
            print(f"  Address: {prop.address}, {prop.city}")
            print(f"  Owner: {prop.owner_name or 'N/A'}")
            print(f"  Value: ${prop.market_value_total:,.0f}" if prop.market_value_total else "  Value: N/A")
            print(f"  Year Built: {prop.year_built or 'N/A'}")
            print(f"  Beds/Baths: {prop.bedrooms or 'N/A'}/{prop.bathrooms or 'N/A'}")
            print(f"  Sq Ft: {prop.living_area_sqft:,}" if prop.living_area_sqft else "  Sq Ft: N/A")

        # Export if output specified
        if args.output:
            exported = PropertyExporter.export_search_result(
                result,
                args.output,
                format=args.format,
            )
            print(f"\nExported to: {exported}")

    return 0


def cmd_info(args):
    """Get service information."""
    with CuyahogaPropertyScraper() as scraper:
        print("Cuyahoga County ArcGIS Services")
        print("=" * 50)

        for service_name in scraper.SERVICES:
            print(f"\n{service_name}:")
            info = scraper.get_service_info(service_name)
            if info:
                print(f"  Description: {info.get('description', 'N/A')}")
                layers = info.get("layers", [])
                print(f"  Layers: {len(layers)}")
                for layer in layers:
                    print(f"    - [{layer.get('id')}] {layer.get('name')}")
            else:
                print("  (Unable to retrieve info)")

        if args.fields:
            print("\n" + "=" * 50)
            print("Fields for main parcels layer:")
            fields = scraper.get_field_names(layer_id=0, service_name="parcels_cama")
            if fields:
                for field in fields:
                    print(f"  - {field}")
            else:
                print("  (Unable to retrieve fields)")

    return 0


def cmd_count(args):
    """Get property count."""
    with CuyahogaPropertyScraper() as scraper:
        # Build WHERE clause for Cleveland Heights
        city_conditions = " OR ".join(
            [f"UPPER(CITY) = '{city}'" for city in scraper.CLEVELAND_HEIGHTS_IDENTIFIERS]
            + [f"UPPER(MUNICIPALITY) = '{city}'" for city in scraper.CLEVELAND_HEIGHTS_IDENTIFIERS]
        )

        count = scraper.get_property_count(where_clause=f"({city_conditions})")
        print(f"Total Cleveland Heights properties: {count}")

    return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Cuyahoga County Property Scraper - Cleveland Heights",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout (seconds)")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between requests (seconds)")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Fetch command
    fetch_parser = subparsers.add_parser("fetch", help="Fetch Cleveland Heights properties")
    fetch_parser.add_argument("-o", "--output", help="Output file path")
    fetch_parser.add_argument("-f", "--format", choices=["csv", "json", "jsonl", "geojson"], default="csv", help="Output format")
    fetch_parser.add_argument("-l", "--limit", type=int, help="Maximum number of properties to fetch")
    fetch_parser.add_argument("--property-class", help="Filter by property class (e.g., R for residential)")
    fetch_parser.add_argument("--min-value", type=float, help="Minimum market value")
    fetch_parser.add_argument("--max-value", type=float, help="Maximum market value")
    fetch_parser.add_argument("--year-min", type=int, help="Minimum year built")
    fetch_parser.add_argument("--year-max", type=int, help="Maximum year built")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for properties")
    search_parser.add_argument("-a", "--address", help="Search by street address")
    search_parser.add_argument("-p", "--parcel", help="Search by parcel ID")
    search_parser.add_argument("--owner", help="Search by owner name")
    search_parser.add_argument("--all-cities", action="store_true", help="Search all cities, not just Cleveland Heights")
    search_parser.add_argument("-o", "--output", help="Output file path")
    search_parser.add_argument("-f", "--format", choices=["csv", "json", "jsonl", "geojson"], default="csv", help="Output format")

    # Info command
    info_parser = subparsers.add_parser("info", help="Get service information")
    info_parser.add_argument("--fields", action="store_true", help="Show field names")

    # Count command
    subparsers.add_parser("count", help="Get Cleveland Heights property count")

    args = parser.parse_args()
    setup_logging(args.verbose)

    if args.command == "fetch":
        return cmd_fetch(args)
    elif args.command == "search":
        return cmd_search(args)
    elif args.command == "info":
        return cmd_info(args)
    elif args.command == "count":
        return cmd_count(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
