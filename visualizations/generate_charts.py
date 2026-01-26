#!/usr/bin/env python3
"""
Generate visualizations for Cleveland Heights Municipal Policy Data Repository
"""

import matplotlib.pyplot as plt
import pandas as pd
import os

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# Ensure output directory exists
output_dir = '/home/user/mace/visualizations'
os.makedirs(output_dir, exist_ok=True)

# ============================================================
# Chart 1: Population Trends
# ============================================================
print("Generating population trends chart...")

pop_data = pd.read_csv('/home/user/mace/data/demographics/population_trends.csv')

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(pop_data['year'], pop_data['total_population'],
        marker='o', linewidth=2.5, markersize=8, color='#2563eb', label='Total Population')

# Add data labels
for i, row in pop_data.iterrows():
    ax.annotate(f"{row['total_population']:,.0f}",
                xy=(row['year'], row['total_population']),
                xytext=(0, 10), textcoords='offset points',
                ha='center', fontsize=9, color='#374151')

# Highlight Census years
census_years = [2010, 2020]
for year in census_years:
    if year >= 2015:
        row = pop_data[pop_data['year'] == year]
        if not row.empty:
            ax.scatter(year, row['total_population'].values[0],
                      s=150, color='#dc2626', zorder=5, marker='s', label='Census Year' if year == 2020 else '')

ax.set_xlabel('Year')
ax.set_ylabel('Population')
ax.set_title('Cleveland Heights Population Trends (2015-2023)', fontweight='bold', pad=15)
ax.set_ylim(43000, 47000)
ax.set_xlim(2014.5, 2023.5)

# Add trend annotation
ax.annotate('2019: Lowest point\n(43,887)',
            xy=(2019, 43887), xytext=(2017, 44500),
            arrowprops=dict(arrowstyle='->', color='#6b7280'),
            fontsize=10, color='#6b7280')

ax.annotate('2020 Census\ncorrection',
            xy=(2020, 45312), xytext=(2021.5, 46000),
            arrowprops=dict(arrowstyle='->', color='#6b7280'),
            fontsize=10, color='#6b7280')

ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{output_dir}/population_trends.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: population_trends.png")

# ============================================================
# Chart 2: Income Tax Revenue Over Time
# ============================================================
print("Generating income tax revenue chart...")

revenue_data = pd.read_csv('/home/user/mace/data/municipal_finance/revenue.csv')

fig, ax1 = plt.subplots(figsize=(10, 6))

# Bar chart for income tax revenue
colors = ['#93c5fd' if year < 2016 else '#2563eb' for year in revenue_data['year']]
bars = ax1.bar(revenue_data['year'], revenue_data['income_tax_revenue'] / 1_000_000,
               color=colors, edgecolor='#1e40af', linewidth=1.2)

ax1.set_xlabel('Year')
ax1.set_ylabel('Income Tax Revenue (Millions $)', color='#2563eb')
ax1.tick_params(axis='y', labelcolor='#2563eb')
ax1.set_ylim(0, 50)

