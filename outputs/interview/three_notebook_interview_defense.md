# 🎙️ Three-Notebook Technical Interview Defense Guide
### 30 Forensically Answered Questions Across Data Audit, Onboarding Funnel, and Airport Supply

---

## SECTION 1: DATA AUDIT & QUALITY (NOTEBOOK 1)

### Q1: Why did you trust this data? Did you take the raw CSV files at face value?
- **Answer**: I did not take them at face value. I constructed a 16-point invariant audit in `src/validation.py` verifying: (1) 0 duplicate IDs across primary entities; (2) 0 chronological inversions; (3) 100% accounting balance in hourly requests ($requests \equiv fulfilled + unfulfilled$); and (4) 0 orphan IDs across all downstream tables.
- **Numbers**: 0 missing IDs; 0 timestamp inversions; 0 balance errors across 10,248 hourly rows.

### Q2: What subtle data quality issues did you find in `doc_events.csv`?
- **Answer**: `upload_success` and `verification_pass` are decoupled. An upload only records a file receipt, whereas 34.82% of RC uploads fail verification. Additionally, retries occur up to 3 attempts (162.2k Attempt 1, 21.9k Attempt 2, 2.2k Attempt 3).
- **Numbers**: 186,282 total document events; max attempt_no strictly $\le 3$.

### Q3: Did you exclude any records from the analysis?
- **Answer**: No rows were deleted. However, I segmented the base into **all signups ($N=25,000$)** and **mature cohorts ($N=22,407$)** signed up before June 15, 2026. This prevents right-censoring bias from active in-progress captains.
- **Numbers**: 1,297 in-progress signups strictly isolated to $\ge$ June 15; mature cohort converts at 17.57% vs 16.82% overall.

### Q4: How did you handle timezones? Are you sure there is no UTC vs IST offset?
- **Answer**: The metadata defines a cutoff of `2026-06-30 23:59:00 IST`. All timestamps were explicitly parsed in Indian Standard Time (`Asia/Kolkata`, UTC+05:30). If parsed in UTC, peak demand hours shift by +5.5 hours into morning commute hours, corrupting the diagnosis.
- **Numbers**: Consistent 2026-01-01 to 2026-06-30 IST span.

### Q5: How did you verify referential integrity between `activation.csv` and `approvals.csv`?
- **Answer**: I joined on `captain_id` and verified that 100% of activated captains exist in the approved set, and that for every record, $first\_order\_ts \ge decision\_ts$.
- **Numbers**: 4,206 approved captains $\to$ 3,575 activated captains (85.00% post-approval activation rate).

### Q6: What did you discover about vehicle-specific document requirements?
- **Answer**: ERickshaw captains ($N=4,756$) have exactly 0 `PERMIT` events in `doc_events.csv` because commercial permits legally apply only to Auto and Cab.
- **Numbers**: ERickshaws require 5 documents; Auto/Cab require 6 documents. ERickshaws convert at 22.73% vs 15.30% for Auto.

### Q7: Are there any orphan records in `nudges.csv`?
- **Answer**: Zero orphan records. All 16,314 nudges map to valid `captain_id` records in `captains.csv`.
- **Numbers**: 16,314 nudges across 13,667 unique captains.

### Q8: What is the average time to complete onboarding?
- **Answer**: Mean onboarding completion time is **6.42 days** (P25 = 2.1 days, Median = 5.4 days, P99 = 14.1 days).
- **Numbers**: 99% of captains who convert do so within 14 days.

### Q9: Does `airport_trips.csv` contain driver identifiers?
- **Answer**: No. `airport_trips.csv` contains `trip_id` but **NO `captain_id`**. This is a critical data constraint: B2 must remain a trip-level economic analysis.
- **Numbers**: 60,000 trip-level records.

### Q10: How did you verify hourly marketplace market-clearing?
- **Answer**: I verified that $requests \equiv fulfilled\_requests + unfulfilled\_requests$ across all 10,248 rows in `airport_hourly.csv`.
- **Numbers**: 0 accounting discrepancy rows.

