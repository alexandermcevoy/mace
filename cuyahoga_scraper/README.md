# Cuyahoga County Property Scraper

A Python tool for pulling property data from Cuyahoga County's public property lookup systems, specifically designed for Cleveland Heights, Ohio properties.

## Overview

This scraper uses the Cuyahoga County ArcGIS REST API to retrieve parcel and property information. The tool provides:

- Bulk retrieval of Cleveland Heights properties
- Search by address, parcel ID, or owner name
- Property filtering by class, value, year built
- Export to CSV, JSON, JSON Lines, and GeoJSON formats
- Rate limiting and retry logic for reliable data retrieval

## Data Source

The scraper accesses the following Cuyahoga County GIS services:

- **MyPlace Portal**: https://myplace.cuyahogacounty.gov/
- **Fiscal GIS Hub**: https://fiscalhub.gis.cuyahogacounty.gov/
- **ArcGIS REST Services**: https://gis.cuyahogacounty.us/server/rest/services/

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

### Command Line Interface

```bash
# Get all Cleveland Heights properties
python -m cuyahoga_scraper fetch --output properties.csv

# Get residential properties only
python -m cuyahoga_scraper fetch --property-class R --output residential.csv

# Get properties with value filters
python -m cuyahoga_scraper fetch --min-value 100000 --max-value 500000 --output mid_range.csv

# Filter by year built
python -m cuyahoga_scraper fetch --year-min 1900 --year-max 1950 --output historic.csv

# Limit results
python -m cuyahoga_scraper fetch --limit 100 --output sample.csv

# Export to different formats
python -m cuyahoga_scraper fetch --format json --output properties.json
python -m cuyahoga_scraper fetch --format geojson --output properties.geojson

# Search by address
python -m cuyahoga_scraper search --address "123 Main St"

# Search by parcel ID
python -m cuyahoga_scraper search --parcel "561-01-001"

# Search by owner name
python -m cuyahoga_scraper search --owner "Smith"

# Get service information
python -m cuyahoga_scraper info --fields

# Get property count
python -m cuyahoga_scraper count
```

### Python API

```python
from cuyahoga_scraper import CuyahogaPropertyScraper
from cuyahoga_scraper.export import PropertyExporter

# Initialize scraper
scraper = CuyahogaPropertyScraper()

# Get Cleveland Heights properties
result = scraper.get_cleveland_heights_properties(
    limit=1000,
    property_class="R",  # Residential
    min_value=150000,
)

print(f"Found {result.total_count} properties")

# Export to CSV
PropertyExporter.to_csv(result.properties, "output.csv")

# Search by address
result = scraper.search_by_address("2345 Overlook Rd")
for prop in result.properties:
    print(f"{prop.address}: ${prop.market_value_total:,.0f}")

# Search by parcel ID
result = scraper.search_by_parcel_id("561-12-345")

# Search by owner
result = scraper.search_by_owner("Johnson")

# Iterate through all properties (memory efficient)
for prop in scraper.iter_all_cleveland_heights():
    print(prop.parcel_id, prop.address)

# Clean up
scraper.close()

# Or use context manager
with CuyahogaPropertyScraper() as scraper:
    result = scraper.get_cleveland_heights_properties()
```

## Property Data Fields

The scraper retrieves the following property information when available:

| Field | Description |
|-------|-------------|
| `parcel_id` | Unique parcel identification number |
| `address` | Property street address |
| `city` | Municipality (Cleveland Heights) |
| `zip_code` | ZIP code |
| `owner_name` | Current owner name |
| `property_class` | Property classification code |
| `land_use` | Land use code |
| `year_built` | Year structure was built |
| `bedrooms` | Number of bedrooms |
| `bathrooms` | Number of bathrooms |
| `living_area_sqft` | Living area in square feet |
| `lot_size_sqft` | Lot size in square feet |
| `market_value_land` | Market value of land |
| `market_value_building` | Market value of building/improvements |
| `market_value_total` | Total market value |
| `assessed_value` | Assessed value for taxation |
| `annual_taxes` | Annual property taxes |
| `last_sale_date` | Date of last sale |
| `last_sale_price` | Price of last sale |
| `latitude` | Geographic latitude |
| `longitude` | Geographic longitude |

## Cleveland Heights Information

Cleveland Heights is a city in Cuyahoga County, Ohio with:
- Population: ~44,000
- Incorporated: 1921
- Tax districts: 561-565 (typically)

The scraper filters properties using multiple strategies:
1. City/Municipality field matching
2. Tax district codes in parcel IDs

## Export Formats

### CSV
Standard comma-separated values with header row. Best for spreadsheet analysis.

### JSON
Full JSON export with metadata. Best for web applications.

### JSON Lines (JSONL)
One JSON object per line. Best for streaming/processing large datasets.

### GeoJSON
Geographic JSON format with point coordinates. Best for mapping applications.

## Rate Limiting

The scraper includes built-in rate limiting (default 0.5s between requests) to be respectful to the county's servers. You can adjust this:

```python
scraper = CuyahogaPropertyScraper(rate_limit_delay=1.0)  # 1 second delay
```

## Error Handling

The scraper includes retry logic with exponential backoff for transient failures:

```python
scraper = CuyahogaPropertyScraper(
    timeout=60,      # Request timeout in seconds
    max_retries=5,   # Maximum retry attempts
)
```

## Legal Notice

This tool accesses publicly available property records from Cuyahoga County. Please:
- Use the data responsibly
- Respect rate limits
- Review Cuyahoga County's terms of use
- Do not use for harassment or illegal purposes

## Additional Resources

- [Cuyahoga County Fiscal Office](https://cuyahogacounty.gov/fiscal-officer)
- [MyPlace Property Search](https://myplace.cuyahogacounty.gov/)
- [Cuyahoga County Open Data](https://data-cuyahoga.opendata.arcgis.com/)
- [CuyahogaGIS Hub](https://geospatial.gis.cuyahogacounty.gov/)
