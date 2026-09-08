"""
Campaign evaluation module: Causal inference, selection bias correction, 
and observational matching for CAMP_WA_002.
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats
from typing import Dict, Any, List

def compute_campaign_balance_table(
    eligible_df: pd.DataFrame,
    covariates: List[str] = ['city', 'vehicle_type', 'acquisition_channel', 'device_tier', 'age_band']
) -> pd.DataFrame:
    """
    Computes a baseline covariate balance table between treated and untreated 
    captains in the eligible cohort (cleared DL and RC).
    Calculates percentage distribution and Standardized Mean Differences (SMDs).
    """
    rows = []
    treated = eligible_df[eligible_df['treated_wa_002'] == 1]
    control = eligible_df[eligible_df['treated_wa_002'] == 0]
    
    for cov in covariates:
        unique_vals = sorted(eligible_df[cov].dropna().unique())
        for val in unique_vals:
            t_pct = (treated[cov] == val).mean() * 100
            c_pct = (control[cov] == val).mean() * 100
            p_t = t_pct / 100
            p_c = c_pct / 100
            pooled_var = (p_t * (1 - p_t) + p_c * (1 - p_c)) / 2
            smd = (p_t - p_c) / np.sqrt(pooled_var) if pooled_var > 0 else 0.0
            
            rows.append({
                "Covariate": cov,
                "Category": str(val),
                "Treated N": int((treated[cov] == val).sum()),
                "Treated (%)": round(t_pct, 1),
                "Control N": int((control[cov] == val).sum()),
                "Control (%)": round(c_pct, 1),
                "Standardized Mean Difference (SMD)": round(smd, 3)
            })
            
    return pd.DataFrame(rows)

def evaluate_camp_wa_002_rigorous(
    captains_df: pd.DataFrame,
    doc_events_df: pd.DataFrame,
    approvals_df: pd.DataFrame,
    nudges_df: pd.DataFrame
) -> Dict[str, Any]:
    """
    Performs a multi-tier observational evaluation of CAMP_WA_002:
    1. Naive unadjusted comparison (exposing immortal-time selection bias)
    2. Stage-matched eligible-control comparison (cleared DL & RC)
    3. Fully adjusted logistic regression controlling for demographics, vehicle, channel, & month
    4. 14-Day outcome window analysis from index date
    5. Baseline balance table with SMDs
    6. Power and sample size calculation for a proposed RCT
    
    IMPORTANT: This is strictly an observational association and NOT a causal claim.
    """
    # 1. Map document pass events
    doc_pass_events = doc_events_df.loc[
        doc_events_df['event_type'].eq('verification_pass')
    ].copy()
    doc_pass_events['event_ts'] = pd.to_datetime(doc_pass_events['event_ts'])
    first_passes = (
        doc_pass_events.sort_values('event_ts')
        .drop_duplicates(['captain_id', 'doc_type'])
        .pivot(index='captain_id', columns='doc_type', values='event_ts')
    )
    
    # 2. Merge baseline attributes
    df = captains_df.copy().merge(approvals_df, on='captain_id', how='left')
    df['signup_ts'] = pd.to_datetime(df['signup_ts'])
    df['decision_ts'] = pd.to_datetime(df['decision_ts'])
    df['dl_ts'] = df['captain_id'].map(first_passes.get('DL'))
    df['rc_ts'] = df['captain_id'].map(first_passes.get('RC'))
    df['insurance_ts'] = df['captain_id'].map(first_passes.get('INSURANCE'))
    
    # Eligibility: cleared both DL and RC
    df['cleared_dl_and_rc'] = df['dl_ts'].notna() & df['rc_ts'].notna()
    df['eligible_ts'] = df[['dl_ts', 'rc_ts']].max(axis=1)
    
    # 3. Campaign treatment mapping
    wa2 = nudges_df[nudges_df['campaign_id'] == 'CAMP_WA_002'].copy()
    wa2['sent_ts'] = pd.to_datetime(wa2['sent_ts'])
    first_wa2_send = wa2.groupby('captain_id')['sent_ts'].min()
    wa2_clicked = set(wa2[wa2['clicked'] == 1]['captain_id'])
    
    df['wa2_sent_ts'] = df['captain_id'].map(first_wa2_send)
    df['treated_wa_002'] = df['wa2_sent_ts'].notna().astype(int)
    df['clicked_wa_002'] = df['captain_id'].isin(wa2_clicked).astype(int)
    df['approved'] = (df['final_status'] == 'approved').astype(int)
    df['signup_month'] = df['signup_ts'].dt.month.astype(str)
    
    # 4. Pre-treatment timing audit
    treated_subset = df[df['treated_wa_002'] == 1].copy()
    treated_pre_dl_rc = (
        (treated_subset['dl_ts'] <= treated_subset['wa2_sent_ts']) &
        (treated_subset['rc_ts'] <= treated_subset['wa2_sent_ts'])
    ).mean() * 100
    
    # 5. Eligible population analysis (cleared DL & RC)
    el_df = df[df['cleared_dl_and_rc']].copy()
    
    # Index date for 14-day outcome window:
    # Treated: wa2_sent_ts. Control: eligible_ts (moment of passing DL+RC)
    el_df['index_ts'] = np.where(
        el_df['treated_wa_002'] == 1,
        el_df['wa2_sent_ts'],
        el_df['eligible_ts']
    )
    el_df['index_ts'] = pd.to_datetime(el_df['index_ts'])
    
    horizon = pd.Timedelta(days=14)
    el_df['approved_14d'] = (
        el_df['approved'].eq(1) &
        el_df['decision_ts'].gt(el_df['index_ts']) &
        el_df['decision_ts'].le(el_df['index_ts'] + horizon)
    ).astype(int)
    
    # 6. Baseline balance table
    balance_table = compute_campaign_balance_table(el_df)
    
    # 7. Logistic regression on eligible cohort
    m = smf.logit(
        'approved ~ treated_wa_002 + C(acquisition_channel) + C(vehicle_type) + C(device_tier) + C(city) + C(app_language) + C(age_band) + C(signup_month)',
        data=el_df
    ).fit(disp=False)
    ame = m.get_margeff(at='overall')
    idx = list(m.params.index[1:]).index('treated_wa_002')
    
    # 8. Unadjusted & Matched Approval Rates
    t_rate_terminal = el_df[el_df['treated_wa_002'] == 1]['approved'].mean() * 100
    c_rate_terminal = el_df[el_df['treated_wa_002'] == 0]['approved'].mean() * 100
    stage_matched_lift = t_rate_terminal - c_rate_terminal
    
    t_rate_14d = el_df[el_df['treated_wa_002'] == 1]['approved_14d'].mean() * 100
    c_rate_14d = el_df[el_df['treated_wa_002'] == 0]['approved_14d'].mean() * 100
    lift_14d = t_rate_14d - c_rate_14d
    
    se_terminal = np.sqrt(
        (t_rate_terminal * (100 - t_rate_terminal) / len(el_df[el_df['treated_wa_002'] == 1])) +
        (c_rate_terminal * (100 - c_rate_terminal) / len(el_df[el_df['treated_wa_002'] == 0]))
    )
    
    # 9. RCT Power & Sample Size Calculation
    p0 = c_rate_terminal / 100
    mde = 0.03
    z_alpha = 1.96
    z_beta = 0.84
    p1 = p0 + mde
    n_per_arm = int(
        np.ceil(
            ((z_alpha + z_beta) ** 2 * (p0 * (1 - p0) + p1 * (1 - p1))) / (mde ** 2)
        )
    )
    
    time_aligned_summary = {
        'treated_n': int(len(el_df[el_df['treated_wa_002'] == 1])),
        'control_n': int(len(el_df[el_df['treated_wa_002'] == 0])),
        'treated_approved': int(el_df[el_df['treated_wa_002'] == 1]['approved_14d'].sum()),
        'control_approved': int(el_df[el_df['treated_wa_002'] == 0]['approved_14d'].sum()),
        'treated_rate_pct': round(t_rate_14d, 2),
        'control_rate_pct': round(c_rate_14d, 2),
        'lift_pct_points': round(lift_14d, 2),
        'outcome_horizon_days': 14,
        'uncertainty_note': 'Observational association with 14-day outcome horizon; randomized holdout required before scaling.'
    }
    
    return {
        "treated_n": int(len(el_df[el_df['treated_wa_002'] == 1])),
        "control_n": int(len(el_df[el_df['treated_wa_002'] == 0])),
        "treated_rate_pct": round(t_rate_terminal, 2),
        "control_rate_pct": round(c_rate_terminal, 2),
        "stage_matched_lift_pct_pts": round(stage_matched_lift, 2),
        "stage_matched_ci": [round(stage_matched_lift - 1.96 * se_terminal, 2), round(stage_matched_lift + 1.96 * se_terminal, 2)],
        "adjusted_observational_lift_pct_pts": round(ame.margeff[idx] * 100, 2),
        "adjusted_ci": [round(ame.conf_int()[idx][0] * 100, 2), round(ame.conf_int()[idx][1] * 100, 2)],
        "p_value": float(ame.pvalues[idx]),
        "treated_14d_rate_pct": round(t_rate_14d, 2),
        "control_14d_rate_pct": round(c_rate_14d, 2),
        "lift_14d_pct_pts": round(lift_14d, 2),
        "naive_lift_pct_pts": round((df[df['treated_wa_002'] == 1]['approved'].mean() - df[df['treated_wa_002'] == 0]['approved'].mean()) * 100, 2),
        "treated_pre_nudge_dl_rc_rate_pct": round(treated_pre_dl_rc, 2),
        "timing_audit": "Treated-stage eligibility is measured before first campaign send; control timing remains unaligned in observational data.",
        "time_aligned_risk_set": time_aligned_summary,
        "click_approval_rate_pct": round(el_df[el_df['clicked_wa_002'] == 1]['approved'].mean() * 100, 2),
        "non_click_approval_rate_pct": round(el_df[(el_df['treated_wa_002'] == 1) & (el_df['clicked_wa_002'] == 0)]['approved'].mean() * 100, 2),
        "balance_table": balance_table,
        "rct_sample_size_per_arm": n_per_arm,
        "rct_total_sample_size": n_per_arm * 2,
        "causal_label": "Observational association — not causal."
    }
