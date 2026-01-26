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
from .sample_data import SAMPLE_PROPERTIES, generate_sample_properties


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


def plot_annual_taxes_by_property_class(
    properties: List[Property],
    output_path: str = "annual_taxes_by_class.png",
    show: bool = False,
) -> str:
    """
    Create bar chart of average annual property taxes by property class.

    Args:
        properties: List of Property objects
        output_path: Path to save the chart
        show: Whether to display the chart

    Returns:
        Path to saved chart
    """
    # Group properties by class and collect annual taxes
    class_taxes: Dict[str, List[float]] = defaultdict(list)

    for prop in properties:
        if prop.annual_taxes and prop.property_class:
            class_taxes[prop.property_class].append(prop.annual_taxes)

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
    avg_taxes = []
    counts = []

    for class_code in sorted(class_taxes.keys()):
        taxes = class_taxes[class_code]
        label = class_labels.get(class_code, class_code)
        categories.append(f"{label}\n(n={len(taxes)})")
        avg_taxes.append(sum(taxes) / len(taxes))
        counts.append(len(taxes))

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create bars with colors
    colors = ['#2ecc71', '#3498db', '#9b59b6', '#e74c3c', '#f39c12', '#95a5a6']
    bars = ax.bar(categories, avg_taxes, color=colors[:len(categories)], edgecolor='black', linewidth=1.2)

    # Add value labels on bars
    for bar, tax in zip(bars, avg_taxes):
        height = bar.get_height()
        ax.annotate(f'${tax:,.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=12, fontweight='bold')

    # Styling
    ax.set_ylabel('Average Annual Property Tax ($)', fontsize=12)
    ax.set_xlabel('Property Class', fontsize=12)
    ax.set_title('Cleveland Heights Annual Property Taxes by Property Class', fontsize=14, fontweight='bold')
    ax.set_ylim(0, max(avg_taxes) * 1.2)

    # Format y-axis as currency
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))

    # Add grid
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)

    plt.tight_layout()

    # Save
    plt.savefig(output_path, dpi=150, bbox_inches='tight')

    if show:
        plt.show()

    plt.close()
    return output_path


