"""
Validation module for schema verification, integrity checks, and data anomaly detection.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any

def audit_dataset_profile(df: pd.DataFrame, name: str, id_col: str = None) -> Dict[str, Any]:
    """Generates structural and quality profile for a single dataframe."""
    profile = {
        "dataset_name": name,
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_counts": df.isnull().sum().to_dict(),
        "missing_percentages": (df.isnull().mean() * 100).round(2).to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
    }
    if id_col and id_col in df.columns:
        profile["id_col"] = id_col
        profile["unique_ids"] = int(df[id_col].nunique())
        profile["duplicate_ids"] = int(df[id_col].duplicated().sum())
    
    # Categorical distributions
    cat_summary = {}
    for col in df.select_dtypes(include=['object', 'category']).columns:
        if df[col].nunique() <= 30:
            cat_summary[col] = df[col].value_counts(dropna=False).to_dict()
    profile["categorical_distributions"] = cat_summary
    
    # Timestamp summaries
    ts_summary = {}
    for col in df.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns:
        valid_ts = df[col].dropna()
        if len(valid_ts) > 0:
            ts_summary[col] = {
                "min": str(valid_ts.min()),
                "max": str(valid_ts.max()),
                "null_count": int(df[col].isnull().sum())
            }
    profile["timestamp_summaries"] = ts_summary
    return profile

def check_referential_integrity(datasets: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """Verifies foreign key relationships and orphaned records across datasets."""
    captains_ids = set(datasets["captains"]["captain_id"])
    
    integrity = {}
    # approvals
    app_ids = set(datasets["approvals"]["captain_id"])
    integrity["approvals_in_captains"] = {
        "total_records": len(datasets["approvals"]),
        "unique_ids": len(app_ids),
        "missing_in_captains": len(app_ids - captains_ids),
        "captains_missing_in_approvals": len(captains_ids - app_ids)
    }
    
    # doc_events
    doc_ids = set(datasets["doc_events"]["captain_id"])
    integrity["doc_events_in_captains"] = {
        "total_records": len(datasets["doc_events"]),
        "unique_ids": len(doc_ids),
        "missing_in_captains": len(doc_ids - captains_ids),
        "captains_without_doc_events": len(captains_ids - doc_ids)
    }
    
    # activation
    act_ids = set(datasets["activation"]["captain_id"])
    approved_ids = set(datasets["approvals"][datasets["approvals"]["final_status"] == "approved"]["captain_id"])
    integrity["activation_in_approvals"] = {
        "total_activation_records": len(datasets["activation"]),
        "unique_act_ids": len(act_ids),
        "act_ids_not_in_approved": len(act_ids - approved_ids),
        "approved_not_in_activation": len(approved_ids - act_ids)
    }
    
    # nudges
    nudge_ids = set(datasets["nudges"]["captain_id"])
    integrity["nudges_in_captains"] = {
        "total_nudge_records": len(datasets["nudges"]),
        "unique_nudge_captains": len(nudge_ids),
        "nudge_captains_missing_in_captains": len(nudge_ids - captains_ids)
    }
    
    # zones
    hourly_zones = set(datasets["airport_hourly"]["zone_id"])
    trip_pickups = set(datasets["airport_trips"]["pickup_zone_id"])
    trip_drops = set(datasets["airport_trips"]["drop_zone_id"])
    integrity["zones"] = {
        "hourly_zones": list(hourly_zones),
        "trip_pickup_zones": list(trip_pickups),
        "trip_pickup_not_in_hourly": list(trip_pickups - hourly_zones),
        "trip_drop_zones_count": len(trip_drops)
    }
    return integrity

def check_chronological_ordering(datasets: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """Inspects chronological integrity: signup <= doc_event <= decision <= first_order."""
    caps = datasets["captains"][["captain_id", "signup_ts"]]
    apps = datasets["approvals"][["captain_id", "decision_ts", "final_status"]]
    acts = datasets["activation"][["captain_id", "first_order_ts"]]
    
    merged = caps.merge(apps, on="captain_id", how="left").merge(acts, on="captain_id", how="left")
    
    # decision before signup
    dec_before_signup = merged[merged["decision_ts"] < merged["signup_ts"]]
    # first order before signup
    order_before_signup = merged[merged["first_order_ts"] < merged["signup_ts"]]
    # first order before decision
    order_before_decision = merged[merged["first_order_ts"] < merged["decision_ts"]]
    
    # doc events before signup
    doc_events = datasets["doc_events"].merge(caps, on="captain_id", how="left")
    doc_before_signup = doc_events[doc_events["event_ts"] < doc_events["signup_ts"]]
    
    # nudges before signup
    nudges = datasets["nudges"].merge(caps, on="captain_id", how="left")
    nudge_before_signup = nudges[nudges["sent_ts"] < nudges["signup_ts"]]
    
    return {
        "decision_before_signup_count": len(dec_before_signup),
        "order_before_signup_count": len(order_before_signup),
        "order_before_decision_count": len(order_before_decision),
        "doc_event_before_signup_count": len(doc_before_signup),
        "nudge_before_signup_count": len(nudge_before_signup)
    }
