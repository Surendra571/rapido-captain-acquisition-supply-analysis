"""
Data cleaning and standardized preprocessing module.
"""
import pandas as pd
import numpy as np
from typing import Dict

def clean_captains_data(df: pd.DataFrame) -> pd.DataFrame:
    clean_df = df.copy()
    clean_df['city'] = clean_df['city'].str.strip()
    clean_df['vehicle_type'] = clean_df['vehicle_type'].str.strip()
    clean_df['acquisition_channel'] = clean_df['acquisition_channel'].str.strip()
    clean_df['device_tier'] = clean_df['device_tier'].str.strip().str.lower()
    clean_df['app_language'] = clean_df['app_language'].str.strip().str.lower()
    clean_df['age_band'] = clean_df['age_band'].str.strip()
    return clean_df

def clean_approvals_data(df: pd.DataFrame) -> pd.DataFrame:
    clean_df = df.copy()
    clean_df['final_status'] = clean_df['final_status'].str.strip().str.lower()
    clean_df['last_stage_reached'] = clean_df['last_stage_reached'].str.strip()
    return clean_df

def clean_doc_events_data(df: pd.DataFrame) -> pd.DataFrame:
    clean_df = df.copy()
    clean_df['doc_type'] = clean_df['doc_type'].str.strip().str.upper()
    clean_df['event_type'] = clean_df['event_type'].str.strip().str.lower()
    clean_df['failure_reason'] = clean_df['failure_reason'].str.strip().str.lower()
    return clean_df
