---
layout: default
title: "Outcomes Adjusted for Who the District Serves"
---

# Outcomes Adjusted for Who the District Serves

[← Back to the CH-UH schools guide](./)

*Research status as of October 12, 2026. This page answers a narrower question than a raw report card: **given the students Cleveland Heights-University Heights City Schools (CH-UH) serves, how much are they learning, and is that improving?** It combines Ohio's own data files, an OpenHeights regression across all 607 Ohio districts, and the Stanford/Harvard reports. Every figure carries a source and a data year. Calculations by OpenHeights are labeled as such.*

> **Verification status: checked against primary sources on Oct. 12, 2026**, except items listed under [Gaps / unverified](#gaps--unverified). State figures come from the Ohio Department of Education and Workforce (DEW) report-card data files. Stanford/Harvard figures were read from the report PDFs themselves. The regression results are OpenHeights calculations; the method is described in full in section 4, and the corrections are listed in the [Corrections log](#corrections-log).

## Key facts / bottom line

- **Raw achievement is low, which mostly reflects who the district serves.** CH-UH's 2025–26 Performance Index (PI) was **79.0**, against **82.8** for Ohio as a whole. Its PI ranked **72nd of 77** districts in its state typology group [9][11][12]. Nationally, Stanford places CH-UH's 2022–25 grade 3–8 scores at about the **11th percentile in math** and **22nd in reading** [1].
- **Adjusted for poverty, CH-UH is roughly where it is predicted to be, and it has moved up since 2023–24.** In an OpenHeights regression across all 607 Ohio districts, CH-UH's 2025–26 PI was **0.7 points above** what its economically disadvantaged share predicts (53rd percentile of residuals). With census child poverty and special-education and English-learner shares as controls, it was **1.1 points above** (55th percentile), up from 7.1 points *below* prediction in 2023–24. On the poverty-flag model, CH-UH has stayed within about 4 points of prediction in every year since 2022–23. **The result depends on the model.** When race is also controlled for, CH-UH ranks near the top of the state (98th percentile). See section 4.
- **Ohio's growth measure is strong this year, weaker before.** District Progress (value-added) was **3 stars (2021–22), 3 (2022–23), 2 (2023–24), 3 (2024–25) and 4 (2025–26)** [11]. The 2025–26 Value-Added Growth Index of **+7.68** ranked at the **87th percentile** of Ohio districts. A year earlier it was −0.68, at the 48th percentile (OpenHeights calculation from [11]).
- **Stanford's learning-rate measure points the other way.** Stanford's 2025 report says CH-UH students gained **0.76 grade levels per year** in grades 3–8 during 2022–25. That is the **14th percentile** nationally, below the **0.92** average of Stanford's "similar districts" and the **0.98** Ohio average [1]. It was the lowest of the 12 Cuyahoga County districts compared below. Stanford calls learning rates "a better indicator of school quality than average test scores" [1].
- **Recovery since 2022 is strong by national standards.** Stanford ranks CH-UH's 2022–25 *trend* at the **96th percentile in math** and **70th in reading** [1]. The Education Scorecard lists CH-UH among Ohio's reading "Districts on the Rise" for 2024–25 [3][4].
- **Honest assessment.** On Ohio's measures, CH-UH performs about as expected for its students on achievement, with a clear improvement in the last two years. Its 2025–26 value-added was well above average. On Stanford's measure of within-year learning in grades 3–8 it lags similar districts. All the adjusted measures carry real caveats, especially about how poverty is measured and which students leave for private schools (section 7).

## Why adjustment matters

Raw test scores mostly measure who attends a school. In the OpenHeights regression, the share of economically disadvantaged students alone explains **53–72%** of the variation in Performance Index across Ohio districts, depending on the year (R², section 4). Adjusted measures try to separate the school's contribution from the starting point students bring:

| Measure | What it captures | How much it depends on family background |
|---|---|---|
| Average score level (Ohio Performance Index; SEDA average scores) | Where students are | High |
| Change over time (Education Scorecard; SEDA trend) | Whether a district is improving relative to its own past | Lower, but can reflect changes in who enrolls |
| Learning rate (SEDA grade 3→8 slope) | How much students gain per grade | Lower; Stanford presents it as closer to school contribution |
| Value-added (Ohio Progress, EVAAS) | Student growth compared with growth predicted from each student's own prior scores | Lowest of these, but still imperfect |
| Regression residuals / "similar districts" | Performance compared with districts that have similar demographics | Depends on which variables are controlled |

No single measure is clean. That is why this page puts several side by side.

## 1. Stanford Educational Opportunity Project (SEDA) and the Education Scorecard

**Identifiers.** NCES LEA ID **3904379**; Ohio IRN **043794** [1][11].

### 1a. Pandemic loss and recovery (Education Recovery Scorecard, 2024 release)

Grade 3–8 averages, in grade levels relative to the **2019 national average** (0 = national average in 2019). Figures as printed in the report [2]:

| Subject | 2019 | 2022 | 2023 | Change 2019→22 | Change 2022→23 | Net 2019→23 |
|---|---|---|---|---|---|---|
| Math, CH-UH | −1.03 | −2.62 | −1.92 | −1.59 | +0.69 | −0.89 |
| Reading, CH-UH | −0.57 | −1.15 | −0.95 | −0.58 | +0.20 | −0.38 |
| Math, Black students in CH-UH | −1.77 | −3.14 | −2.48 | −1.37 | +0.66 | −0.71 |
| Reading, Black students in CH-UH | −1.41 | −1.94 | −1.80 | −0.52 | +0.13 | −0.39 |

For comparison, the same report gives these changes in grade levels [2]:

- **Ohio:** math −0.49 (2019→22) and +0.30 (2022→23); reading −0.35 and +0.29.
- **Similar districts** (Princeton City, Winton Woods City, Mt. Healthy City, South Euclid-Lyndhurst City and Bedford City): math −0.90 and +0.38; reading −0.36 and +0.14.

CH-UH's 2019–22 math drop was about three times Ohio's. Its one-year rebound was also larger.

*Conflict resolved:* the −2.48 (math) and −1.80 (reading) 2023 values that appeared in an earlier search excerpt are the report's figures for **Black students**, not for all students [2].

### 1b. 2025 trends report (SEDA, school years 2022–25)

From Stanford's report, version 2025.1, generated April 28, 2026 [1]. Scores are math and reading combined, in grade levels relative to the 2019 national average. Trends are in grade levels per year.

| Group | Average score 2022–25 | Trend 2022–25 |
|---|---|---|
| CH-UH, all students | **−1.66** | **+0.05/yr** |
| Similar districts average* | −2.30 | −0.04/yr |
| Ohio | −0.14 | −0.01/yr |
| CH-UH White students | +2.33 | +0.20/yr |
| CH-UH Black students | −2.44 | 0.00/yr |
| CH-UH "poor" students | −1.66 | +0.05/yr |
| CH-UH female / male | −1.51 / −1.81 | −0.01 / +0.10/yr |

\*In the 2025 report, Stanford's similar districts are South Euclid-Lyndhurst, Mt. Healthy, Winton Woods, North College Hill and Bedford [1]. The "poor" row is identical to the all-students row because Ohio data flag essentially every CH-UH student as economically disadvantaged (section 4).

**National rankings, 2022–25** [1]:

| | CH-UH average | CH-UH trend | Similar-district average | Similar-district trend |
|---|---|---|---|---|
| Math | 9,056 / 10,205 (**11th pct**) | 201 / 5,468 (**96th pct**) | 9,677 / 10,205 (5th pct) | 601 / 5,468 (89th pct) |
| Reading | 7,822 / 10,076 (**22nd pct**) | 1,695 / 5,673 (**70th pct**) | 9,371 / 10,076 (7th pct) | 4,148 / 5,673 (27th pct) |

**Subgroup national ranks (averages)** [1]:

- **White students:** math 86th percentile, reading 97th.
- **Black students:** math 29th (math trend 94th), reading 39th (reading trend 45th).
- **Hispanic students:** math 24th.
- **Low-income students:** math 20th (trend 96th), reading 46th (trend 65th).

The low-income ranks compare *all* CH-UH students, because all are flagged low-income, with other districts' low-income students. They therefore probably flatter CH-UH.

### 1c. Learning rates, CH-UH and peers (SEDA 2025, grades 3–8, 2022–25)

A learning rate of 1.0 means students gain one grade level per grade, the national average. The figures below were read from each district's 2025 Stanford trends report [1][13]:

| District | Learning rate 2022–25 | National percentile | Avg. math / reading percentile |
|---|---|---|---|
| **CH-UH** | **0.76** | **14th** | 11th / 22nd |
| Stanford "similar districts" avg. | 0.92 | 40th | 5th / 7th |
| Ohio | 0.98 | — | — |
| Beachwood | 1.15 | 86th | 99th / 100th |
| Euclid | 1.09 | 78th | 3rd / 6th |
| Cleveland Municipal | 1.09 | 77th | 1st / 1st |
| Maple Heights | 1.05 | 71st | 3rd / 2nd |
| Lakewood | 1.02 | 64th | 92nd / 95th |
| Richmond Heights | 0.98 | 56th | 6th / 6th |
| Bedford | 0.94 | 47th | 6th / 8th |
| Warrensville Heights | 0.88 | 34th | 10th / 8th |
| Shaker Heights | 0.86 | 30th | 44th / 81st |
| Garfield Heights | 0.86 | 30th | 1st / 1st |
| South Euclid-Lyndhurst | 0.84 | 27th | 13th / 38th |

CH-UH's learning-rate trend is −0.05 per year in the report's table, ranked 4,512 of 6,065 (26th percentile); the report's own explanatory sentence says −0.04 [1].

**How to read this.** A learning rate is estimated by comparing scores across grades 3–8 in the same years. It can therefore be pulled down by enrollment patterns as well as by teaching. One example would be higher-scoring students leaving for private or charter schools in the middle grades. This page did not test that explanation. It conflicts with Ohio's value-added for 2025–26, which follows the same students over time (section 2). Value-added was also strongest at Heights High and the two middle schools.

### 1d. Recognition in the 2025 Education Scorecard

- The Scorecard's Ohio page (2025 results, May 13, 2026) names **Fairborn City, Cleveland Heights-University Heights City and Euclid City** as "leading the way in reading" [3].
- The "2024–2025 Districts on the Rise" PDF lists CH-UH in its **Reading** section. Other Ohio districts in that section are Big Walnut, Centerville, Euclid, Fairborn, Marion and Princeton. CH-UH is **not** in the "Math and Reading" section, where Ohio is represented by Anthony Wayne, Mayfield, Mount Vernon and Troy [4].
- Statewide context from the same page: Ohio ranked **14th of 38 states in math growth** and **24th of 35 in reading** from 2022 to 2025. The average Ohio student is about **0.26 grade levels below 2019 in math** and **0.52 below in reading** [3].

## 2. Ohio's Progress component (value-added)

Ohio's Progress component uses EVAAS value-added. Each student's growth is compared with growth predicted from that student's own prior test history, combined over up to three years. Three stars means students met expected growth.

| Report card year | Progress | Value-Added Growth Index (statewide pct.*) | Overall | Achievement | Gap Closing | PI |
|---|---|---|---|---|---|---|
| 2021–22 | 3 stars | +1.22 | not rated | 2 stars | 4 stars | 66.9 |
| 2022–23 | 3 stars | −1.10 (44th) | 3 stars | 2 stars | 5 stars | 70.6 |
| 2023–24 | 2 stars | −7.06 (14th) | 2.5 stars | 2 stars | 3 stars | 69.2 |
| 2024–25 | 3 stars | −0.68 (48th) | 3.5 stars | 2 stars | 4 stars | 74.6 |
| 2025–26 | **4 stars** | **+7.68 (87th)** | 3.5 stars | 3 stars | 5 stars | 79.0 |

*Source: DEW district "high-level" and Achievement data files, 2021–22 to 2025–26 [11]. \*Percentile among 607 traditional districts is an OpenHeights calculation. The Ohio PI is 82.8 for 2025–26 [12].*

**School-level Progress** [14]:

- **2025–26:** Heights High **5 stars**; Baumgardner Middle and Roxboro Middle **4 stars**; Boulevard, Fairfax and Gearity **3 stars**; Roxboro Elementary **2 stars**; Canterbury, Noble and Oxford **1 star**.
- **2024–25:** seven of 10 schools had 3 or more stars, which confirms the district's statement [5]. Heights High and Monticello Middle had 4 stars, and Canterbury had 1 star.

In 2025–26, growth was concentrated in the middle and high schools, and three elementary schools were below expected growth.

## 3. Ohio typology and "similar districts"

**Typology.** DEW's 2013 typology places CH-UH in **code 5, "Suburban – Low Student Poverty & Average Student Population Size"** (77 districts) [15]. The typology is based on 2010-era data, when 61% of CH-UH students were classed as low-income and the median income was $37,822 [15]. CH-UH is now far less like its group: 99.9% of its students are flagged economically disadvantaged, against a typology median of 36.7% (2025–26) [11].

Within typology 5 (OpenHeights calculation from [11]):

| Year | PI rank | Value-added rank |
|---|---|---|
| 2022–23 | 74th of 77 | 58th |
| 2023–24 | 75th | 76th |
| 2024–25 | 74th | 64th |
| 2025–26 | 72nd | **29th** |

**DEW "similar districts."** DEW's 2025 similar-district list for CH-UH has six districts: South Euclid-Lyndhurst, Norwood, Princeton, Winton Woods, Reynoldsburg and Northwest Local [16].

- **2025–26:** CH-UH's PI of 79.0 ranks **3rd of 7**, behind Norwood (79.8) and Princeton (79.3). The other four are South Euclid-Lyndhurst 75.9, Northwest 77.3, Reynoldsburg 73.6 and Winton Woods 63.8. The six-district average is 75.0. CH-UH's value-added (+7.68) is second to Princeton's (+17.77).
- **2024–25:** CH-UH's PI of 74.6 equaled the six-district average of 74.6.

All figures are OpenHeights calculations from [11][16].

## 4. Performance relative to poverty (statewide residual analysis)

**Method (OpenHeights calculation; reproducible).**

- **Data.** For every one of Ohio's 607 traditional public school districts and each year from 2022–23 to 2025–26, we took:
  - the district Performance Index (DEW Achievement file; for 2025–26, the "high-level" file);
  - the Value-Added Growth Index;
  - the percentages of enrolled students who are economically disadvantaged, students with disabilities, English learners, Black and Hispanic (DEW District Details file) [11].
  - Groups suppressed for having fewer than 10 students were set to 0%.
  - We also matched each district to the Census Bureau's **SAIPE 2024 child-poverty rate**: the share of resident children aged 5–17 in families below the poverty line [17]. The match used NCES IDs from the Common Core of Data directory [18].
- **Models.** Ordinary least squares, one observation per district, unweighted:
  - **M1:** PI on % economically disadvantaged.
  - **M2:** M1 plus % with disabilities, % English learners, % Black and % Hispanic.
  - **M4:** PI on census child poverty, % with disabilities and % English learners (no race terms).
  - A residual is actual PI minus predicted PI. The percentile is CH-UH's position among all 607 residuals.
- **Reproducing it.** The analysis uses DEW's public download files unchanged (Python with numpy least squares). Anyone with the files and the steps above can reproduce the results.

**CH-UH results by year:**

| Year | Actual PI | M1 predicted → residual (pct.) | M2 residual (pct.) | M4 predicted → residual (pct.) | R²: M1 / M2 / M4 |
|---|---|---|---|---|---|
| 2022–23 | 70.6 | 66.9 → **+3.7** (74th) | +12.5 (99th) | 77.1 → **−6.5** (13th) | 0.70 / 0.77 / 0.73 |
| 2023–24 | 69.2 | 67.5 → **+1.7** (62nd) | +10.5 (98th) | 76.3 → **−7.1** (12th) | 0.72 / 0.77 / 0.72 |
| 2024–25 | 74.6 | 77.3 → **−2.7** (34th) | +11.2 (96th) | 77.6 → **−3.0** (30th) | 0.53 / 0.68 / 0.72 |
| 2025–26 | 79.0 | 78.3 → **+0.7** (53rd) | +13.5 (98th) | 77.9 → **+1.1** (55th) | 0.53 / 0.68 / 0.71 |

N = 607 districts in every year. A version of M4 with race terms added (M3) gives CH-UH residuals of +2.1, +0.8, +2.7 and +5.6, at the 64th, 51st, 67th and 86th percentiles.

**Peers, 2025–26** (OpenHeights calculation from [11][17]):

| District | % econ. disadv. | Child poverty (SAIPE) | PI | M1 residual (pct.) | M2 residual (pct.) | M4 residual (pct.) | Value-added index (pct.) |
|---|---|---|---|---|---|---|---|
| **CH-UH** | 99.9 | 18.9% | **79.0** | **+0.7 (53)** | **+13.5 (98)** | **+1.1 (55)** | **+7.68 (87)** |
| Beachwood | 14.2 | 7.0% | 103.3 | +4.0 (73) | +12.4 (98) | +11.5 (99) | +10.72 (92) |
| Lakewood | 40.0 | 11.6% | 93.3 | +0.3 (50) | +2.3 (64) | +5.5 (86) | −2.93 (35) |
| Shaker Heights | 39.9 | 10.0% | 86.8 | −6.2 (18) | +3.3 (72) | −3.2 (30) | +9.53 (91) |
| South Euclid-Lyndhurst | 99.8 | 15.0% | 75.9 | −2.4 (35) | +10.8 (96) | −6.2 (14) | −2.92 (35) |
| Richmond Heights | 99.3 | 17.6% | 70.3 | −8.1 (13) | +3.8 (74) | −13.3 (2) | +7.83 (88) |
| Warrensville Heights | 100.0 | 32.9% | 68.7 | −9.5 (9) | +7.5 (91) | +3.7 (72) | +6.04 (84) |
| Euclid | 99.9 | 27.3% | 66.7 | −11.6 (7) | +5.1 (82) | −2.4 (34) | +8.15 (88) |
| Bedford | 99.9 | 22.7% | 65.1 | −13.2 (5) | +3.1 (69) | −6.9 (12) | +4.81 (80) |
| Maple Heights | 100.0 | 31.0% | 61.7 | −16.5 (2) | −0.2 (48) | −5.4 (18) | +0.38 (58) |
| Cleveland Municipal | 100.0 | 37.9% | 59.9 | −18.3 (2) | 0.0 (49) | +7.8 (94) | +17.18 (97) |
| Garfield Heights | 98.0 | 28.0% | 57.9 | −20.8 (1) | −6.4 (15) | −12.7 (2) | +0.09 (55) |

**Plain-language reading.**

- **Against the poverty flag alone (M1),** CH-UH scores about what a district whose students are all flagged disadvantaged is predicted to score. It has done better than most Cuyahoga peers that are also near 100%. The poverty flag predicts the same PI for all of those districts, so this mainly says CH-UH outperforms Euclid, Maple Heights, Bedford, Warrensville and Garfield Heights.
- **With race added (M2),** CH-UH looks exceptional. Statewide, the race terms pick up differences in poverty and disadvantage that the crude poverty flag misses. CH-UH is then being compared mostly with majority-Black, higher-poverty districts. This is a statistical description, not a claim that race causes outcomes.
- **Against census child poverty (M4),** CH-UH was well below prediction in 2022–24 and is now slightly above. Census poverty counts all resident children, including the many CH-UH residents in private, charter and voucher-funded schools. It probably *understates* the disadvantage of the students CH-UH actually enrolls. SAIPE counts about **8,400** school-age residents [17], while the district enrolled **4,683** students in 2025–26 [11]. That pushes the M4 residual down.
- **Change over time.** From 2023–24 to 2025–26, CH-UH's PI rose 9.8 points. Its residual rose 8.2 points on M4, 4.8 on M3 and 3.0 on M2. On M1 it moved from +1.7 to +0.7. M1's predicted value for CH-UH jumped 10.8 points over the same period, because the poverty flag changed statewide (see the caveat below). That makes M1 a poor guide to change over time.

**Important data caveat.** Ohio's "economically disadvantaged" flag is reported as **99.9–100%** for CH-UH in every year studied [11]. The number of districts reporting at least 99.5% jumped from 56–57 (2022–23, 2023–24) to **157 (2024–25) and 187 (2025–26)**, and M1's R² fell from about 0.71 to 0.53 (OpenHeights count from [11]). The flag no longer distinguishes moderately poor districts from very poor ones. This page has not established why the count rose. Results that rely on this flag (M1, M2) should be read with that in mind.

## 5. Cost-effectiveness

**No outcome-per-dollar figure is published here.** Spending per pupil is covered on the finance page of this site. Linking spending to the outcomes above needs care, for three reasons:

1. **The nonpublic-student distortion.** CH-UH's books include costs for students who don't attend its schools, such as EdChoice deductions, transportation for private-school students and auxiliary services. Districts with high private-school or voucher participation can therefore look more expensive per pupil than they are.
2. **Need-based costs.** Higher-poverty districts, and districts with more students with disabilities (22.2% at CH-UH in 2025–26 [11]), face higher costs to reach the same outcomes.
3. **Levels versus growth.** Comparing spending with PI mostly measures demographics. Comparing spending with value-added or learning rates is more meaningful, and those two measures currently disagree for CH-UH.

## 6. Subgroups: comparing like with like

ESSA Performance Index by student group. ESSA PI excludes the "Advanced Plus" level, so the all-students figure (78.6) is slightly below the report-card PI (79.0) [12]:

| Group | 2022–23 | 2023–24 | 2024–25 | 2025–26 | CH-UH rank among districts reporting the group, 2025–26* |
|---|---|---|---|---|---|
| **Black students, CH-UH** | 63.3 | 61.4 | 66.5 | **70.9** | 191st of 319 (40th pct.) |
| Black students, Ohio | 58.1 | 59.0 | 61.9 | 63.0 | |
| **Econ. disadvantaged, CH-UH** | 70.5 | 69.1 | 74.3 | **78.6** | 424th of 606 (30th pct.) |
| Econ. disadvantaged, Ohio | 67.3 | 69.0 | 73.0 | 73.8 | |
| White students, CH-UH | 100.5 | 101.8 | 103.9 | 107.7 | |
| White students, Ohio | 87.8 | 87.8 | 89.0 | 89.3 | |

*\*OpenHeights calculation from [12]. Ranks in earlier years: Black students 234th of 314 (2022–23), 254th of 315 (2023–24) and 226th of 322 (2024–25). Economically disadvantaged students 518th, 540th and 507th of 606.*

**2025–26 peer values** for Black and economically disadvantaged students respectively [12]:

| District | Black students | Econ. disadvantaged |
|---|---|---|
| CH-UH | 70.9 | 78.6 |
| South Euclid-Lyndhurst | 72.8 | 75.5 |
| Shaker Heights | 67.7 | 65.9 |
| Lakewood | 67.7 | 79.8 |
| Euclid | 65.3 | 66.6 |
| Cleveland Municipal | 55.9 | 59.9 |
| Beachwood | 85.4 | 89.5 |

**Reading this.**

- **Black students** in CH-UH scored **7.9 points above** Ohio's Black-student average in 2025–26, up from 2.4 points above in 2023–24 (OpenHeights calculation). They were still below the median district-level result for Black students. Ohio's average is weighted toward large urban districts, while many suburban districts report higher Black-student scores.
- The **economically disadvantaged** comparison flatters CH-UH. CH-UH's "disadvantaged" group is its entire enrollment, while elsewhere the flag picks out the poorer students.
- Gap Closing reached **5 stars in 2025–26** [11].

## 7. Limitations

- **The poverty flag is crude.** CH-UH's 99.9% economically disadvantaged figure covers students who would not be counted as poor under income tests. Statewide, the flag became less informative from 2024–25 (section 4).
- **Selection through private schools and EdChoice.** Many resident children attend private, charter or voucher-funded schools. Census measures describe all residents, and state measures describe only those enrolled, so neither matches the enrolled population well. Who leaves, and whether they would have scored higher or lower, affects CH-UH's averages, its residuals and possibly its SEDA learning rate. That is not measured here.
- **Model dependence.** CH-UH's residual ranges from the 12th to the 99th percentile depending on the controls and the year. The more robust findings are the rise in PI and value-added since 2023–24, and the low SEDA learning rate, not any single rank.
- **Regression to the mean.** CH-UH's large 2019→22 math drop (−1.59 grade levels) makes some later rebound likely by statistical reversion alone.
- **Tests and report-card rules change.** Ohio moved to star ratings in 2021–22 and has adjusted weights since. SEDA links state tests to NAEP, which adds estimation error, especially for a district of about 4,700 students.
- **Value-added caveats.** EVAAS adjusts for prior scores but not directly for poverty. Composites span up to three years, and star cut points are policy choices.
- **Residuals are descriptive.** A residual is a gap between actual and predicted scores, not a causal estimate of school quality.

## Gaps / unverified

1. **SEDA district data files** (for example, learning rates for every district) were not downloaded. The edopportunity.org data page did not expose direct file links. Peer learning rates were read from each district's PDF report instead [13].
2. **Subgroup value-added** (for example, for students with disabilities or the lowest 20%) was not extracted. The DEW value-added detail files are available [11].
3. **Why Ohio's economically disadvantaged counts jumped in 2024–25** has not been documented. Confirming it would need DEW guidance.
4. **A resident-versus-enrolled adjustment** (for example, using the ACS for enrolled public-school children only) was not attempted. The Census API now requires a key, which this research did not have.
5. **Students-with-disabilities subgroup PI for CH-UH** did not appear in the district ESSA PI sheet extracted here.

## Corrections log

- **2026-10-12** — Math change 2022→23 (Scorecard): **+0.70 → +0.69**, as printed in the report [2]. The earlier figure was computed from rounded values.
- **2026-10-12** — The "conflicting" 2023 values −2.48 / −1.80 were identified as **Black-student** results, not an error [2].
- **2026-10-12** — "Districts on the Rise": CH-UH is on the **Reading** list, **not "math and reading"** [4]. Euclid, Fairborn and Marion City are on the same Reading list.
- **2026-10-12** — Ohio's 2025 math gap versus 2019: "about one-third of a grade level" → **about 0.26 grade levels**. Reading: "over half" → **0.52** [3].
- **2026-10-12** — The school-level name was confirmed as **Baumgardner Middle School** (4 stars, 2025–26), not a misreading [14].
- **2026-10-12** — SEDA 2022–25 values previously unassigned are now assigned: **−1.66** is the all-students average; **+0.05/yr** is the all-students score trend; **−0.04/yr** is the similar-district score trend (and the learning-rate trend in the report's text) [1]. The subgroup percentiles (97th, 39th, 46th) are **reading** ranks for White, Black and low-income students [1].
- **2026-10-12** — PI 69.2 (2023–24), 74.6 (2024–25) and 79.0 (2025–26); Progress 2, 3 and 4 stars; Achievement 3 stars and Gap Closing 5 stars (2025–26); and the 93.0% four-year graduation rate were all **confirmed** in DEW data files [11]. They were previously district-reported only.

## Sources

1. Educational Opportunity Project at Stanford, "Trends in Academic Performance in Cleveland Heights-University Heights City," version 2025.1 (generated Apr. 28, 2026; school years 2022–25). https://edopportunity.org/reports/trends/2025/OH/report_OH_3904379_cleveland-heights-university-heights-city.pdf
2. Education Recovery Scorecard (Harvard CEPR / Stanford EOP), district report for Cleveland Heights-University Heights City (January 2024 release; 2019–2023 data). https://educationscorecard.org/wp-content/uploads/2024/01/report_OH_3904379_cleveland-heights-university-heights-city.pdf
3. Education Scorecard, Ohio state page, 2025 results (press release May 13, 2026). https://educationscorecard.org/states/ohio/
4. Education Scorecard, "2024-2025 Districts on the Rise" (PDF). https://educationscorecard.org/wp-content/uploads/2026/05/Districts-on-the-Rise.pdf
5. CH-UH City School District, "CH-UH Announces Report Card Gains For 2024-2025." https://www.chuh.org/p/~board/district-board-posts/post/ch-uh-announces-report-card-gains-for-2024-2025
6. News 5 Cleveland, "Ohio school report cards released: East Cleveland and Akron Public School districts see improvements" (2025). https://www.news5cleveland.com/news/local-news/ohio-school-report-cards-released-east-cleveland-and-akron-public-school-districts-see-improvements
7. CH-UH City School District, "CH-UH Announces Report Card Gains For 2025-2026" (September 2026). https://www.chuh.org/p/~board/district-board-posts/post/ch-uh-announces-report-card-gains-for-2025-2026
8. Cleveland.com via NewsBreak, "Cleveland Heights-University Heights maintains 3.5 stars: Ohio school report cards 2026." https://www.newsbreak.com/cleveland-com-512965/4889945722889-cleveland-heights-university-heights-maintains-3-5-stars-ohio-school-report-cards-2026
9. Ohio School Report Cards (DEW). https://reportcard.education.ohio.gov/
10. Stanford Educational Opportunity Project explorer. https://edopportunity.org/trends/explorer
11. DEW report card "Download Data," district files for 2021–22 to 2025–26: DISTRICT_HIGH_LEVEL_2122 … 2526; 22-23/23-24/24-25_Achievement_District; 2023–2026_District_Details. https://reportcard.education.ohio.gov/download
12. DEW report card "Download Data," 2023–2026 Title I Performance Index files (State and District ESSA PI by student group). https://reportcard.education.ohio.gov/download
13. Educational Opportunity Project, 2025 trends reports for peer districts, at https://edopportunity.org/reports/trends/2025/OH/ — Beachwood (3904355), Bedford (3910017), Cleveland Municipal (3904378), Euclid (3904395), Garfield Heights (3904404), Lakewood (3904419), Maple Heights (3904430), Richmond Heights (3904659), Shaker Heights (3904475), South Euclid-Lyndhurst (3904479), Warrensville Heights (3904500).
14. DEW report card "Download Data," BUILDING_HIGH_LEVEL_2425 and BUILDING_HIGH_LEVEL_2526. https://reportcard.education.ohio.gov/download
15. DEW, "Typology of Ohio School Districts" and 2013 School District Typology file. https://education.ohio.gov/Topics/Data/Frequently-Requested-Data/Typology-of-Ohio-School-Districts
16. DEW report card "Download Data," Historical Similar District Data File 2006 to 2025 (List_2025). https://reportcard.education.ohio.gov/download
17. U.S. Census Bureau, Small Area Income and Poverty Estimates (SAIPE), 2024 school district estimates (ussd24.txt). https://www2.census.gov/programs-surveys/saipe/datasets/2024/2024-school-districts/ussd24.txt
18. NCES Common Core of Data, 2022 district directory, via the Urban Institute Education Data API (IRN to NCES ID crosswalk). https://educationdata.urban.org/api/v1/school-districts/ccd/directory/2022/?fips=39
