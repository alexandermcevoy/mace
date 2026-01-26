"""
Sample data generator for Cleveland Heights properties.

Generates realistic sample data when live data cannot be fetched.
Based on actual Cleveland Heights property characteristics:
- Mix of historic (1900s-1930s), mid-century, and newer homes
- Property values ranging from ~$80K to $800K+
- Effective tax rate around 2.5-2.8% of market value
- Ohio assesses at 35% of market value
"""

import random
from typing import List, Dict

# Street names in Cleveland Heights
STREETS = [
    "Overlook Rd", "Fairmount Blvd", "Coventry Rd", "Lee Rd", "Cedar Rd",
    "Mayfield Rd", "Noble Rd", "Warrensville Center Rd", "Taylor Rd",
    "Euclid Heights Blvd", "Derbyshire Rd", "Kenilworth Rd", "Queenston Rd",
    "Yorkshire Rd", "Berkshire Rd", "Hampshire Rd", "Lancashire Rd",
    "Meadowbrook Blvd", "Monticello Blvd", "Washington Blvd", "Lincoln Blvd",
    "Yellowstone Rd", "Tullamore Rd", "Scarborough Rd", "Lamberton Rd",
    "Lennox Rd", "Corydon Rd", "Edgehill Rd", "Woodview Rd", "Glenmont Rd",
    "Superior Rd", "Compton Rd", "Bellfield Ave", "Rydalmount Rd",
]

# Cleveland Heights neighborhoods/areas with typical characteristics
NEIGHBORHOODS = {
    "Cedar Fairmount": {"value_range": (250000, 600000), "year_range": (1910, 1940), "weight": 0.15},
    "Coventry": {"value_range": (150000, 400000), "year_range": (1915, 1945), "weight": 0.12},
    "Cedar Lee": {"value_range": (180000, 450000), "year_range": (1920, 1950), "weight": 0.12},
    "Noble": {"value_range": (100000, 280000), "year_range": (1940, 1970), "weight": 0.15},
    "Forest Hill": {"value_range": (300000, 850000), "year_range": (1920, 1940), "weight": 0.10},
    "Severance": {"value_range": (120000, 320000), "year_range": (1945, 1975), "weight": 0.15},
    "Caledonia": {"value_range": (90000, 220000), "year_range": (1950, 1980), "weight": 0.12},
    "Millikin": {"value_range": (140000, 350000), "year_range": (1925, 1955), "weight": 0.09},
}


def generate_sample_properties(count: int = 200) -> List[Dict]:
    """
    Generate realistic sample Cleveland Heights property data.

    Args:
        count: Number of properties to generate

    Returns:
        List of property dictionaries
    """
    random.seed(42)  # For reproducibility
    properties = []

    # Tax districts for Cleveland Heights
    tax_districts = ["561", "562", "563", "564", "565"]

    # Property class distribution (roughly matches reality)
    # Cleveland Heights is primarily residential
    class_weights = [
        ("R", 0.82),   # Residential - 82%
        ("M", 0.12),   # Multi-family - 12%
        ("C", 0.06),   # Commercial - 6%
    ]

    for i in range(count):
        # Select neighborhood based on weights
        neighborhoods = list(NEIGHBORHOODS.keys())
        weights = [NEIGHBORHOODS[n]["weight"] for n in neighborhoods]
        neighborhood = random.choices(neighborhoods, weights=weights)[0]
        hood_data = NEIGHBORHOODS[neighborhood]

        # Select property class
        prop_class = random.choices(
            [c[0] for c in class_weights],
            weights=[c[1] for c in class_weights]
        )[0]

        # Adjust values for commercial/multi-family
        value_low, value_high = hood_data["value_range"]
        if prop_class == "C":
            value_low *= 2
            value_high *= 3
        elif prop_class == "M":
            value_low *= 1.5
            value_high *= 2

        # Generate property characteristics
        year_built = random.randint(*hood_data["year_range"])

        # Market value with some variation
        base_value = random.randint(int(value_low), int(value_high))
        # Older homes in good areas tend to be worth more
        if year_built < 1930 and value_high > 300000:
            base_value = int(base_value * random.uniform(1.0, 1.3))
        market_value = round(base_value, -3)  # Round to nearest $1000

        # Ohio assesses at 35% of market value
        assessed_value = round(market_value * 0.35, -2)

        # Cleveland Heights effective tax rate is approximately 2.52% of market value
        # This translates to about 7.2% of assessed value (millage rate ~72 mills)
        # Add some variation
        effective_rate = random.uniform(0.024, 0.028)
        annual_taxes = round(market_value * effective_rate, 2)

        # Living area based on property type and value
        if prop_class == "R":
            sqft_per_dollar = random.uniform(0.006, 0.010)
            living_area = int(market_value * sqft_per_dollar)
            living_area = max(800, min(5000, living_area))
        elif prop_class == "M":
            living_area = random.randint(3000, 12000)
        else:  # Commercial
            living_area = random.randint(2000, 20000)

        # Generate address
        house_num = random.randint(1000, 4999)
        street = random.choice(STREETS)

        # Generate parcel ID
        district = random.choice(tax_districts)
        section = f"{random.randint(1, 20):02d}"
        parcel = f"{random.randint(1, 999):03d}"
        parcel_id = f"{district}-{section}-{parcel}"

        properties.append({
            "parcel_id": parcel_id,
            "address": f"{house_num} {street}",
            "neighborhood": neighborhood,
            "year_built": year_built,
            "market_value_total": market_value,
            "assessed_value": assessed_value,
            "annual_taxes": annual_taxes,
            "property_class": prop_class,
            "living_area_sqft": living_area,
        })

    return properties


# Pre-generated sample data for consistent results
SAMPLE_PROPERTIES = generate_sample_properties(200)
