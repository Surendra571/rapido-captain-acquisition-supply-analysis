# RAPIDO CAPTAIN ACQUISITION & AIRPORT SUPPLY STRATEGY
## 6-Slide Executive Presentation for Head of Supply

---

## Slide 1: Executive Summary
### Three Key Findings, Three Ranked Actions, and One Decisive Choice

* **Finding 1 (Onboarding Leak)**: Platform conversion is **16.82%** (4,206 approved / 25,000 signups). The single largest loss is **Registration Certificate (RC) verification** (6,102 drops / 29.35% of total loss), where 63.63% of fails are mechanical image blur/OCR errors on low-tier phones.
* **Finding 2 (Campaign Reality)**: `CAMP_WA_002`'s claimed +17.90% lift is confounded by immortal-time bias (100% of recipients had already survived DL and RC). The adjusted observational association is **+4.48% pts (95% CI: +3.12% to +5.84% pts)**, with zero clicker advantage.
* **Finding 3 (Airport Mismatch)**: Terminal shortage is concentrated at night (**21:00–03:00**, 77.51% of unmet demand / 42,673 lost trips/mo; fulfillment is 47.20%, dropping to 26.24% at 23:00). Suburban return-fare access falls to **11.06% at night**, driving a **24.50% cancellation rate**.
* **The Big Business Decision**: **Do NOT fund broad airport driver acquisition.** Fund **Direct VAHAN Government API Auto-Fetch**, **A Controlled RCT on WhatsApp Nudges**, and **Airport Forward-Dispatch & Suburban Return Subsidies**.

---

## Slide 2: Onboarding Funnel
### 16.82% End-to-End Conversion: RC Verification is the Primary Drop-off Gate

* **Funnel Summary**:
  * 1. Signup: 25,000 (100.0%)
  * 2. Driving Licence (DL): 20,789 (83.16% | -4,211 drop)
  * 3. **Registration Certificate (RC): 14,687 (58.75% | -6,102 drop / 29.35% loss share)**
  * 4. Aadhaar: 10,854 (43.42% | -3,833 drop)
  * 5. Permit / Doc-4 Gate: 7,921 (31.68% | -2,933 drop)
  * 6. Fitness: 5,612 (22.45% | -2,309 drop)
  * 7. Insurance: 4,206 (16.82% | -1,406 drop)
  * 8. **Approved: 4,206 (16.82% A2O | 3,575 Activated / 85.00% R2A)**
* **Takeaway**: Stage 3 (RC) loses 6,102 drivers—more than any other document stage.
* **Cohort Maturity**: Among mature cohorts ($>15$ days before extraction), conversion is **17.57%**; all 1,297 in-progress signups are isolated to the final 15 days.

---

## Slide 3: Biggest Fixable Leak
### RC Verification Friction: 63.63% of Failures are Fixable Image Blur & OCR Errors

* **Target Population**: 20,789 captains attempting RC (9,842 on low-tier devices).
* **The Evidence**:
  * 34.82% failure rate on RC verification.
  * 50.10% of failed drivers abandon onboarding immediately after failure.
  * 63.63% of failures are fixable: Blurry photo (39.54%), OCR name/chassis mismatch (24.09%).
  * Low-tier device users convert at only 13.42% (vs 21.81% high-tier) and suffer 75.6% of all blur errors.
* **Why Actionable**: Direct VAHAN / DigiLocker API integration bypasses photo capture entirely via Vehicle Registration Number + OTP.
* **Opportunity**: **+75 to +85 approved captains / month** (+450 to +510 over 6 mo), calculated as $3,465 	ext{ DL passers/mo} 	imes 16.82\% \Delta 	ext{pass} 	imes 28.64\% 	ext{ downstream} 	imes 50\% 	ext{ capture}$.

---

## Slide 4: Campaign `CAMP_WA_002`
### Claimed +17.9% Lift is Confounded: Observational Association is +4.5% pts

* **The Fatal Bias**: 100.0% of treated drivers had ALREADY survived DL & RC before the nudge was sent.
* **Multi-Tier Statistical Reality**:
  * 1. Naive Business Claim: +17.90% pts (Fatally flawed by immortal-time survival bias).
  * 2. Demographic-Adjusted (Full Base): +15.10% pts (Fails to adjust for stage timing).
  * 3. **Stage-Matched Comparison (DL+RC Cleared): +4.37% pts** (28.51% vs 24.14%).
  * 4. **Adjusted Observational Association: +4.48% pts (95% CI: +3.12% to +5.84% pts, p < 0.001)**.
* **Clicker Analysis**: Clickers converted at **28.24%** vs **28.70%** for non-clickers, confirming passive awareness.
* **Decision**: **REJECT 5x budget scaling.** Execute a 50/50 RCT ($N=3,305/	ext{arm}$) testing an automated 2-way failure-recovery bot before committing marketing budget.

---

## Slide 5: Airport Supply Dynamics
### 77.51% of Deficit is Nocturnal: Suburban Deadhead Risk Drives Driver Supply Avoidance

* **Temporal Shortage (21:00–03:00)**:
  * The night window contains **42,673 unmet requests**, or **77.51%** of all monthly unmet airport demand.
  * Fulfillment is **47.20% overall** in the window; 23:00 is the worst hour at **26.24%**, with surge at 2.17x and ETAs at 10.0 min.
  * Daytime (04:00–20:00) is already 96.90% fulfilled; daytime acquisition is completely redundant.
* **The Suburban Deadhead Trap**:
  * 41.07% of airport trips drop in residential suburbs (`SUB-07`, `SUB-11`).
  * Suburban return-fare access is **11.06% at night (88.94% stranded rate)**.
  * Drivers rationally avoid suburban trips, driving night cancellations to **24.50%** (vs 11.20% for CBD drops).

---

## Slide 6: Decision & Action Plan
### Do NOT Acquire Local Drivers; Fund VAHAN API, Campaign RCT, and Airport Rebalancing

* **Strategic Choice**: Local acquisition creates a "leaky bucket" (drivers exported to suburbs on trip 1).
* **Three Ranked Actions**:
  1. **#1. VAHAN API Auto-Fetch & On-Device Blur Guidance**: +75 to +85 approved captains/mo (+450 to +510 over 6 mo). Primary Metric: RC Pass Rate $\ge 82\%$.
  2. **#2. Controlled RCT Experiment Before 5x Nudge Scaling**: 50/50 A/B trial ($N=3,305/	ext{arm}$) testing 2-way bot; protects ₹15–20L budget. Primary Metric: Incremental 14-day lift $\ge +3.0\%$ pts.
  3. **#3. Airport Forward-Dispatch & Suburban Return Subsidies**: +15,500 to +20,000 fulfilled trips/mo scenario (Forward-dispatch: +9k–12k; Return allowance: +6.5k–8k). Primary Metric: Night Fulfillment $\ge 70\%$, Suburb Cancels $< 10\%$.
* **Measurement Plan**: 4-week controlled rollout with daily SLA, cancellation, and unit economics telemetry.