# Add data labels on bars
for bar, value in zip(bars, revenue_data['income_tax_revenue']):
    height = bar.get_height()
    ax1.annotate(f'${value/1_000_000:.1f}M',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords='offset points',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

# Add tax rate line on secondary axis
ax2 = ax1.twinx()
ax2.plot(revenue_data['year'], revenue_data['income_tax_rate'],
         color='#dc2626', linewidth=2.5, marker='s', markersize=8, label='Tax Rate')
ax2.set_ylabel('Income Tax Rate (%)', color='#dc2626')
ax2.tick_params(axis='y', labelcolor='#dc2626')
ax2.set_ylim(1.5, 2.75)

# Add annotation for tax increase
ax1.axvline(x=2015.5, color='#6b7280', linestyle='--', alpha=0.7)
ax1.annotate('Tax rate increased\n2.00% → 2.25%\n(Nov 2015 voter approval)',
            xy=(2015.5, 42), fontsize=10, ha='center', color='#6b7280',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#d1d5db'))

ax1.set_title('Cleveland Heights Income Tax Revenue (2015-2023)', fontweight='bold', pad=15)

# Create custom legend
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
legend_elements = [
    Patch(facecolor='#93c5fd', edgecolor='#1e40af', label='Revenue @ 2.00% rate'),
    Patch(facecolor='#2563eb', edgecolor='#1e40af', label='Revenue @ 2.25% rate'),
    Line2D([0], [0], color='#dc2626', linewidth=2.5, marker='s', label='Tax Rate')
]
ax1.legend(handles=legend_elements, loc='upper left')

ax1.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{output_dir}/income_tax_revenue.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: income_tax_revenue.png")

# ============================================================
# Chart 3: Working-Age Population as % of Total
# ============================================================
print("Generating working-age population chart...")

fig, ax = plt.subplots(figsize=(10, 6))

# Create stacked area chart
ax.fill_between(pop_data['year'], 0, pop_data['under_15_pct'],
                alpha=0.8, color='#fbbf24', label='Under 15')
ax.fill_between(pop_data['year'], pop_data['under_15_pct'],
                pop_data['under_15_pct'] + pop_data['working_age_pct'],
                alpha=0.8, color='#2563eb', label='Working Age (15-64)')
ax.fill_between(pop_data['year'], pop_data['under_15_pct'] + pop_data['working_age_pct'],
                100, alpha=0.8, color='#6b7280', label='65 and Over')

# Add percentage labels
for year_idx in [0, 4, 8]:  # 2015, 2019, 2023
    row = pop_data.iloc[year_idx]
    year = row['year']

    # Under 15
    ax.annotate(f"{row['under_15_pct']:.1f}%",
                xy=(year, row['under_15_pct']/2),
                ha='center', va='center', fontsize=10, fontweight='bold', color='#78350f')

    # Working age
    mid_working = row['under_15_pct'] + row['working_age_pct']/2
    ax.annotate(f"{row['working_age_pct']:.1f}%",
                xy=(year, mid_working),
                ha='center', va='center', fontsize=11, fontweight='bold', color='white')

    # 65+
    ax.annotate(f"{row['age_65_plus_pct']:.1f}%",
                xy=(year, row['under_15_pct'] + row['working_age_pct'] + row['age_65_plus_pct']/2),
                ha='center', va='center', fontsize=10, fontweight='bold', color='white')

ax.set_xlabel('Year')
ax.set_ylabel('Percentage of Population')
ax.set_title('Cleveland Heights Age Distribution (2015-2023)\nWorking-Age Population Stability',
             fontweight='bold', pad=15)
ax.set_ylim(0, 100)
ax.set_xlim(2015, 2023)

ax.legend(loc='upper right', bbox_to_anchor=(1.0, 0.98))

# Add annotation
ax.annotate('Working-age population\nremains stable at ~65%',
            xy=(2019, 50), fontsize=11, ha='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#d1d5db', alpha=0.9))

plt.tight_layout()
plt.savefig(f'{output_dir}/working_age_population.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: working_age_population.png")

# ============================================================
# Bonus: Summary Dashboard
# ============================================================
print("Generating summary dashboard...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Cleveland Heights Municipal Data Dashboard (2015-2023)',
             fontsize=16, fontweight='bold', y=1.02)

# 1. Population (top left)
ax1 = axes[0, 0]
ax1.plot(pop_data['year'], pop_data['total_population'],
        marker='o', linewidth=2, markersize=6, color='#2563eb')
ax1.fill_between(pop_data['year'], pop_data['total_population'], alpha=0.3, color='#2563eb')
ax1.set_title('Total Population', fontweight='bold')
ax1.set_ylabel('Population')
ax1.set_ylim(43000, 47000)
ax1.grid(True, alpha=0.3)

# 2. Income Tax Revenue (top right)
ax2 = axes[0, 1]
ax2.bar(revenue_data['year'], revenue_data['income_tax_revenue'] / 1_000_000,
        color='#10b981', edgecolor='#047857')
ax2.set_title('Income Tax Revenue', fontweight='bold')
ax2.set_ylabel('Revenue ($ Millions)')
ax2.grid(True, alpha=0.3, axis='y')

# 3. Median Household Income (bottom left)
income_data = pd.read_csv('/home/user/mace/data/economics/income_poverty.csv')
ax3 = axes[1, 0]
ax3.plot(income_data['year'], income_data['median_household_income'] / 1000,
        marker='o', linewidth=2, markersize=6, color='#8b5cf6')
ax3.fill_between(income_data['year'], income_data['median_household_income'] / 1000, alpha=0.3, color='#8b5cf6')
ax3.set_title('Median Household Income', fontweight='bold')
ax3.set_ylabel('Income ($ Thousands)')
ax3.set_xlabel('Year')
ax3.grid(True, alpha=0.3)

# 4. School Enrollment (bottom right)
school_data = pd.read_csv('/home/user/mace/data/education/school_enrollment.csv')
ax4 = axes[1, 1]
ax4.bar(school_data['year'], school_data['total_enrollment'],
        color='#f59e0b', edgecolor='#d97706')
ax4.set_title('School District Enrollment', fontweight='bold')
ax4.set_ylabel('Students')
ax4.set_xlabel('Year')
ax4.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{output_dir}/summary_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: summary_dashboard.png")

print("\nAll visualizations generated successfully!")
print(f"Output directory: {output_dir}")
