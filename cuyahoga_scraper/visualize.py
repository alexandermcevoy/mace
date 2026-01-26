#!/usr/bin/env python3
"""
Visualization module for Cleveland Heights property data.

Creates charts and visualizations from property tax data.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from typing import List, Optional, Dict, Tuple
from collections import defaultdict
from pathlib import Path
import json

from .models import Property
from .scraper import CuyahogaPropertyScraper


# Sample data representing realistic Cleveland Heights properties
# Used when live data cannot be fetched
SAMPLE_PROPERTIES = [
    # Historic district properties (1900-1930)
    {"parcel_id": "561-01-001", "address": "2345 Overlook Rd", "year_built": 1925, "market_value_total": 285000, "assessed_value": 99750, "annual_taxes": 7182, "property_class": "R", "living_area_sqft": 2400},
    {"parcel_id": "561-01-002", "address": "2401 Overlook Rd", "year_built": 1922, "market_value_total": 310000, "assessed_value": 108500, "annual_taxes": 7812, "property_class": "R", "living_area_sqft": 2650},
    {"parcel_id": "561-02-015", "address": "1890 Coventry Rd", "year_built": 1918, "market_value_total": 195000, "assessed_value": 68250, "annual_taxes": 4914, "property_class": "R", "living_area_sqft": 1800},
    {"parcel_id": "561-02-022", "address": "2156 Lennox Rd", "year_built": 1928, "market_value_total": 225000, "assessed_value": 78750, "annual_taxes": 5670, "property_class": "R", "living_area_sqft": 2100},
    {"parcel_id": "561-03-008", "address": "2678 Fairmount Blvd", "year_built": 1924, "market_value_total": 425000, "assessed_value": 148750, "annual_taxes": 10710, "property_class": "R", "living_area_sqft": 3200},
    {"parcel_id": "561-03-019", "address": "2890 Fairmount Blvd", "year_built": 1920, "market_value_total": 520000, "assessed_value": 182000, "annual_taxes": 13104, "property_class": "R", "living_area_sqft": 4100},

    # Mid-century properties (1940-1970)
    {"parcel_id": "562-04-011", "address": "3456 Mayfield Rd", "year_built": 1952, "market_value_total": 175000, "assessed_value": 61250, "annual_taxes": 4410, "property_class": "R", "living_area_sqft": 1450},
    {"parcel_id": "562-04-025", "address": "3512 Mayfield Rd", "year_built": 1948, "market_value_total": 185000, "assessed_value": 64750, "annual_taxes": 4662, "property_class": "R", "living_area_sqft": 1550},
    {"parcel_id": "562-05-003", "address": "1245 Yellowstone Rd", "year_built": 1955, "market_value_total": 165000, "assessed_value": 57750, "annual_taxes": 4158, "property_class": "R", "living_area_sqft": 1380},
    {"parcel_id": "562-05-018", "address": "1367 Yellowstone Rd", "year_built": 1960, "market_value_total": 155000, "assessed_value": 54250, "annual_taxes": 3906, "property_class": "R", "living_area_sqft": 1320},
    {"parcel_id": "562-06-007", "address": "2089 Noble Rd", "year_built": 1958, "market_value_total": 145000, "assessed_value": 50750, "annual_taxes": 3654, "property_class": "R", "living_area_sqft": 1250},
    {"parcel_id": "562-06-021", "address": "2145 Noble Rd", "year_built": 1965, "market_value_total": 138000, "assessed_value": 48300, "annual_taxes": 3478, "property_class": "R", "living_area_sqft": 1180},

    # Later properties (1970-2000)
    {"parcel_id": "563-07-004", "address": "4567 Warrensville Rd", "year_built": 1975, "market_value_total": 125000, "assessed_value": 43750, "annual_taxes": 3150, "property_class": "R", "living_area_sqft": 1100},
    {"parcel_id": "563-07-016", "address": "4623 Warrensville Rd", "year_built": 1978, "market_value_total": 135000, "assessed_value": 47250, "annual_taxes": 3402, "property_class": "R", "living_area_sqft": 1200},
    {"parcel_id": "563-08-009", "address": "1789 Lee Rd", "year_built": 1985, "market_value_total": 198000, "assessed_value": 69300, "annual_taxes": 4990, "property_class": "R", "living_area_sqft": 1650},
    {"parcel_id": "563-08-023", "address": "1845 Lee Rd", "year_built": 1992, "market_value_total": 215000, "assessed_value": 75250, "annual_taxes": 5418, "property_class": "R", "living_area_sqft": 1800},

    # Commercial properties
    {"parcel_id": "564-09-001", "address": "2200 Lee Rd", "year_built": 1945, "market_value_total": 850000, "assessed_value": 297500, "annual_taxes": 22313, "property_class": "C", "living_area_sqft": 8500},
    {"parcel_id": "564-09-012", "address": "2287 Lee Rd", "year_built": 1955, "market_value_total": 425000, "assessed_value": 148750, "annual_taxes": 11156, "property_class": "C", "living_area_sqft": 4200},
    {"parcel_id": "564-10-005", "address": "1800 Coventry Rd", "year_built": 1935, "market_value_total": 675000, "assessed_value": 236250, "annual_taxes": 17719, "property_class": "C", "living_area_sqft": 6800},
    {"parcel_id": "564-10-019", "address": "1856 Coventry Rd", "year_built": 1940, "market_value_total": 525000, "assessed_value": 183750, "annual_taxes": 13781, "property_class": "C", "living_area_sqft": 5200},

    # Multi-family properties
    {"parcel_id": "565-11-002", "address": "2450 Derbyshire Rd", "year_built": 1930, "market_value_total": 380000, "assessed_value": 133000, "annual_taxes": 9576, "property_class": "M", "living_area_sqft": 4800},
    {"parcel_id": "565-11-014", "address": "2512 Derbyshire Rd", "year_built": 1928, "market_value_total": 420000, "assessed_value": 147000, "annual_taxes": 10584, "property_class": "M", "living_area_sqft": 5400},
    {"parcel_id": "565-12-008", "address": "3100 Euclid Heights Blvd", "year_built": 1925, "market_value_total": 550000, "assessed_value": 192500, "annual_taxes": 13860, "property_class": "M", "living_area_sqft": 7200},
    {"parcel_id": "565-12-020", "address": "3156 Euclid Heights Blvd", "year_built": 1932, "market_value_total": 485000, "assessed_value": 169750, "annual_taxes": 12222, "property_class": "M", "living_area_sqft": 6100},
]


def get_sample_properties() -> List[Property]:
    """
    Get sample Cleveland Heights properties for demonstration.

    Returns:
        List of Property objects with sample data
    """
    properties = []
    for data in SAMPLE_PROPERTIES:
        prop = Property(
            parcel_id=data["parcel_id"],
            address=data["address"],
            city="CLEVELAND HEIGHTS",
            year_built=data["year_built"],
            market_value_total=data["market_value_total"],
            assessed_value=data["assessed_value"],
            annual_taxes=data["annual_taxes"],
            property_class=data["property_class"],
            living_area_sqft=data["living_area_sqft"],
            data_source="Sample Data",
        )
        properties.append(prop)
    return properties


def calculate_tax_rate(prop: Property) -> Optional[float]:
    """
    Calculate effective property tax rate.

    Tax rate = (Annual Taxes / Market Value) * 100

    Args:
        prop: Property object

    Returns:
        Tax rate as percentage, or None if calculation not possible
    """
    if prop.annual_taxes and prop.market_value_total and prop.market_value_total > 0:
        return (prop.annual_taxes / prop.market_value_total) * 100
    return None


def calculate_assessed_tax_rate(prop: Property) -> Optional[float]:
    """
    Calculate tax rate based on assessed value.

    Tax rate = (Annual Taxes / Assessed Value) * 100

    Args:
        prop: Property object

    Returns:
        Tax rate as percentage based on assessed value
    """
    if prop.annual_taxes and prop.assessed_value and prop.assessed_value > 0:
        return (prop.annual_taxes / prop.assessed_value) * 100
    return None


def plot_tax_rates_by_property_class(
    properties: List[Property],
    output_path: str = "tax_rates_by_class.png",
    show: bool = False,
) -> str:
    """
    Create bar chart of average property tax rates by property class.

    Args:
        properties: List of Property objects
        output_path: Path to save the chart
        show: Whether to display the chart

    Returns:
        Path to saved chart
    """
    # Group properties by class and calculate average tax rates
    class_rates: Dict[str, List[float]] = defaultdict(list)

    for prop in properties:
        rate = calculate_tax_rate(prop)
        if rate is not None and prop.property_class:
            class_rates[prop.property_class].append(rate)

    # Calculate averages
    class_labels = {
        "R": "Residential",
        "C": "Commercial",
        "M": "Multi-Family",
        "I": "Industrial",
        "A": "Agricultural",
        "E": "Exempt",
    }

    categories = []
    avg_rates = []
    counts = []

    for class_code in sorted(class_rates.keys()):
        rates = class_rates[class_code]
        label = class_labels.get(class_code, class_code)
        categories.append(f"{label}\n(n={len(rates)})")
        avg_rates.append(sum(rates) / len(rates))
        counts.append(len(rates))

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create bars with colors
    colors = ['#2ecc71', '#3498db', '#9b59b6', '#e74c3c', '#f39c12', '#95a5a6']
    bars = ax.bar(categories, avg_rates, color=colors[:len(categories)], edgecolor='black', linewidth=1.2)

    # Add value labels on bars
    for bar, rate in zip(bars, avg_rates):
        height = bar.get_height()
        ax.annotate(f'{rate:.2f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=12, fontweight='bold')

    # Styling
    ax.set_ylabel('Average Effective Tax Rate (%)', fontsize=12)
    ax.set_xlabel('Property Class', fontsize=12)
    ax.set_title('Cleveland Heights Property Tax Rates by Property Class', fontsize=14, fontweight='bold')
    ax.set_ylim(0, max(avg_rates) * 1.2)

    # Add grid
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)

    # Add note about calculation
    ax.text(0.02, 0.98, 'Tax Rate = Annual Taxes / Market Value × 100',
            transform=ax.transAxes, fontsize=9, verticalalignment='top',
            style='italic', color='gray')

    plt.tight_layout()

    # Save
    plt.savefig(output_path, dpi=150, bbox_inches='tight')

    if show:
        plt.show()

    plt.close()
    return output_path


def plot_tax_rates_by_value_range(
    properties: List[Property],
    output_path: str = "tax_rates_by_value.png",
    show: bool = False,
) -> str:
    """
    Create bar chart of average property tax rates by property value range.

    Args:
        properties: List of Property objects
        output_path: Path to save the chart
        show: Whether to display the chart

    Returns:
        Path to saved chart
    """
    # Define value ranges
    ranges = [
        (0, 150000, "$0-150K"),
        (150000, 250000, "$150K-250K"),
        (250000, 400000, "$250K-400K"),
        (400000, 600000, "$400K-600K"),
        (600000, float('inf'), "$600K+"),
    ]

    # Group properties by value range
    range_rates: Dict[str, List[float]] = defaultdict(list)

    for prop in properties:
        rate = calculate_tax_rate(prop)
        if rate is not None and prop.market_value_total:
            for low, high, label in ranges:
                if low <= prop.market_value_total < high:
                    range_rates[label].append(rate)
                    break

    # Prepare data
    categories = []
    avg_rates = []

    for _, _, label in ranges:
        if label in range_rates:
            rates = range_rates[label]
            categories.append(f"{label}\n(n={len(rates)})")
            avg_rates.append(sum(rates) / len(rates))

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create gradient colors
    colors = plt.cm.Blues([(i + 3) / (len(categories) + 3) for i in range(len(categories))])
    bars = ax.bar(categories, avg_rates, color=colors, edgecolor='black', linewidth=1.2)

    # Add value labels
    for bar, rate in zip(bars, avg_rates):
        height = bar.get_height()
        ax.annotate(f'{rate:.2f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=12, fontweight='bold')

    # Styling
    ax.set_ylabel('Average Effective Tax Rate (%)', fontsize=12)
    ax.set_xlabel('Property Value Range', fontsize=12)
    ax.set_title('Cleveland Heights Property Tax Rates by Value Range', fontsize=14, fontweight='bold')
    ax.set_ylim(0, max(avg_rates) * 1.2)

    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')

    if show:
        plt.show()

    plt.close()
    return output_path


def plot_tax_rates_by_year_built(
    properties: List[Property],
    output_path: str = "tax_rates_by_year.png",
    show: bool = False,
) -> str:
    """
    Create bar chart of average property tax rates by decade built.

    Args:
        properties: List of Property objects
        output_path: Path to save the chart
        show: Whether to display the chart

    Returns:
        Path to saved chart
    """
    # Group by decade
    decade_rates: Dict[str, List[float]] = defaultdict(list)

    for prop in properties:
        rate = calculate_tax_rate(prop)
        if rate is not None and prop.year_built:
            decade = (prop.year_built // 10) * 10
            label = f"{decade}s"
            decade_rates[label].append(rate)

    # Sort by decade
    sorted_decades = sorted(decade_rates.keys())

    categories = []
    avg_rates = []

    for decade in sorted_decades:
        rates = decade_rates[decade]
        categories.append(f"{decade}\n(n={len(rates)})")
        avg_rates.append(sum(rates) / len(rates))

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))

    # Create gradient colors
    colors = plt.cm.Greens([(i + 3) / (len(categories) + 3) for i in range(len(categories))])
    bars = ax.bar(categories, avg_rates, color=colors, edgecolor='black', linewidth=1.2)

    # Add value labels
    for bar, rate in zip(bars, avg_rates):
        height = bar.get_height()
        ax.annotate(f'{rate:.2f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=11, fontweight='bold')

    # Styling
    ax.set_ylabel('Average Effective Tax Rate (%)', fontsize=12)
    ax.set_xlabel('Decade Built', fontsize=12)
    ax.set_title('Cleveland Heights Property Tax Rates by Decade Built', fontsize=14, fontweight='bold')
    ax.set_ylim(0, max(avg_rates) * 1.2)

    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')

    if show:
        plt.show()

    plt.close()
    return output_path


def plot_comprehensive_tax_analysis(
    properties: List[Property],
    output_path: str = "cleveland_heights_tax_analysis.png",
    show: bool = False,
) -> str:
    """
    Create comprehensive multi-panel tax rate analysis.

    Args:
        properties: List of Property objects
        output_path: Path to save the chart
        show: Whether to display the chart

    Returns:
        Path to saved chart
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Cleveland Heights Property Tax Rate Analysis', fontsize=16, fontweight='bold', y=1.02)

    # Panel 1: Tax rates by property class
    ax1 = axes[0, 0]
    class_rates = defaultdict(list)
    for prop in properties:
        rate = calculate_tax_rate(prop)
        if rate and prop.property_class:
            class_rates[prop.property_class].append(rate)

    class_labels = {"R": "Residential", "C": "Commercial", "M": "Multi-Family"}
    cats1 = [class_labels.get(k, k) for k in sorted(class_rates.keys())]
    vals1 = [sum(v)/len(v) for k, v in sorted(class_rates.items())]

    bars1 = ax1.bar(cats1, vals1, color=['#2ecc71', '#3498db', '#9b59b6'][:len(cats1)], edgecolor='black')
    ax1.set_ylabel('Avg Tax Rate (%)')
    ax1.set_title('By Property Class')
    for bar, val in zip(bars1, vals1):
        ax1.annotate(f'{val:.2f}%', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 3), textcoords="offset points", ha='center', fontsize=10, fontweight='bold')
    ax1.yaxis.grid(True, linestyle='--', alpha=0.5)

    # Panel 2: Tax rates by value range
    ax2 = axes[0, 1]
    ranges = [(0, 200000, "<$200K"), (200000, 400000, "$200-400K"), (400000, float('inf'), ">$400K")]
    range_rates = defaultdict(list)
    for prop in properties:
        rate = calculate_tax_rate(prop)
        if rate and prop.market_value_total:
            for low, high, lbl in ranges:
                if low <= prop.market_value_total < high:
                    range_rates[lbl].append(rate)
                    break

    cats2 = [lbl for _, _, lbl in ranges if lbl in range_rates]
    vals2 = [sum(range_rates[lbl])/len(range_rates[lbl]) for lbl in cats2]

    bars2 = ax2.bar(cats2, vals2, color=plt.cm.Blues([0.4, 0.6, 0.8])[:len(cats2)], edgecolor='black')
    ax2.set_ylabel('Avg Tax Rate (%)')
    ax2.set_title('By Property Value')
    for bar, val in zip(bars2, vals2):
        ax2.annotate(f'{val:.2f}%', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 3), textcoords="offset points", ha='center', fontsize=10, fontweight='bold')
    ax2.yaxis.grid(True, linestyle='--', alpha=0.5)

    # Panel 3: Distribution histogram
    ax3 = axes[1, 0]
    all_rates = [calculate_tax_rate(p) for p in properties]
    all_rates = [r for r in all_rates if r is not None]

    ax3.hist(all_rates, bins=15, color='#e74c3c', edgecolor='black', alpha=0.7)
    ax3.axvline(sum(all_rates)/len(all_rates), color='black', linestyle='--', linewidth=2, label=f'Mean: {sum(all_rates)/len(all_rates):.2f}%')
    ax3.set_xlabel('Tax Rate (%)')
    ax3.set_ylabel('Number of Properties')
    ax3.set_title('Tax Rate Distribution')
    ax3.legend()
    ax3.yaxis.grid(True, linestyle='--', alpha=0.5)

    # Panel 4: Summary statistics table
    ax4 = axes[1, 1]
    ax4.axis('off')

    # Calculate statistics
    total_props = len(properties)
    props_with_tax = len([p for p in properties if p.annual_taxes])
    avg_rate = sum(all_rates) / len(all_rates) if all_rates else 0
    min_rate = min(all_rates) if all_rates else 0
    max_rate = max(all_rates) if all_rates else 0
    avg_value = sum(p.market_value_total for p in properties if p.market_value_total) / total_props
    avg_tax = sum(p.annual_taxes for p in properties if p.annual_taxes) / props_with_tax

    stats_text = f"""
    Cleveland Heights Property Tax Summary
    {'='*45}

    Total Properties:           {total_props:,}

    Average Market Value:       ${avg_value:,.0f}
    Average Annual Taxes:       ${avg_tax:,.0f}

    Average Effective Tax Rate: {avg_rate:.2f}%
    Minimum Tax Rate:           {min_rate:.2f}%
    Maximum Tax Rate:           {max_rate:.2f}%

    {'='*45}
    Data Source: Cuyahoga County ArcGIS
    """

    ax4.text(0.1, 0.9, stats_text, transform=ax4.transAxes,
             fontsize=11, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')

    if show:
        plt.show()

    plt.close()
    return output_path


def generate_all_visualizations(
    properties: Optional[List[Property]] = None,
    output_dir: str = ".",
    show: bool = False,
) -> List[str]:
    """
    Generate all property tax visualizations.

    Args:
        properties: List of Property objects (uses sample data if None)
        output_dir: Directory for output files
        show: Whether to display charts

    Returns:
        List of paths to generated files
    """
    if properties is None:
        print("Using sample Cleveland Heights property data...")
        properties = get_sample_properties()

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    generated_files = []

    print(f"Generating visualizations for {len(properties)} properties...")

    # Generate individual charts
    path1 = plot_tax_rates_by_property_class(
        properties,
        str(output_dir / "tax_rates_by_class.png"),
        show=show,
    )
    generated_files.append(path1)
    print(f"  Created: {path1}")

    path2 = plot_tax_rates_by_value_range(
        properties,
        str(output_dir / "tax_rates_by_value.png"),
        show=show,
    )
    generated_files.append(path2)
    print(f"  Created: {path2}")

    path3 = plot_tax_rates_by_year_built(
        properties,
        str(output_dir / "tax_rates_by_year.png"),
        show=show,
    )
    generated_files.append(path3)
    print(f"  Created: {path3}")

    # Generate comprehensive analysis
    path4 = plot_comprehensive_tax_analysis(
        properties,
        str(output_dir / "cleveland_heights_tax_analysis.png"),
        show=show,
    )
    generated_files.append(path4)
    print(f"  Created: {path4}")

    return generated_files


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate Cleveland Heights property tax visualizations")
    parser.add_argument("-o", "--output-dir", default=".", help="Output directory for charts")
    parser.add_argument("--show", action="store_true", help="Display charts")
    parser.add_argument("--fetch", action="store_true", help="Fetch live data from Cuyahoga County")
    parser.add_argument("--limit", type=int, default=100, help="Limit properties to fetch")

    args = parser.parse_args()

    properties = None

    if args.fetch:
        print("Attempting to fetch live data from Cuyahoga County...")
        try:
            scraper = CuyahogaPropertyScraper()
            result = scraper.get_cleveland_heights_properties(limit=args.limit)
            if result.properties:
                properties = result.properties
                print(f"Fetched {len(properties)} properties")
            else:
                print("Could not fetch live data, using sample data...")
            scraper.close()
        except Exception as e:
            print(f"Error fetching data: {e}")
            print("Using sample data...")

    files = generate_all_visualizations(
        properties=properties,
        output_dir=args.output_dir,
        show=args.show,
    )

    print(f"\nGenerated {len(files)} visualization files")