---

## SECTION 2: ONBOARDING FUNNEL & CAMPAIGN (NOTEBOOK 2)

### Q11: What is the top-of-funnel conversion rate and denominator?
- **Answer**: Overall conversion (A2O) is **16.82%** (4,206 / 25,000). The denominator is all created captain accounts, because acquisition marketing costs are incurred at signup.
- **Numbers**: 25,000 signups $\to$ 4,206 approved (16.82%); 3,575 activated (85.00% R2A).

### Q12: Why is Registration Certificate (RC) the biggest fixable leak over DL?
- **Answer**: RC drops **6,102 captains (29.35% of all lifecycle losses)** vs 4,211 at DL. 63.63% of RC failures are mechanical camera blur or OCR name/chassis mismatches on low-tier phones, solvable via VAHAN API auto-fetch.
- **Numbers**: RC Step Conversion: 70.65% (14,687 / 20,789); 50.10% fail abandonment rate.

### Q13: What is the device-tier disparity at the RC stage?
- **Answer**: Captains on low-tier Android phones achieve an overall conversion of only **13.42%** (vs 21.81% on high-tier) and account for **75.6% of all camera blur failures**.
- **Numbers**: Low-tier signups: $N=9,842$, Approved: 1,321 (13.42%).

### Q14: Why is the naive +17.90% pt campaign claim invalid?
- **Answer**: It suffers from **immortal-time selection bias**. 100.0% of `CAMP_WA_002` recipients had already survived DL and RC stages before receiving the nudge. Comparing them to raw signups compares survivors against dropouts.
- **Numbers**: Treated DL+RC pre-nudge pass rate: 100.0%; Control full base pass rate: 44.0%.

### Q15: What is the true stage-matched observational lift of `CAMP_WA_002`?
- **Answer**: When evaluated against captains who also cleared DL+RC, treated conversion is **28.51% vs 24.14%** ($\Delta = +4.37\% \text{ pts}$). Logistic regression adjusting for demographics yields **+4.48% pts (95% CI: +3.12% to +5.84% pts)**.
- **Numbers**: Treated N = 8,673; Control N = 7,179; p < 0.001.

### Q16: What did the complier/clicker analysis reveal?
- **Answer**: Captains who clicked the WhatsApp link converted at **28.24%** vs **28.70%** for non-clickers ($p = 0.635$). The link provided zero functional utility; the message acted purely as passive awareness.
- **Numbers**: Clickers: 3,569; Non-clickers: 5,104.

### Q17: Should Rapido scale `CAMP_WA_002` budget by 5x?
- **Answer**: **NO. (TEST BEFORE SCALING).** A 5x broadcast budget would waste marketing capital on drivers already self-completing without solving physical document rejections.
- **Numbers**: Unit yield: ~38 incremental active drivers per 1,000 nudges.

### Q18: What experiment would you run before scaling?
- **Answer**: A 50/50 randomized controlled trial ($N=3,305/\text{arm}$) testing an automated 2-way failure-resolution WhatsApp bot against a holdout control.
- **Numbers**: Sample size: 3,305 per arm (6,610 total) for MDE = +3.0% pts at $\alpha=0.05, 80\%$ power.

### Q19: Show the mathematical formula for +75 to +85 approved captains/month.
- **Answer**: $3,465 \text{ DL passers/mo} \times 16.82\% \Delta\text{pass} \times 28.64\% \text{ downstream} \times 50\% \text{ capture} = \mathbf{83.5 \approx 75\text{--}85/\text{mo}}$.
- **Numbers**: 3,465 monthly DL passers; 28.64% downstream multiplier; 50% realization discount.

### Q20: What are your top 3 ranked recommendations?
- **Answer**: (1) Direct VAHAN API Auto-Fetch (+75–85 caps/mo); (2) Controlled CRM RCT (protects ₹15–20L budget); (3) Airport Forward-Dispatch & Suburban Return Subsidies (+15.5k–20k trips/mo).
- **Numbers**: 3 distinct, ranked interventions with explicit guardrail metrics.

