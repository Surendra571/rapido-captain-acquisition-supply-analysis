# STRATEGIC BRIEFING: CAPTAIN ONBOARDING CONVERSION & AIRPORT SUPPLY ARCHITECTURE

**TO:** Head of Supply, Rapido  
**FROM:** Senior Data Scientist, Marketplace Strategy  
**DATE:** September 8, 2026  
**SCOPE:** Forensic Analysis of 25,000 Captain Signups and 60,000 Airport Trips (Jan–Jun 2026)  

---

### EXECUTIVE TAKEAWAYS

* **The Onboarding Funnel is Bleeding at Vehicle RC**: Overall onboarding conversion is only **16.82%** (4,206 approved / 25,000 signups). The single largest volume leak is **Registration Certificate (RC) Stage 3**, where **6,102 captains (29.35% of all losses)** drop out—driven primarily by mechanical camera blur and OCR failures (63.63% of RC errors) on low-tier smartphones.
* **The Claimed 17.9% WhatsApp Nudge Lift is Confounded by Selection Bias**: The business claim that campaign `CAMP_WA_002` drove a +17.90% lift is an artifact of immortal-time bias (100.0% of recipients had already survived DL and RC verification). When compared against stage-matched controls, the adjusted observational association is **+4.48% pts (95% CI: +3.12% to +5.84% pts)**, with 0% engagement lift among clickers. **Do not scale budget 5x without a controlled A/B test.**
* **Airport Shortage is a Nocturnal Deadhead Problem, Not an Acquisition Deficit**: The airport marketplace is 96.90% fulfilled during the day, but crashes to **47.20% fulfillment between 21:00 and 03:00** (accounting for 77.51% of unmet demand / 42,673 lost trips/mo). For suburban drops (`SUB-07`, `SUB-11`), return-fare access falls to **11.06% at night**, driving a **24.50% cancellation rate**.
* **Core Strategic Directive**: **Do NOT fund broad airport driver acquisition.** The airport is a leaky bucket exporting drivers into suburbs. Instead, deploy **Direct VAHAN API Auto-Fetch** for RC onboarding, **Run a Controlled RCT on WhatsApp Nudges**, and **Deploy Forward-Dispatch & Suburban Return Subsidies**.

---

### 1. ONBOARDING HEALTH & FUNNEL LEAK DIAGNOSIS

* **Funnel Conversion Reality (A2O & R2A)**: Out of 25,000 signups, 20,789 clear DL (83.16%), 14,687 clear RC (58.75%), 10,854 clear Aadhaar (43.42%), 7,921 pass Permit/Doc-4 (31.68%), 5,612 clear Fitness (22.45%), 4,206 clear Insurance (16.82%), and **4,206 reach Final Approval (16.82% A2O)**. Post-approval activation (R2A) is **85.00%** (3,575 active captains). Among mature cohorts ($>15$ days before extraction), conversion is **17.57%**; all 1,297 in-progress signups are isolated to the final 15 days.
* **The Biggest Volume Loss**: **Stage 3 (Registration Certificate — RC)** loses **6,102 captains (29.35% of all drop-offs)**, making it the primary system constraint.
* **The Most Important Fixable Leak**: 34.82% of captains fail RC verification at least once, and **50.10% abandon immediately after failure**. Root causes are heavily technical: **63.63% of RC errors** stem from blurry photos (39.54%) and OCR name/chassis mismatches (24.09%). This disproportionately hurts **low-tier phone users**, who convert at only **13.42%** (vs 21.81% on high-tier) and suffer 75.6% of blur failures.

---

### 2. CAMPAIGN EVALUATION: `CAMP_WA_002`

* **The Reality Behind the Claim**: `CAMP_WA_002` sent WhatsApp messages to 8,673 captains. While recipients show an unadjusted 28.51% approval rate vs 10.61% for all non-recipients (a naive "+17.90% pt win"), **100.0% of treated captains had ALREADY passed DL and RC** before receiving the message.
* **Stage-Matched Observational Lift**: Comparing treated captains against untreated controls who also cleared DL+RC yields an approval rate of **28.51% vs 24.14%** ($\Delta = \mathbf{+4.37\% 	ext{ pts}}$). Adjusting for city, vehicle, channel, device tier, age, and month via logistic regression yields **+4.48% pts (95% CI: +3.12% to +5.84% pts, p < 0.001)**.
* **Causal Status & Confidence**: This is strictly an **observational association, not causal proof**. Captains who clicked the link converted at **28.24%**, identical to non-clickers (**28.70%**), proving the message acted as passive awareness rather than active friction removal.
* **Decision on 5x Budget Scaling**: **REJECT 5x budget scale.** Do not commit capital to linear broadcast blasts. Instead, execute a 50/50 randomized holdout experiment ($N=3,305/	ext{arm}$) to test an automated 2-way failure-recovery bot.

