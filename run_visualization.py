#!/usr/bin/env python3
"""
Simple script to run the Cleveland Heights property tax visualization.

Usage:
    python run_visualization.py                    # Use sample data (200 properties)
    python run_visualization.py --fetch            # Fetch live data from Cuyahoga County
    python run_visualization.py --fetch --limit 500  # Fetch 500 properties
"""

import sys
import os

# Add the project to path if running from project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cuyahoga_scraper.visualize import generate_all_visualizations, get_sample_properties
from cuyahoga_scraper.scraper import CuyahogaPropertyScraper


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate Cleveland Heights property tax visualizations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_visualization.py                      # Use 200 sample properties
    python run_visualization.py --fetch              # Fetch real data
    python run_visualization.py --fetch --limit 1000 # Fetch 1000 properties
    python run_visualization.py -o ./charts          # Save to ./charts folder
        """,
    )
    parser.add_argument(
        "-o", "--output-dir",
        default="./output",
        help="Output directory for charts (default: ./output)"
    )
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="Fetch live data from Cuyahoga County (requires internet)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=500,
        help="Number of properties to fetch when using --fetch (default: 500)"
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Display charts in window (requires display)"
    )

    args = parser.parse_args()

    properties = None

    if args.fetch:
        print(f"Fetching up to {args.limit} properties from Cuyahoga County...")
        print("(This may take a minute...)")
        try:
            with CuyahogaPropertyScraper() as scraper:
                result = scraper.get_cleveland_heights_properties(limit=args.limit)
                if result.properties:
                    properties = result.properties
                    print(f"Successfully fetched {len(properties)} properties")
                else:
                    print(f"Could not fetch data: {result.error}")
                    print("Falling back to sample data...")
        except Exception as e:
            print(f"Error: {e}")
            print("Falling back to sample data...")

    if properties is None:
        print("Using sample data (200 Cleveland Heights properties)...")
        properties = get_sample_properties()

    # Generate visualizations
    print(f"\nGenerating visualizations for {len(properties)} properties...")
    files = generate_all_visualizations(
        properties=properties,
        output_dir=args.output_dir,
        show=args.show,
    )

    print(f"\n{'='*50}")
    print(f"Generated {len(files)} charts in {args.output_dir}/")
    print(f"{'='*50}")
    for f in files:
        print(f"  - {os.path.basename(f)}")

    print(f"\nTo view the charts, open:")
    print(f"  {os.path.abspath(args.output_dir)}/cleveland_heights_tax_analysis.png")


if __name__ == "__main__":
    main()
