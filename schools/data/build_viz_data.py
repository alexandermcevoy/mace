"""Build schools/data/viz.json for the OpenHeights charts page.

Every hand-entered series below is copied from a verified table on the
corresponding guide page (noted in `page`). The scatter plot is built from the
statewide residual file produced for the adjusted-outcomes page (DEW 2025-26
report card data + Census SAIPE 2024 child poverty); pass its path as argv[1].
Usage: python3 -I build_viz_data.py residuals_2025-26.csv
"""
import csv, json, sys, os

def ols(xs, ys):
    n = len(xs); mx = sum(xs)/n; my = sum(ys)/n
    b = sum((x-mx)*(y-my) for x, y in zip(xs, ys)) / sum((x-mx)**2 for x in xs)
    a = my - b*mx
    ss_res = sum((y-(a+b*x))**2 for x, y in zip(xs, ys)); ss_tot = sum((y-my)**2 for y in ys)
    return a, b, 1-ss_res/ss_tot

V = {}

# ---- Money --------------------------------------------------------------
V["forecast"] = {"page": "levy-2026", "unit": "$M", "x": ["FY27", "FY28", "FY29", "FY30"],
  "series": [
    {"name": "August 2026 forecast (no levy)", "values": [32.19, 24.81, 13.10, -3.72]},
    {"name": "February 2026 forecast (before cuts)", "values": [23.70, 7.25, -13.56, None]},
    {"name": "With Issue 4 (OpenHeights illustration)", "values": [37.7, 41.5, 40.9, 35.1]}]}

V["millage"] = {"page": "revenue-and-taxes", "unit": "mills", "x": ["TY2021", "TY2022", "TY2023", "TY2024"],
  "series": [
    {"name": "Voted operating mills", "values": [149.5, 149.5, 149.5, 149.5]},
    {"name": "Effective mills on homes (Class I)", "values": [69.96, 69.88, 70.02, 51.05]}]}

V["revmix"] = {"page": "revenue-and-taxes", "unit": "%", "categories": ["Local taxes", "Other local", "State", "Federal"],
  "rows": [
    {"name": "CH-UH", "values": [65.7, 7.5, 18.3, 8.5]},
    {"name": "Ohio average", "values": [46.8, 7.9, 37.0, 8.3]}]}

V["taxpeers"] = {"page": "revenue-and-taxes", "unit": "mills", "highlight": "CH-UH",
  "refs": [{"name": "Ohio average", "value": 27.75}, {"name": "Median Ohio district", "value": 22.86}],
  "rows": [["CH-UH", 51.05], ["Shaker Heights", 63.62], ["Garfield Heights", 46.50], ["South Euclid-Lyndhurst", 43.93],
           ["Maple Heights", 41.20], ["Euclid", 35.41], ["Cleveland Metropolitan", 34.39], ["Rocky River", 30.12],
           ["Lakewood", 29.62], ["Beachwood", 29.44], ["Bedford", 28.81], ["Berea", 27.35]]}

V["levyhistory"] = {"page": "levy-2026", "unit": "% yes",
  "rows": [["Nov 2011 · 6.9 mills", 57.1, "Passed"], ["Nov 2013 · bond", 59.3, "Passed"], ["May 2015 · 5.9 mills", 43.30, "Failed"],
           ["Nov 2016 · 5.5 mills", 53.9, "Passed"], ["Apr 2020 · 7.9 mills", 47.3, "Failed"], ["Nov 2020 · 4.8 mills", 50.2, "Passed"]]}
# Nov 2020: 15,061 / (15,061 + 14,926) = 50.22%

# ---- Spending -----------------------------------------------------------
V["spending"] = {"page": "spending-and-staffing", "unit": "$",
  "x": ["FY14", "FY16", "FY18", "FY20", "FY21", "FY22", "FY23", "FY24"],
  "series": [
    {"name": "CH-UH", "values": [17748, 21346, 21783, 21719, 23440, 22217, 24221, 25025]},
    {"name": "Ohio", "values": [11349, 12102, 13027, 13805, 14613, 15583, 16476, 17257]}]}

