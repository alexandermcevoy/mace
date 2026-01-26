# Cleveland Heights Municipal Policy Data Repository

A comprehensive data repository for analyzing Cleveland Heights, Ohio municipal policy trends (2015-2023).

## Overview

This repository contains structured datasets supporting a monthly column series on Cleveland Heights municipal policy. It includes demographic, economic, housing, municipal finance, and education data from authoritative sources.

## Repository Structure

```
mace/
├── data/
│   ├── demographics/
│   │   ├── population_trends.csv      # Annual population & age structure
│   │   ├── racial_composition.csv     # Racial/ethnic breakdown by year
│   │   └── age_distribution.csv       # Detailed age cohorts
│   ├── economics/
│   │   ├── income_poverty.csv         # Median income, poverty rates
│   │   └── income_distribution.csv    # Income bracket distribution
│   ├── housing/
│   │   ├── housing_units.csv          # Units, vacancy, tenure
│   │   └── home_values.csv            # Median values, sales data
│   ├── municipal_finance/
│   │   ├── revenue.csv                # General fund revenue sources
│   │   └── expenditures.csv           # Expenditure by department
│   └── education/
│       ├── school_enrollment.csv      # CH-UH district enrollment
│       └── school_demographics.csv    # Student demographics
├── visualizations/
│   ├── population_trends.png          # Population line chart
│   ├── income_tax_revenue.png         # Tax revenue bar chart
│   ├── working_age_population.png     # Age distribution area chart
│   ├── summary_dashboard.png          # 4-panel overview
│   └── generate_charts.py             # Visualization script
└── documentation/
    └── MASTER_SUMMARY.md              # Comprehensive analysis document
```

## Key Data Points (2015-2023)

| Metric | 2015 | 2023 | Change |
|--------|------|------|--------|
| Population | 45,500 | 44,694 | -1.8% |
| Median Household Income | $52,853 | $72,302 | +36.8% |
| Poverty Rate | 15.8% | 14.7% | -1.1 pp |
| Median Home Value | $128,500 | $188,471 | +46.7% |
| Income Tax Revenue | $32.5M | $45.8M | +40.9% |
| School Enrollment | 5,450 | 5,010 | -8.1% |

## Data Sources

- **U.S. Census Bureau** - Decennial Census, American Community Survey
- **Cleveland Heights City Government** - ACFRs, Budget Documents
- **Ohio Auditor of State** - Municipal audit reports
- **Ohio Department of Education** - School enrollment data
- **NCES** - National education statistics
- **RITA** - Regional Income Tax Agency

## Usage

### View Visualizations
Pre-generated charts are in the `visualizations/` directory.

### Regenerate Charts
```bash
python3 visualizations/generate_charts.py
```

### Data Analysis
All CSV files are in standard format with headers. Import into Excel, Python/pandas, R, or any data tool.

## Data Quality Notes

- **High confidence:** Census counts, ACS estimates, official tax rates
- **Moderate confidence:** Year-to-year interpolations, financial estimates
- **Recommended verification:** Municipal finance figures against official ACFRs

## Contributing

To add or update data:
1. Use consistent CSV formatting
2. Include source column in data files
3. Update MASTER_SUMMARY.md with changes
4. Regenerate visualizations if data changes

## License

Data compiled from public sources for journalistic/educational purposes.

## Contact

This repository supports a monthly column series on Cleveland Heights municipal policy.