---

### 3. AIRPORT SUPPLY & MARKETPLACE DYNAMICS

* **When and Where Shortage Occurs**: Undersupply is strictly nocturnal. Daytime (04:00–20:00) is healthy (**96.90% fulfillment**, ETA 3.8 min, Surge 1.05x). The **21:00–03:00 window collapses to 47.20% fulfillment** (26.24% at 23:00), with surge averaging 2.17x and ETAs hitting 10.0 minutes.
* **Magnitude of Deficit**: **42,673 requests go unfulfilled during the night window (77.51% of all unmet airport demand)**, averaging ~710 lost requests per night.
* **Post-Trip Trajectory & The Deadhead Trap**: Airport trips average 17.9 km (₹279 fare). However, **41.07% of trips drop passengers in suburban zones (`SUB-07`, `SUB-11`)**, where the night return-fare rate is only **11.06% (88.94% stranded rate)**. Suburban night cancellations spike to **24.50%** as drivers reject unpaid 30 km return deadheading.
* **Targeted Acquisition Decision**: **NOT RECOMMENDED.** Acquiring drivers around the airport creates a leaky bucket—drivers take suburban trips and are immediately drained from the catchment. We must fix return economics and turnaround speed first.

---

### 4. THREE RANKED STRATEGIC RECOMMENDATIONS

| Rank | Strategic Action | Target Problem | Expected Monthly Impact (Scenario) | Cost & Risk | Primary Success Metric |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **#1** | **Direct VAHAN API Auto-Fetch & Camera Blur Guidance**<br>Replace manual RC photo upload with instant RTO vehicle lookup via Registration Number + OTP; add client-side blur detection. | RC Stage 3 drop-off (6,102 drops; 63.6% blur/OCR failure share). | **+75 to +85 Approved Captains / month** (+450 to +510 over 6 mo). Formula: $3,465 	ext{ DL passers/mo} 	imes 16.82\% \Delta 	ext{pass} 	imes 28.64\% 	ext{ downstream} 	imes 50\% 	ext{ capture}$. | API lookup fee (₹5–8/call); RTO downtime mitigated via manual fallback. | **RC First-Time Pass Rate** ($\ge 82.0\%$, from 65.2%) & **Low-Tier Pass Rate** ($\ge 75\%$). |
| **#2** | **Controlled RCT Experiment on Nudges Before 5x Scaling**<br>Halt broadcast blast; launch 50/50 RCT ($N=3,305/	ext{arm}$) testing an event-driven 2-way WhatsApp failure-resolution bot. | Immortal-time bias in naive claim (+17.9% pts); true lift +4.5% pts; 0% clicker lift. | **Protects ₹15–20L marketing budget**; establishes true causal lift and CAC per incremental active driver. | Opportunity cost of holding out 3,305 captains during 6-week trial. | **14-Day Incremental Approval Lift** ($\ge +3.0\% 	ext{ pts}$, RCT verified; p < 0.05). |
| **#3** | **Airport Forward-Dispatch & Suburban Return Subsidies**<br>Pre-match inbound airport drops 5–7 min before terminal arrival; provide ₹120 return allowance for `SUB-07`/`SUB-11` night drops. | 77.5% nocturnal airport shortage & suburban deadhead trap (88.9% night stranded rate). | **+15,500 to +20,000 Fulfilled Trips / month** (Forward-dispatch: +9k–12k; Return allowance: +6.5k–8k). | ₹120 allowance funded via existing 2.17x night surge pool (net subsidy $\le ₹45/	ext{trip}$). | **Airport Night Fulfillment** ($\ge 70\%$, from 47.2%) & **Suburb Cancels** ($< 10\%$, from 24.5%). |

---

### 5. ASSUMPTIONS & WHAT WOULD CHANGE MY ANSWER

1. **Downstream Conversion Multiplier (28.64%)**: Assumes captains rescued at RC pass downstream stages (Aadhaar $	o$ Insurance) at historical rates. *What changes answer*: If RC-failing drivers possess uninsurable vehicles (downstream pass $<15\%$), net approvals drop to $+44/	ext{mo}$, shifting priority to Insurance FinTech financing.
2. **Suburban Deadheading Elasticity**: Assumes night cancellations (24.50%) are driven by return economics (11.06% return fare rate). *What changes answer*: If cancellations stem from personal driver night-shift curfews rather than fuel economics, return subsidies will have lower elasticity.
3. **Government VAHAN API Uptime**: Assumes $\ge 90\%$ digital coverage across RTO databases in target cities. *What changes answer*: If rural vehicle registration records have high latency, on-device native camera guides become the primary path.