base = {"ADM": 5221, "Total": 890, "Instruction": 480, "Pupil support": 130}
staff = {"ADM": [5221, 5029, 4767, 4649], "Total": [890, 923, 910, 956],
         "Instruction": [480, 440, 432, 413], "Pupil support": [130, 157, 186, 222]}
V["staffing"] = {"page": "spending-and-staffing", "unit": "index", "x": ["FY16", "FY19", "FY22", "FY25"],
  "raw": staff,
  "series": [
    {"name": "Enrollment (ADM)", "values": [round(v/base["ADM"]*100, 1) for v in staff["ADM"]]},
    {"name": "All full-time employees", "values": [round(v/base["Total"]*100, 1) for v in staff["Total"]]},
    {"name": "Instruction staff", "values": [round(v/base["Instruction"]*100, 1) for v in staff["Instruction"]]},
    {"name": "Pupil-support staff", "values": [round(v/base["Pupil support"]*100, 1) for v in staff["Pupil support"]]}]}

V["teacherpeers"] = {"page": "spending-and-staffing", "unit": "% change, 2015-16 to 2024-25",
  "categories": ["Enrollment", "Teachers (FTE)"],
  "rows": [{"name": "CH-UH", "values": [-6, -21]}, {"name": "Shaker Heights", "values": [-16, -14]},
           {"name": "South Euclid-Lyndhurst", "values": [-9, -9]}, {"name": "Euclid", "values": [-19, -27]},
           {"name": "Lakewood", "values": [-18, -13]}, {"name": "Cleveland Municipal", "values": [-16, -30]}]}

# ---- Enrollment & choice ------------------------------------------------
V["enrollment"] = {"page": "enrollment-and-demographics", "unit": "students",
  "x": ["1999-00","2000-01","2002-03","2004-05","2005-06","2007-08","2009-10","2010-11","2012-13","2014-15","2015-16","2017-18","2019-20","2020-21","2021-22","2022-23","2023-24","2024-25"],
  "series": [{"name": "Enrollment (NCES)", "values": [7451,7311,7044,6494,6376,6257,6056,6032,5845,5572,5349,5217,5169,4936,4967,5010,4916,5019]}]}

pe = [  # year, in CH-UH, OE, other means, online cs, site cs, EdChoice/Cleveland, Expansion, Autism/JP
 ["2018-19",4701,154,62,108,229,882,153,260], ["2019-20",4669,128,90,105,235,1400,148,261],
 ["2020-21",4501,130,83,142,267,1772,144,265], ["2021-22",4438,129,106,112,239,1885,182,267],
 ["2022-23",4488,113,84,115,207,1926,210,278], ["2023-24",4387,130,82,117,199,1816,465,271],
 ["2024-25",4431,122,80,128,182,1730,888,283], ["2025-26",4281,89,72,113,230,1592,1052,294]]
V["residents"] = {"page": "enrollment-and-demographics", "unit": "students",
  "categories": ["Attend CH-UH", "Traditional EdChoice", "EdChoice Expansion", "Autism / Jon Peterson", "Charter schools", "Other public districts"],
  "rows": [{"name": r[0], "values": [r[1], r[6], r[7], r[8], r[4]+r[5], r[2]+r[3]]} for r in pe]}

V["privateshare"] = {"page": "enrollment-and-demographics", "unit": "%", "highlight": "CH-UH",
  "rows": [["CH-UH", 34.3, 3.2, 34.7], ["Euclid", 27.8, 4.8, 22.4], ["South Euclid-Lyndhurst", 25.1, 5.9, 16.8],
           ["Shaker Heights", 21.6, 3.8, 16.5], ["Lakewood", 16.9, 3.7, 20.2]]}
# [district, 2020-24 share, MOE, 2008-12 share]

# ---- Outcomes -----------------------------------------------------------
V["pi"] = {"page": "academic-outcomes", "unit": "PI (0-120)",
  "x": ["05-06","06-07","07-08","08-09","09-10","10-11","11-12","12-13","13-14","14-15","15-16","16-17","17-18","18-19","19-20","20-21","21-22","22-23","23-24","24-25","25-26"],
  "series": [
    {"name": "CH-UH", "values": [90.0,88.7,86.8,86.2,86.9,87.3,87.7,87.2,87.2,82.9,69.6,74.4,75.4,75.2,None,56.3,66.9,70.6,69.2,74.6,79.0]},
    {"name": "Median Ohio district", "values": [None]*15 + [80.7,85.4,87.6,87.4,88.2,88.5]}]}
