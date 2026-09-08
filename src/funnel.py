"""
Onboarding Funnel analytics module: stage conversion, drop-offs, timing, and vehicle-specific workflows.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional

def compute_captain_doc_pass_matrix(doc_events_df: pd.DataFrame) -> pd.DataFrame:
    """Computes a boolean matrix indicating if a captain has verified each document type."""
    passes = doc_events_df[doc_events_df['event_type'] == 'verification_pass']
    pass_matrix = passes.groupby(['captain_id', 'doc_type']).size().unstack(fill_value=0) > 0
    return pass_matrix

def compute_stage_timing_summary(
    captains_df: pd.DataFrame,
    doc_events_df: pd.DataFrame,
) -> pd.DataFrame:
    """Summarize elapsed days between signup and first document passes."""
    captains = captains_df[['captain_id', 'signup_ts']].copy()
    captains['signup_ts'] = pd.to_datetime(captains['signup_ts'])
    passes = doc_events_df.loc[
        doc_events_df['event_type'].eq('verification_pass'),
        ['captain_id', 'doc_type', 'event_ts'],
    ].copy()
    passes['event_ts'] = pd.to_datetime(passes['event_ts'])
    first_pass = (
        passes.sort_values('event_ts')
        .drop_duplicates(['captain_id', 'doc_type'])
        .pivot(index='captain_id', columns='doc_type', values='event_ts')
    )

    transitions = [
        ('signup_to_dl', 'signup_ts', 'DL'),
        ('dl_to_rc', 'DL', 'RC'),
        ('rc_to_aadhaar', 'RC', 'AADHAAR'),
        ('aadhaar_to_permit', 'AADHAAR', 'PERMIT'),
        ('permit_to_fitness', 'PERMIT', 'FITNESS'),
        ('fitness_to_insurance', 'FITNESS', 'INSURANCE'),
    ]
    rows = []
    for transition, start_field, end_field in transitions:
        start = (
            captains.set_index('captain_id')['signup_ts']
            if start_field == 'signup_ts'
            else first_pass.get(start_field, pd.Series(dtype='datetime64[ns]'))
        )
        end = first_pass.get(end_field, pd.Series(dtype='datetime64[ns]'))
        elapsed = (end - start).dropna().dt.total_seconds() / 86400
        elapsed = elapsed[elapsed.ge(0)]
        if elapsed.empty:
            continue
        rows.append({
            'transition': transition,
            'sample_size': len(elapsed),
            'p25_days': round(elapsed.quantile(0.25), 2),
            'median_days': round(elapsed.median(), 2),
            'p75_days': round(elapsed.quantile(0.75), 2),
        })
    return pd.DataFrame(rows)

def build_onboarding_funnel(
    captains_df: pd.DataFrame,
    doc_events_df: pd.DataFrame,
    approvals_df: pd.DataFrame,
    mature_only: bool = False,
    maturity_cutoff_date: str = "2026-06-15 00:00:00"
) -> pd.DataFrame:
    """
    Constructs the step-by-step onboarding funnel respecting document sequence,
    vehicle-specific Permit exemptions (ERickshaw), and terminal approval outcomes.
    """
    caps = captains_df.copy()
    caps['signup_ts'] = pd.to_datetime(caps['signup_ts'])
    
    if mature_only:
        caps = caps[caps['signup_ts'] < maturity_cutoff_date].copy()
    
    total_signups = len(caps)
    pass_matrix = compute_captain_doc_pass_matrix(doc_events_df)
    
    df = caps.merge(approvals_df, on='captain_id', how='left')
    for dt in ['DL', 'RC', 'AADHAAR', 'PERMIT', 'FITNESS', 'INSURANCE']:
        if dt in pass_matrix.columns:
            df[f'pass_{dt}'] = df['captain_id'].map(pass_matrix[dt]).eq(True)
        else:
            df[f'pass_{dt}'] = False
            
    is_auto_cab = df['vehicle_type'].isin(['Auto', 'Cab'])
    is_erickshaw = df['vehicle_type'] == 'ERickshaw'
    
    s_signup = total_signups
    s_dl = int(df['pass_DL'].sum())
    s_rc = int((df['pass_DL'] & df['pass_RC']).sum())
    s_aadhaar = int((df['pass_DL'] & df['pass_RC'] & df['pass_AADHAAR']).sum())
    
    cond_ac_permit = is_auto_cab & df['pass_DL'] & df['pass_RC'] & df['pass_AADHAAR'] & df['pass_PERMIT']
    cond_er_permit = is_erickshaw & df['pass_DL'] & df['pass_RC'] & df['pass_AADHAAR']
    s_permit_stage = int((cond_ac_permit | cond_er_permit).sum())
    
    cond_ac_fitness = cond_ac_permit & df['pass_FITNESS']
    cond_er_fitness = cond_er_permit & df['pass_FITNESS']
    s_fitness = int((cond_ac_fitness | cond_er_fitness).sum())
    
    cond_ac_ins = cond_ac_fitness & df['pass_INSURANCE']
    cond_er_ins = cond_er_fitness & df['pass_INSURANCE']
    s_insurance = int((cond_ac_ins | cond_er_ins).sum())
    
    # Treat approval as a terminal business outcome, but require the modeled
    # document sequence to be complete before counting it in this funnel.
    s_approved = int(
        (df['final_status'].eq('approved') & df['pass_INSURANCE']).sum()
    )
    
    stages_data = [
        {"Stage": "1. Signup", "Eligible Captains": s_signup, "Completed": s_signup, "Drop": 0},
        {"Stage": "2. Driving Licence (DL)", "Eligible Captains": s_signup, "Completed": s_dl, "Drop": s_signup - s_dl},
        {"Stage": "3. Registration Certificate (RC)", "Eligible Captains": s_dl, "Completed": s_rc, "Drop": s_dl - s_rc},
        {"Stage": "4. Aadhaar", "Eligible Captains": s_rc, "Completed": s_aadhaar, "Drop": s_rc - s_aadhaar},
        {"Stage": "5. Permit (Auto/Cab) / Doc-4 Gate", "Eligible Captains": s_aadhaar, "Completed": s_permit_stage, "Drop": s_aadhaar - s_permit_stage},
        {"Stage": "6. Fitness Certificate", "Eligible Captains": s_permit_stage, "Completed": s_fitness, "Drop": s_permit_stage - s_fitness},
        {"Stage": "7. Insurance (All Docs Cleared)", "Eligible Captains": s_fitness, "Completed": s_insurance, "Drop": s_fitness - s_insurance},
        {"Stage": "8. BG Check & Final Approval", "Eligible Captains": s_insurance, "Completed": s_approved, "Drop": s_insurance - s_approved}
    ]
    
    fdf = pd.DataFrame(stages_data)
    fdf["Stage Conversion (%)"] = (fdf["Completed"] / fdf["Eligible Captains"] * 100).round(2)
    fdf["Cumulative Conversion (%)"] = (fdf["Completed"] / total_signups * 100).round(2)
    
    total_drop = total_signups - s_approved
    fdf["Share of Total Losses (%)"] = (fdf["Drop"] / total_drop * 100).round(2)
    return fdf