def plot_annual_taxes_by_value_range(
    properties: List[Property],
    output_path: str = "annual_taxes_by_value.png",
    show: bool = False,
) -> str:
    """
    Create bar chart of average annual property taxes by property value range.

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
    range_taxes: Dict[str, List[float]] = defaultdict(list)

    for prop in properties:
        if prop.annual_taxes and prop.market_value_total:
            for low, high, label in ranges:
                if low <= prop.market_value_total < high:
                    range_taxes[label].append(prop.annual_taxes)
                    break

    # Prepare data
    categories = []
    avg_taxes = []

    for _, _, label in ranges:
        if label in range_taxes:
            taxes = range_taxes[label]
            categories.append(f"{label}\n(n={len(taxes)})")
            avg_taxes.append(sum(taxes) / len(taxes))

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create gradient colors
    colors = plt.cm.Blues([(i + 3) / (len(categories) + 3) for i in range(len(categories))])
    bars = ax.bar(categories, avg_taxes, color=colors, edgecolor='black', linewidth=1.2)

    # Add value labels
    for bar, tax in zip(bars, avg_taxes):
        height = bar.get_height()
        ax.annotate(f'${tax:,.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=12, fontweight='bold')

    # Styling
    ax.set_ylabel('Average Annual Property Tax ($)', fontsize=12)
    ax.set_xlabel('Property Value Range', fontsize=12)
    ax.set_title('Cleveland Heights Annual Property Taxes by Value Range', fontsize=14, fontweight='bold')
    ax.set_ylim(0, max(avg_taxes) * 1.2)

    # Format y-axis as currency
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))

    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')

    if show:
        plt.show()

    plt.close()
    return output_path


def plot_annual_taxes_by_year_built(
    properties: List[Property],
    output_path: str = "annual_taxes_by_year.png",
    show: bool = False,
) -> str:
    """
    Create bar chart of average annual property taxes by decade built.

    Args:
        properties: List of Property objects
        output_path: Path to save the chart
        show: Whether to display the chart

    Returns:
        Path to saved chart
    """
    # Group by decade
    decade_taxes: Dict[str, List[float]] = defaultdict(list)

    for prop in properties:
        if prop.annual_taxes and prop.year_built:
            decade = (prop.year_built // 10) * 10
            label = f"{decade}s"
            decade_taxes[label].append(prop.annual_taxes)

    # Sort by decade
    sorted_decades = sorted(decade_taxes.keys())

    categories = []
    avg_taxes = []

    for decade in sorted_decades:
        taxes = decade_taxes[decade]
        categories.append(f"{decade}\n(n={len(taxes)})")
        avg_taxes.append(sum(taxes) / len(taxes))

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))

    # Create gradient colors
    colors = plt.cm.Greens([(i + 3) / (len(categories) + 3) for i in range(len(categories))])
    bars = ax.bar(categories, avg_taxes, color=colors, edgecolor='black', linewidth=1.2)

    # Add value labels
    for bar, tax in zip(bars, avg_taxes):
        height = bar.get_height()
        ax.annotate(f'${tax:,.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=11, fontweight='bold')

    # Styling
    ax.set_ylabel('Average Annual Property Tax ($)', fontsize=12)
    ax.set_xlabel('Decade Built', fontsize=12)
    ax.set_title('Cleveland Heights Annual Property Taxes by Decade Built', fontsize=14, fontweight='bold')
    ax.set_ylim(0, max(avg_taxes) * 1.2)

    # Format y-axis as currency
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))

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
    Create comprehensive multi-panel annual property tax analysis.

    Args:
        properties: List of Property objects
        output_path: Path to save the chart
        show: Whether to display the chart

    Returns:
        Path to saved chart
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Cleveland Heights Annual Property Tax Analysis', fontsize=16, fontweight='bold', y=1.02)

    # Panel 1: Annual taxes by property class
    ax1 = axes[0, 0]
    class_taxes = defaultdict(list)
    for prop in properties:
        if prop.annual_taxes and prop.property_class:
            class_taxes[prop.property_class].append(prop.annual_taxes)

    class_labels = {"R": "Residential", "C": "Commercial", "M": "Multi-Family"}
    cats1 = [class_labels.get(k, k) for k in sorted(class_taxes.keys())]
    vals1 = [sum(v)/len(v) for k, v in sorted(class_taxes.items())]

    bars1 = ax1.bar(cats1, vals1, color=['#2ecc71', '#3498db', '#9b59b6'][:len(cats1)], edgecolor='black')
    ax1.set_ylabel('Avg Annual Tax ($)')
    ax1.set_title('By Property Class')
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    for bar, val in zip(bars1, vals1):
        ax1.annotate(f'${val:,.0f}', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 3), textcoords="offset points", ha='center', fontsize=10, fontweight='bold')
    ax1.yaxis.grid(True, linestyle='--', alpha=0.5)

    # Panel 2: Annual taxes by value range
    ax2 = axes[0, 1]
    ranges = [(0, 200000, "<$200K"), (200000, 400000, "$200-400K"), (400000, float('inf'), ">$400K")]
    range_taxes = defaultdict(list)
    for prop in properties:
        if prop.annual_taxes and prop.market_value_total:
            for low, high, lbl in ranges:
                if low <= prop.market_value_total < high:
                    range_taxes[lbl].append(prop.annual_taxes)
                    break

    cats2 = [lbl for _, _, lbl in ranges if lbl in range_taxes]
    vals2 = [sum(range_taxes[lbl])/len(range_taxes[lbl]) for lbl in cats2]

    bars2 = ax2.bar(cats2, vals2, color=plt.cm.Blues([0.4, 0.6, 0.8])[:len(cats2)], edgecolor='black')
    ax2.set_ylabel('Avg Annual Tax ($)')
    ax2.set_title('By Property Value')
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    for bar, val in zip(bars2, vals2):
        ax2.annotate(f'${val:,.0f}', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 3), textcoords="offset points", ha='center', fontsize=10, fontweight='bold')
    ax2.yaxis.grid(True, linestyle='--', alpha=0.5)

    # Panel 3: Distribution histogram of annual taxes
    ax3 = axes[1, 0]
    all_taxes = [p.annual_taxes for p in properties if p.annual_taxes]

    ax3.hist(all_taxes, bins=20, color='#e74c3c', edgecolor='black', alpha=0.7)
    mean_tax = sum(all_taxes)/len(all_taxes)
    ax3.axvline(mean_tax, color='black', linestyle='--', linewidth=2, label=f'Mean: ${mean_tax:,.0f}')
    ax3.set_xlabel('Annual Property Tax ($)')
    ax3.set_ylabel('Number of Properties')
    ax3.set_title('Tax Distribution')
    ax3.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    ax3.legend()
    ax3.yaxis.grid(True, linestyle='--', alpha=0.5)

    # Panel 4: Summary statistics table
    ax4 = axes[1, 1]
    ax4.axis('off')

    # Calculate statistics
    total_props = len(properties)
    props_with_tax = len([p for p in properties if p.annual_taxes])
    avg_tax = sum(all_taxes) / len(all_taxes) if all_taxes else 0
    min_tax = min(all_taxes) if all_taxes else 0
    max_tax = max(all_taxes) if all_taxes else 0
    median_tax = sorted(all_taxes)[len(all_taxes)//2] if all_taxes else 0
    avg_value = sum(p.market_value_total for p in properties if p.market_value_total) / total_props

    stats_text = f"""
    Cleveland Heights Property Tax Summary
    {'='*45}

    Total Properties:           {total_props:,}

    Average Market Value:       ${avg_value:,.0f}

    Average Annual Tax:         ${avg_tax:,.0f}
    Median Annual Tax:          ${median_tax:,.0f}
    Minimum Annual Tax:         ${min_tax:,.0f}
    Maximum Annual Tax:         ${max_tax:,.0f}

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
    path1 = plot_annual_taxes_by_property_class(
        properties,
        str(output_dir / "annual_taxes_by_class.png"),
        show=show,
    )
    generated_files.append(path1)
    print(f"  Created: {path1}")

    path2 = plot_annual_taxes_by_value_range(
        properties,
        str(output_dir / "annual_taxes_by_value.png"),
        show=show,
    )
    generated_files.append(path2)
    print(f"  Created: {path2}")

    path3 = plot_annual_taxes_by_year_built(
        properties,
        str(output_dir / "annual_taxes_by_year.png"),
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