# 2015-16 to 2017-18 reported as % of 120 (58.0, 62.0, 62.8) -> x1.2. 2019-20: no tests.

V["valueadded"] = {"page": "adjusted-outcomes", "unit": "growth index",
  "rows": [["2021-22", 1.22, None], ["2022-23", -1.10, 44], ["2023-24", -7.06, 14], ["2024-25", -0.68, 48], ["2025-26", 7.68, 87]]}

V["learningrate"] = {"page": "adjusted-outcomes", "unit": "grade levels per year", "highlight": "CH-UH",
  "refs": [{"name": "Typical (1 grade/year)", "value": 1.0}],
  "rows": [["Beachwood",1.15],["Euclid",1.09],["Cleveland Municipal",1.09],["Maple Heights",1.05],["Lakewood",1.02],
           ["Ohio average",0.98],["Richmond Heights",0.98],["Bedford",0.94],["Similar districts (Stanford)",0.92],
           ["Warrensville Heights",0.88],["Shaker Heights",0.86],["Garfield Heights",0.86],["South Euclid-Lyndhurst",0.84],["CH-UH",0.76]]}

V["gaps"] = {"page": "academic-outcomes", "unit": "% proficient, 2025-26",
  "rows": [{"name": "CH-UH · ELA", "black": 47.8, "white": 91.6}, {"name": "Ohio · ELA", "black": 39.2, "white": 69.7},
           {"name": "CH-UH · Math", "black": 38.7, "white": 87.1}, {"name": "Ohio · Math", "black": 30.4, "white": 64.7}]}

V["absent"] = {"page": "academic-outcomes", "unit": "%", "x": ["2021-22","2022-23","2023-24","2024-25","2025-26"],
  "series": [{"name": "CH-UH", "values": [46.3,39.5,37.5,38.2,37.9]}, {"name": "Ohio", "values": [30.2,26.8,25.6,25.1,23.9]}]}


V["simpson"] = {"page": "adjusted-outcomes", "unit": "ESSA Performance Index, 2025-26",
  "rows": [["All students", 78.6, 82.5, 88.0, 17], ["Black", 70.9, 63.0, 74.1, 40], ["Hispanic", 80.7, 70.8, 83.6, 41],
           ["Multiracial", 93.3, 77.8, 83.3, 78], ["White", 107.7, 89.3, 89.5, 97]],
  "cf": 87}
# [group, CH-UH, Ohio average, median district, CH-UH percentile among districts]

# ---- Scatter: PI vs child poverty, all districts -------------------------
pts = []
with open(sys.argv[1], newline="") as f:
    for r in csv.DictReader(f):
        pts.append({"irn": r["irn"], "name": r["name"], "cpov": float(r["cpov"]), "pi": float(r["pi"]),
                    "res": float(r["M4_res"]), "pct": float(r["M4_pct"])})
a, b, r2 = ols([p["cpov"] for p in pts], [p["pi"] for p in pts])
V["scatter"] = {"page": "adjusted-outcomes", "year": "2025-26", "fit": {"a": round(a, 3), "b": round(b, 4), "r2": round(r2, 3)},
  "highlight": "043794",
  "label": {"043794": "CH-UH", "044750": "Shaker Heights", "044198": "Lakewood", "043950": "Euclid", "043786": "Cleveland",
            "043554": "Beachwood", "044792": "South Euclid-Lyndhurst"},
  "points": [[p["irn"], p["name"], p["cpov"], p["pi"]] for p in pts]}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "viz.json")
with open(out, "w") as f:
    json.dump(V, f, separators=(",", ":"))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pi_vs_child_poverty_2025-26.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["irn", "district", "child_poverty_pct_saipe2024", "performance_index_2025_26", "residual_model4", "residual_pct_model4"])
    for p in pts: w.writerow([p["irn"], p["name"], p["cpov"], p["pi"], p["res"], p["pct"]])
print("fit: PI = %.2f + %.3f*cpov, R2=%.3f, n=%d" % (a, b, r2, len(pts)))