---

## SECTION 3: AIRPORT MARKETPLACE & SUPPLY (NOTEBOOK 3)

### Q21: When and how large is the airport demand-supply mismatch?
- **Answer**: The shortage is **77.51% nocturnal (21:00–03:00)**, accounting for **42,673 unfulfilled trips/month** (out of 55,053 total). Daytime (04:00–20:00) is **96.90% fulfilled**.
- **Numbers**: Night fulfillment: 47.20% (26.24% at 23:00); Surge: 2.17x; ETA: 10.0 min.

### Q22: Why is broad airport driver acquisition rejected?
- **Answer**: The airport is an open network / leaky bucket. **41.07% of trips drop in suburbs (`SUB-07`, `SUB-11`)**, where the night return-fare rate is only **11.06% (88.94% stranded rate)**. Acquired drivers take suburban trips and are immediately drained from the catchment.
- **Numbers**: Daytime fulfillment is already 96.90%; suburb night deadhead is 88.94%.

### Q23: What does `airport_trips.csv` reveal about captain cancellations?
- **Answer**: Cancellations are a rational response to deadhead risk. For Commercial Center drops, cancellations are **11.20%** (74.12% return fare). For Suburban drops, cancellations spike to **21.00% (24.50% at night)**.
- **Numbers**: Commercial Center return: 74.12%, Cancels: 11.20%; Suburb return: 16.53% (11.06% night), Cancels: 24.50% night.

### Q24: How does Forward-Dispatch work without acquiring new drivers?
- **Answer**: It pre-matches inbound city-to-airport drivers 5–7 minutes before terminal drop-off with departing passengers at Arrivals, cutting terminal idle turnaround from 42 min to $<8$ min.
- **Numbers**: Unlocks **+9,000 to +12,000 fulfilled trips/month** at zero CAC.

### Q25: How does the Suburban Return Allowance prevent deadheading?
- **Answer**: It provides a ₹120 allowance for drops in `SUB-07` and `SUB-11` between 21:00 and 03:00 conditional on remaining online for 30 minutes. Funded via existing 2.17x nocturnal surge margins.
- **Numbers**: Unlocks **+6,500 to +8,000 fulfilled trips/month**; net subsidy outlay $\le ₹45/\text{trip}$.

### Q26: Does `airport_trips.csv` track individual drivers over time?
- **Answer**: No. It contains `trip_id` but no `captain_id`. It proves trip-level economics and destination cross-tabulations, not individual driver multi-day shifts.
- **Numbers**: 60,000 trip-level records.

### Q27: What is the total unlock from the airport rebalancing strategy?
- **Answer**: **+15,500 to +20,000 fulfilled trips / month** (Forward-Dispatch: +9k–12k; Return Subsidies: +6.5k–8k).
- **Numbers**: Recovers 35–45% of observed night unmet demand.

### Q28: What would make you reverse your decision on airport acquisition?
- **Answer**: (1) If daytime fulfillment drops below 80% (currently 96.90%); (2) If suburban organic return-fare density matures above 60% (currently 11.06% at night).
- **Numbers**: Daytime fulfillment: 96.90%; Night suburb return rate: 11.06%.

### Q29: What guardrail metrics will you monitor for the airport interventions?
- **Answer**: Inbound forward-match cancellation rate $<6.0\%$; net subsidy outlay $\le ₹45/\text{trip}$; passenger ETA $<5.5$ min.
- **Numbers**: Baseline night ETA: 10.0 min; Baseline night cancellations: 24.50%.

### Q30: What is your rollout plan for Monday morning?
- **Answer**: (1) Deploy client-side blur camera overlay; (2) Initiate VAHAN API vendor contract; (3) Launch 50/50 RCT on 2-way failure bot; (4) Configure nocturnal suburban return guarantees in dispatch engine.
- **Numbers**: Low-tier blur failure share: 75.6%; Night airport shortage: 42.7k trips/mo.
