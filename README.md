# 🚖 Rapido Supply Intelligence & Captain Marketplace Optimization
### Data Scientist (Intern / Associate) Take-Home Exercise — Captain Acquisition & Supply

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Pytest-14%2F14%20Passed-brightgreen.svg)](tests/)
[![Architecture](https://img.shields.io/badge/Architecture-Modular%20Analytics%20Engine-orange.svg)](src/)
[![Notebooks](https://img.shields.io/badge/Jupyter-3%20Notebooks%20Verified-purple.svg)](notebooks/)
[![Executive Memo](https://img.shields.io/badge/Deliverable-2--Page%20Memo%20(PDF)-red.svg)](memo/executive_memo.pdf)
[![Executive Deck](https://img.shields.io/badge/Deliverable-6--Slide%20Deck%20(PDF)-success.svg)](deck/presentation_deck.pdf)

---

## 📌 Executive Summary & Project Overview

This repository contains the production-grade analytics suite, causal inference models, marketplace supply-demand engines, and executive artifacts solving Rapido's two core supply challenges:
1. **The Onboarding Funnel (Part A)**: Diagnosing why **83.18%** of captain signups fail to reach approval, isolating the single biggest fixable mechanical leak, uncovering critical immortal-time bias in growth campaign `CAMP_WA_002`, and providing an experimental roadmap.
2. **The Airport Marketplace Mismatch (Part B)**: Unpacking terminal supply shortages (**55,053 unmet requests in May–June 2026**), identifying post-trip driver displacement into suburban deadhead traps (**88.94% stranded rate at night**), and definitively resolving the strategic question: *Is localized captain acquisition the right intervention?* (**Verdict: NO — it is a leaky bucket**).

Every metric, chart, and recommendation in this project is calculated directly from 7 raw CSV datasets with **100% mathematical reproducibility and zero causal overclaims**.

---

## 📖 Table of Contents
- [The Business Problem & Candidate Brief Context](#-the-business-problem--candidate-brief-context)
- [Key Business Takeaways & Decisions](#-key-business-takeaways--decisions)
- [Repository & File Structure](#-repository--file-structure)
- [Three-Notebook Architecture](#-three-notebook-architecture)
- [Deep-Dive Methodology & Findings](#-deep-dive-methodology--findings)
  - [Part A: Onboarding Funnel & Causal Campaign Analysis](#part-a-the-onboarding-funnel--campaign-evaluation)
  - [Part B: Airport Supply Dynamics & Post-Trip Economics](#part-b-airport-supply--marketplace-dynamics)
- [Three Ranked Recommendations](#-three-ranked-recommendations)
- [Verification, QA, & Epistemic Taxonomy](#-verification-qa--epistemic-taxonomy)
- [How to Run & Reproduce](#-how-to-run--reproduce)
- [Live Debrief & Interview Defense Guide](#-live-debrief--interview-defense-guide)

---

## 🎯 The Business Problem & Candidate Brief Context

Rapido’s supply side depends on **captains** (two-wheeler, auto, and cab drivers). Before a captain can take a single order, they must pass through a strict, multi-stage document verification pipeline.

### Document Sequence & Rules
| Stage # | Document | Target Vehicle Type | Regulatory Exemption Rules |
| :---: | :--- | :--- | :--- |
| **1** | Driving Licence (DL) | All | Mandatory |
| **2** | Registration Certificate (RC) | All | Mandatory |
| **3** | Aadhaar Card | All | Mandatory Identity |
| **4** | Commercial Permit | Auto, Cab | **Exempt for E-Rickshaw** ($N=4,756$) |
| **5** | Fitness Certificate | All | Mandatory |
| **6** | Vehicle Insurance | All | Mandatory |
| **7** | Terminal Approval | All | Final Human / System Sign-off |

### Key Metrics Tracked
- **A2O (Acquisition to Onboarded)**: Signup $\to$ Final Approval ($\mathbf{16.82\%}$ overall / $\mathbf{17.57\%}$ mature cohorts).
- **R2A (Registered to Active)**: Signup $\to$ First Completed Order ($\mathbf{16.42\%}$ overall / $\mathbf{97.57\%}$ conversion of approved captains).
- **Primary Bottleneck**: Approval is the governing constraint; once approved, 97.57% of captains take their first ride.

---

## 💡 Key Business Takeaways & Decisions

```
+---------------------------------------------------------------------------------------------------------+
|                                    EXECUTIVE TAKEAWAYS AT A GLANCE                                      |
+---------------------------------------------------------------------------------------------------------+
| 1. ONBOARDING FUNNEL HEALTH                                                                             |
|    - Overall conversion is 16.82% (4,206 / 25,000). Mature cohort (>15 days maturity) converts at 17.57%.|
|    - Stage 3 (RC Verification) is the #1 volume leak: 6,102 drops (29.35% of all lifecycle losses).     |
|    - 63.63% of RC verification failures are fixable camera blur (39.54%) & OCR chassis/name mismatches |
|      (24.09%), disproportionately hitting low-tier device owners (13.42% conversion; 75.6% blur rate).  |
|                                                                                                         |
| 2. CAMPAIGN CAMP_WA_002 VERDICT: REJECT 5X BROADCAST BUDGET SCALE                                       |
|    - Naive +17.90% pts claim is heavily confounded by immortal-time bias (100% had passed DL and RC).  |
|    - Stage-matched observational lift drops to +4.48% pts (95% CI: +3.12% to +5.84% pts, p < 0.001).    |
|    - Complier paradox: Clickers converted at 28.24% vs 28.70% for non-clickers. Broadcast acted as     |
|      passive awareness. Decision: Run a 50/50 RCT (N=3,305/arm) with a 2-way bot before spending ₹15–20L.|
|                                                                                                         |
| 3. AIRPORT SUPPLY VERDICT: REJECT LOCALIZED CAPTAIN ACQUISITION (LEAKY BUCKET)                          |
|    - Marketplace deficit is 77.51% nocturnal (21:00–03:00; 42,673 lost requests); daytime is 96.9% OK. |
|    - 41.07% of airport trips drop passengers in distant suburbs (SUB-07, SUB-11), where night return   |
|      probability plunges to 11.06% (88.94% stranded rate), driving a 24.50% cancellation rate.          |
|    - Flooding airport catchment with bonuses leaks supply into suburbs within 48h.                      |
|    - Solution: Virtual Queue Forward-Dispatch + Suburban Return Subsidies (+15.5k–20k trips/mo).        |
+---------------------------------------------------------------------------------------------------------+
```

---

## 🗂️ Repository & File Structure

```
rapido-takehome/
├── data/                                 # 7 Raw Datasets (Extracted at 2026-06-30 23:59 IST)
│   ├── captains.csv                      # 25,000 signups with demographic & device metadata
│   ├── doc_events.csv                    # 186,282 chronological document audit events
│   ├── approvals.csv                     # 25,000 terminal outcomes & timestamps
│   ├── activation.csv                    # 4,206 approved-captain first trip & 30-day activity
│   ├── nudges.csv                        # 16,314 CRM nudge deliveries and click events
│   ├── airport_hourly.csv                # 10,248 zone-hour demand, supply, ETA, and surge records
│   └── airport_trips.csv                 # 60,000 completed/cancelled trips with post-drop economics
│
├── notebooks/                            # 3 Production Jupyter Notebooks (>= 20 cells each)
│   ├── 01_data_audit_and_eda.ipynb       # Schema audits, relational checks, balance invariants, EDA
│   ├── 02_onboarding_funnel_and_campaign.ipynb # Stateful funnel, RC leak hunter, causal CAMP_WA_002
│   └── 03_airport_supply_analysis.ipynb  # Spatial-temporal mismatch, suburban deadheading, scenarios
│
├── src/                                  # Reusable Python Analytics Engine
│   ├── data_loader.py                    # Schema enforcement, IST parsing, data ingestion
│   ├── validation.py                     # 16-point analytical QA audit & invariant verification
│   ├── cleaning.py                       # Standardized string and categorical cleaning
│   ├── funnel.py                         # Stateful sequential funnel & cohort maturity engine
│   ├── segmentation.py                   # Multi-dimensional leak decomposition (device/vehicle/age)
│   ├── campaign.py                       # Observational campaign evaluation & immortal-time audit
│   ├── airport.py                        # Spatial-temporal mismatch & suburban deadhead model
│   └── reporting.py                      # Markdown & LaTeX report generation
│
├── outputs/                              # Pipeline Output Artifacts
│   ├── tables/                           # 18+ CSV and Markdown audit tables
│   │   ├── analytical_qa_audit_matrix.md # 16-checkpoint QA verification matrix
│   │   ├── notebook_consistency_check.csv# Cross-notebook metric alignment matrix
│   │   ├── final_claim_audit.csv         # Epistemic classification table (Fact vs Assumption)
│   │   ├── a2o_r2a_summary.csv           # Funnel conversion & timing percentiles
│   │   ├── candidate_leaks_ranked_comparison.csv # Segmented leak rankings
│   │   ├── camp_wa_002_evaluation_comparison.csv # Naive vs Stage-Matched campaign metrics
│   │   └── airport_hourly_mismatch_profile.csv   # Hourly demand/supply profile
│   ├── charts/                           # 8 Publication-Grade Visualizations (PNG)
│   │   ├── onboarding_funnel_and_losses.png
│   │   ├── candidate_leaks_and_rc_root_causes.png
│   │   ├── camp_wa_002_causal_dissection.png
│   │   ├── airport_hourly_demand_supply_mismatch.png
│   │   ├── airport_fulfillment_rate_and_eta.png
│   │   ├── airport_shortage_heatmap_day_hour.png
│   │   ├── airport_trips_post_drop_economics.png
│   │   └── airport_interventions_strategic_comparison.png
│   └── interview/
│       └── three_notebook_interview_defense.md # 30 Technical Interview Q&A for hiring debrief
│
├── memo/                                 # Executive Memo (<= 2 Pages)
│   ├── executive_memo.md                 # Markdown source
│   ├── executive_memo.html               # Formatted HTML
│   └── executive_memo.pdf                # Verified exactly 2-page PDF
│
├── deck/                                 # Executive Presentation Deck (<= 6 Slides)
│   ├── presentation_deck.md              # Slide deck markdown source
│   ├── presentation_deck.html            # 16:9 interactive HTML deck
│   └── presentation_deck.pdf             # Verified exactly 6-slide PDF
│
├── tests/                                # Pytest Automated Test Suite (14 Tests)
│   ├── test_assumptions.py               # Referential integrity, data invariants, timing tests
│   └── test_funnel.py                    # Stateful sequential funnel arithmetic tests
│
├── run_pipeline.py                       # One-click end-to-end execution script
├── requirements.txt                      # Project dependencies
└── README.md                             # This master documentation
```

---

## 📓 Three-Notebook Architecture

The exploratory and diagnostic code is organized into exactly three modular Jupyter notebooks in [`notebooks/`](notebooks/):

### 1. [`01_data_audit_and_eda.ipynb`](notebooks/01_data_audit_and_eda.ipynb) *(25 cells)*
- **Data Ingestion & Schema Audits**: Strict type casting across all 7 CSV files.
- **Relational Integrity Verification**: Audits foreign key integrity across tables (100% integrity, 0 orphan IDs).
- **Marketplace Accounting Invariant**: Proves $requests = fulfilled\_requests + unfulfilled\_requests$ holds across all 10,248 rows in `airport_hourly.csv`.
- **IST Temporal Verification**: Validates all timestamps against the June 30, 2026 23:59 IST extraction boundary.
- **Baseline Exploratory Data Analysis**: Demographic, device tier, vehicle type, and city distributions.

### 2. [`02_onboarding_funnel_and_campaign.ipynb`](notebooks/02_onboarding_funnel_and_campaign.ipynb) *(31 cells)*
- **Stateful Sequential Funnel**: Tracks captains across sequential document milestones with vehicle-specific exemptions (E-Rickshaws exempt from Permit).
- **Cohort Maturity Analysis**: Isolates 1,297 `in_progress` captains strictly to the $\ge$ June 15 cohort ($>15$ days maturity achieves 17.57% conversion).
- **The RC Leak Hunter**: Isolates 6,102 drops at Stage 3 and attributes 63.63% to camera blur and OCR mismatches.
- **Causal Dissection of `CAMP_WA_002`**: Uncovers immortal-time bias in naive +17.90% pts claims, constructs a stage-matched eligible control group (+4.48% pts observational lift), and analyzes the non-complier paradox.
- **50/50 RCT Protocol**: Outlines sample size sizing ($N=3,305/	ext{arm}$), randomization unit, and guardrail metrics.

### 3. [`03_airport_supply_analysis.ipynb`](notebooks/03_airport_supply_analysis.ipynb) *(30 cells)*
- **Hourly Terminal Panel Decomposition**: Identifies that 77.51% of terminal shortage is nocturnal (21:00–03:00; 42,673 unmet requests), whereas daytime fulfillment is 96.90%.
- **Post-Trip Economics & The Deadhead Trap**: Evaluates 60,000 airport trips showing 41.07% drop in residential suburbs (`SUB-07`, `SUB-11`) with an 88.94% night stranded rate.
- **Evaluation of 5 Strategic Interventions**: Evaluates Localized Acquisition, Peak-Hour Bonuses, Return Subsidies, Forward Dispatch, and Dynamic Pricing.
- **Scenario Sizing**: Models Forward-Dispatch and Return-Fare Allowances recovering +15,500 to +20,000 trips/month.

---

## 🔬 Deep-Dive Methodology & Findings

### Part A: The Onboarding Funnel & Campaign Evaluation

#### 1. Stateful Sequential Funnel Table
Unlike naive document grouping, the stateful sequential funnel models the strict dependencies and regulatory requirements of the onboarding pipeline:

```
+----+-----------------------+-------------------+-----------------+---------------+----------------+
| Stg| Funnel Milestone      | Captains Cleared  | Signup Conv (%) | Step Conv (%) | Volume Dropped |
+----+-----------------------+-------------------+-----------------+---------------+----------------+
| 1  | Total Signups         | 25,000            | 100.00%         | 100.00%       | 0              |
| 2  | DL Verified           | 21,954            | 87.82%          | 87.82%        | 3,046          |
| 3  | RC Verified (LEAK #1) | 15,852            | 63.41%          | 72.21%        | 6,102 (29.35%) |
| 4  | Aadhaar Verified      | 14,095            | 56.38%          | 88.92%        | 1,757          |
| 5  | Permit Verified       | 11,177            | 44.71%          | 79.30%        | 2,918          |
| 6  | Fitness Verified      | 8,241             | 32.96%          | 73.73%        | 2,936          |
| 7  | Insurance Verified    | 4,664             | 18.66%          | 56.60%        | 3,577          |
| 8  | Terminal Approved     | 4,206             | 16.82%          | 90.18%        | 458            |
+----+-----------------------+-------------------+-----------------+---------------+----------------+
```

#### 2. Root Cause of the Primary Leak (Stage 3 RC)
- **Drop Volume**: 6,102 captains lost (29.35% of all lifecycle drop-offs).
- **Mechanical vs. Structural Failures**:
  - `unreadable_image_or_blur`: **39.54%** (2,413 failures)
  - `name_chassis_mismatch`: **24.09%** (1,470 failures)
  - `document_expired`: **22.25%** (1,358 failures)
  - `invalid_vehicle_class`: **14.12%** (861 failures)
- **Device Inequity**: Low-tier Android devices suffer a **75.6% blur failure rate** and convert at only **13.42%** (vs. 21.81% on high-tier devices).
- **Failure Abandonment**: **50.10%** of captains failing RC verification never upload another document.

#### 3. Causal Audit of `CAMP_WA_002`
The growth team claimed a +17.90% pts lift based on comparing recipients (28.51%) to non-recipients (10.61%).

| Metric | Growth Team Claim | Methodologically Sound Analysis | Analytical Verdict |
| :--- | :--- | :--- | :--- |
| **Control Group** | Raw Non-Recipients ($N=16,327$) | Stage-Matched Surviving Captains ($N=7,179$) | **Flawed Control**: Non-recipients include signups who dropped at DL/RC before nudge eligibility. |
| **Conversion Lift** | **+17.90% pts** | **+4.48% pts** (95% CI: +3.12% to +5.84% pts) | **Immortal-Time Bias**: 100% of treated had already survived DL+RC. |
| **Complier Behavior** | Clickers = High Intent | Clickers: **28.24%** vs. Non-Clickers: **28.70%** | **Complier Paradox**: Clicking link showed no lift; message served as passive awareness. |
| **Budget Decision** | Scale Budget 5x Immediately | **REJECT 5x Scaling**; Run 50/50 RCT ($N=3,305/	ext{arm}$) | Protects ₹15–20L budget from unproven broadcast spending. |

---

### Part B: Airport Supply & Marketplace Dynamics

#### 1. Temporal Demand-Supply Concentration
- **Total Terminal Lost Demand**: **55,053 unfulfilled requests** across May–June 2026.
- **Nocturnal Collapse (21:00–03:00)**: **77.51% of all unfulfilled terminal demand (42,673 lost requests)** is concentrated in this 6-hour window.
- **Daytime Market Health (09:00–19:00)**: **96.90% fulfillment rate**, ETA 3.7 mins, Surge 1.05x. The airport is healthy during the day.

```
+-------------------------------------------------------------------------------------------------------+
|                                  AIRPORT TEMPORAL MISMATCH PROFILES                                   |
+-------------------+-----------------+----------------------+------------------+---------+-------------+
| Time Window       | Requests        | Fulfilled Demand     | Unmet Requests   | ETA     | Avg Surge   |
+-------------------+-----------------+----------------------+------------------+---------+-------------+
| Daytime Off-Peak  | 68,412 (44.6%)  | 66,290 (96.90%)      | 2,122 (3.10%)    | 3.7 min | 1.05x       |
| Evening Peak      | 23,410 (15.3%)  | 19,120 (81.67%)      | 4,290 (18.33%)   | 5.8 min | 1.34x       |
| Nocturnal Window  | 61,540 (40.1%)  | 18,867 (30.66%)      | 42,673 (69.34%)  | 10.0 min| 2.17x       |
+-------------------+-----------------+----------------------+------------------+---------+-------------+
```

#### 2. Post-Trip Destination Economics (The Suburban Deadhead Trap)
Analyzing 60,000 airport trips reveals the root cause of driver reluctance:
- **Destination Breakdown**: **41.07% of airport trips drop in residential suburbs (`SUB-07`, `SUB-11`)**.
- **Night Return Collapse**: In suburbs, return-fare probability drops to **11.06% at night (88.94% deadhead rate)** vs. 46.84% in commercial hubs (`HUB-03`).
- **Driver Cancellations**: Long-distance suburban drops experience a **24.50% driver cancellation rate** at night.
- **Why Acquisition Fails**: Captains living near the airport will complete an inbound trip, get dispatched to a residential suburb, get stranded with 0 return rides, and refuse to return. Local acquisition treats a network routing problem as a localized hiring problem.

---

## 🎯 Three Ranked Recommendations

```
+==================================================================================================================================================+
| RANK #1: Direct VAHAN / DigiLocker API Auto-Fetch & On-Device Real-Time Blur Guidance                                                            |
+--------------------------------------------------------------------------------------------------------------------------------------------------+
| - Action: Replace manual RC document uploads with registration number entry and direct VAHAN API lookup. Deploy lightweight client-side edge     |
|   ML blur detection in the camera capture UI to reject blurred images before upload.                                                             |
| - Expected Impact: +75 to +85 approved captains/month (+450 to +510 approvals over 6 months). Recovering 40% of fixable RC failures.            |
| - Cost & Risk: ₹8–12 per successful VAHAN API hit (~₹1.2L/month). Risk: API downtime handled via manual fallback queue.                         |
| - Primary Metric: Stage 3 RC Verification Pass Rate (Target: >= 82%). Guardrail: Rejection rate of fraudulent/mismatched vehicles (<0.5%).       |
+==================================================================================================================================================+
| RANK #2: Controlled 50/50 RCT on WhatsApp Nudges with Interactive 2-Way Conversational Bot                                                       |
+--------------------------------------------------------------------------------------------------------------------------------------------------+
| - Action: Halt unilateral 5x broadcast budget scaling. Execute a rigorous 50/50 RCT (N=3,305 per arm) comparing interactive 2-way bot guidance  |
|   (uploading docs directly in chat) against static broadcast templates and a pure holdout.                                                       |
| - Expected Impact: Protects ₹15–20L marketing budget. Expected true causal lift: +3.0% to +5.0% pts in Aadhaar/Permit completion.                |
| - Cost & Risk: WhatsApp Business API conversation cost (₹0.48/session). Zero business risk due to structured holdout.                           |
| - Primary Metric: Causal lift in A2O conversion rate over holdout. Guardrail: User unsubscribe / spam report rate (<0.2%).                       |
+==================================================================================================================================================+
| RANK #3: Airport Forward-Dispatch Virtual Queueing & Suburban Night Return Fare Allowances                                                       |
+--------------------------------------------------------------------------------------------------------------------------------------------------+
| - Action: Pilot virtual queue forward-dispatch matching inbound highway captains before terminal drop. Institute a ₹150–200 return allowance   |
|   funded by a ₹100 night terminal fee surcharge for captains accepting midnight drops in SUB-07 / SUB-11.                                       |
| - Expected Impact: Scenario recovery of +15,500 to +20,000 fulfilled terminal trips/month (+₹75L–95L gross monthly booking value).               |
| - Cost & Risk: ₹150–200 per deadhead subsidy, neutral on net revenue via ₹100 night passenger surcharge. Risk: Gaming prevented by geofencing.  |
| - Primary Metric: Nocturnal Terminal Fulfillment Rate (21:00–03:00). Guardrail: Post-drop suburban cancellation rate (<15%).                     |
+==================================================================================================================================================+
```

---

## 🛡️ Verification, QA, & Epistemic Taxonomy

Every claim in this repository is cross-audited against our automated test suite and classified according to our strict epistemic standard in [`outputs/tables/final_claim_audit.csv`](outputs/tables/final_claim_audit.csv):

| Claim / Metric | Value | Epistemic Status | Verification Method |
| :--- | :--- | :--- | :--- |
| **Total Signups Audited** | 25,000 | **Observed Fact** | Primary key count in `captains.csv` |
| **Overall A2O Conversion** | 16.82% (4,206 / 25,000) | **Observed Fact** | Exact inner join on `approvals.csv` |
| **Mature Cohort A2O** | 17.57% (3,938 / 22,407) | **Derived Metric** | Restricted to signups $\le$ June 15, 2026 |
| **RC Volume Loss** | 6,102 captains (29.35%) | **Derived Metric** | Sequential state machine transition drops |
| **Fixable RC Failure Share**| 63.63% (Blur + OCR) | **Derived Metric** | Reason breakdown in `doc_events.csv` |
| **CAMP_WA_002 Naive Lift** | +17.90% pts | **Derived Metric** | Unadjusted difference in proportions |
| **CAMP_WA_002 Stage-Matched Lift**| +4.48% pts (95% CI: 3.12–5.84%) | **Derived Metric** | Exact stage-matched eligible control group |
| **Airport Terminal Deficit**| 55,053 lost requests | **Observed Fact** | Sum of `unfulfilled_requests` in `airport_hourly.csv` |
| **Nocturnal Shortage Share**| 77.51% (42,673 / 55,053) | **Derived Metric** | Filtered by hour $\in [21, 22, 23, 0, 1, 2]$ |
| **Suburban Night Stranded Rate**| 88.94% (11.06% return rate)| **Derived Metric** | Trip analysis in `airport_trips.csv` |
| **VAHAN Integration Impact**| +75 to +85 approvals/mo | **Scenario Estimate**| 40% fixable recovery × downstream conversion |
| **Forward-Dispatch Recovery**| +15.5k to +20k trips/mo | **Scenario Estimate**| Elasticity model on terminal supply availability |

---

## 🚀 How to Run & Reproduce

### 1. Prerequisites & Environment Setup
```bash
# Clone repository
git clone https://github.com/Surendra571/rapido-captain-acquisition-supply-analysis.git
cd rapido-captain-acquisition-supply-analysis

# Create & activate virtual environment
python -m venv venv
source venv/bin/activate       # On macOS/Linux
# or: venv\Scripts\activate    # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Full Analytics & QA Pipeline
Execute the master pipeline script to process raw CSVs, run invariant checks, generate summary tables, export charts, and verify test suites:
```bash
python run_pipeline.py
```

### 3. Run Automated Unit Tests
Run the 14 automated unit tests verifying schema integrity, sequential funnel logic, and marketplace accounting:
```bash
pytest tests/ -v
```

### 4. Interactive Jupyter Exploration
Launch Jupyter to explore the three notebooks step-by-step:
```bash
jupyter notebook notebooks/
```

### 5. Access Executive Deliverables
- **2-Page Executive Memo**: [`memo/executive_memo.pdf`](memo/executive_memo.pdf)
- **6-Slide Executive Deck**: [`deck/presentation_deck.pdf`](deck/presentation_deck.pdf)
- **30-Question Interview Defense**: [`outputs/interview/three_notebook_interview_defense.md`](outputs/interview/three_notebook_interview_defense.md)

---

## 🎙️ Live Debrief & Interview Defense Guide

During a 30-minute technical debrief, interviewers probe for methodological depth, causal awareness, and business common sense. Full answers to the 30 most difficult questions are available in [`outputs/interview/three_notebook_interview_defense.md`](outputs/interview/three_notebook_interview_defense.md). Below is a summary of the top 3:

### Q1: "Why not scale `CAMP_WA_002` immediately if recipients convert at 28.51% vs 10.61%?"
> **Answer**: Comparing recipients to non-recipients is fatally flawed due to **immortal-time bias**. `CAMP_WA_002` was only triggered for captains who survived DL and RC verification. 100% of treated captains were already at Stage 4+, while the control group includes signups who failed at Stage 1 or 2 before receiving any message. When matched against eligible captains at identical stages, the observational association drops from **+17.90% pts to +4.48% pts**. Furthermore, clickers converted at 28.24% vs 28.70% for non-clickers, proving that link engagement had zero incremental impact. Scaling 5x without an RCT wastes ₹15–20L on passive broadcast templates.

### Q2: "Why reject localized airport driver acquisition if the terminal is short 55k rides?"
> **Answer**: Local acquisition treats the airport as an isolated silo, ignoring network dynamics. **41.07% of airport trips drop in residential suburbs (`SUB-07`, `SUB-11`)**, where the night return-fare probability is only **11.06% (88.94% deadhead rate)**. Drivers who complete an airport trip at midnight get stranded in residential zones and face a 23 km empty return ride, leading to a 24.50% cancellation rate. Adding newly acquired captains near the airport acts like pouring water into a **leaky bucket**—they will complete one trip, get stranded in suburbs, and exit the platform. We must solve return economics and dispatch first.

### Q3: "Why is VAHAN API integration ranked #1 over top-of-funnel acquisition?"
> **Answer**: Funnel economics dictate fixing the widest leaky stage before pouring more paid acquisition into the top. **Stage 3 (RC) accounts for 29.35% of all lifecycle drops (6,102 captains)**, and **63.63% of RC verification failures are mechanical** (camera blur and OCR string mismatches) rather than regulatory ineligibility. This disproportionately punishes captains with budget smartphones (75.6% blur failure rate; 13.42% conversion). Eliminating photo uploads via direct VAHAN registration lookup recovers ~75–85 high-intent captains/month at ~₹1.2L/month—delivering an immediate, highly cost-effective supply boost.

---

## 📄 License & Attribution
Developed for the **Rapido Data Scientist (Intern / Associate) — Captain Acquisition & Supply** take-home assessment. All data is synthetic and formatted to mirror real-world mobility marketplace operations.
