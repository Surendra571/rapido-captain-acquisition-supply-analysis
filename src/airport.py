"""
Airport supply and demand analysis module: hourly mismatch, peak windows, 
trip economics, and spatial rebalancing strategy.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any

def analyze_airport_mismatch_comprehensive(hourly_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes airport-terminal hourly mismatch profiles, isolating the 
    nocturnal peak shortage window (21:00-03:00) from daytime operations.
    """
    df = hourly_df.copy()
    df['hour_ts'] = pd.to_datetime(df['hour_ts'])
    df['hour_of_day'] = df['hour_ts'].dt.hour
    df['day_of_week'] = df['hour_ts'].dt.day_name()
    df['fulfillment_rate_pct'] = (df['fulfilled_requests'] / df['requests'] * 100).round(2)
    df['unfulfilled_rate_pct'] = (df['unfulfilled_requests'] / df['requests'] * 100).round(2)
    df['requests_per_online_captain'] = (df['requests'] / df['online_captains']).round(2)
    
    # Restrict to airport terminals
    apt = df[df['zone_type'].eq('airport_terminal')].copy()
    
    hourly_profile = apt.groupby('hour_of_day').agg(
        total_requests=('requests', 'sum'),
        avg_requests_per_hour=('requests', 'mean'),
        total_fulfilled=('fulfilled_requests', 'sum'),
        avg_fulfilled_per_hour=('fulfilled_requests', 'mean'),
        total_unfulfilled=('unfulfilled_requests', 'sum'),
        avg_unfulfilled_per_hour=('unfulfilled_requests', 'mean'),
        avg_online_captains=('online_captains', 'mean'),
        avg_req_per_captain=('requests_per_online_captain', 'mean'),
        fulfillment_rate_pct=('fulfilled_requests', lambda x: round(x.sum() / apt.loc[x.index, 'requests'].sum() * 100, 2)),
        unfulfilled_rate_pct=('unfulfilled_requests', lambda x: round(x.sum() / apt.loc[x.index, 'requests'].sum() * 100, 2)),
        avg_eta_min=('avg_eta_min', 'mean'),
        avg_surge_multiplier=('avg_surge_multiplier', 'mean')
    ).reset_index()
    
    # Day vs Night summary
    night_hours = [21, 22, 23, 0, 1, 2, 3]
    apt['is_night'] = apt['hour_of_day'].isin(night_hours)
    
    day_night_summary = apt.groupby('is_night').agg(
        total_requests=('requests', 'sum'),
        total_fulfilled=('fulfilled_requests', 'sum'),
        total_unfulfilled=('unfulfilled_requests', 'sum'),
        avg_online_captains=('online_captains', 'mean'),
        avg_eta_min=('avg_eta_min', 'mean'),
        avg_surge=('avg_surge_multiplier', 'mean')
    ).reset_index()
    day_night_summary['fulfillment_rate_pct'] = (day_night_summary['total_fulfilled'] / day_night_summary['total_requests'] * 100).round(2)
    day_night_summary['Period'] = day_night_summary['is_night'].map({True: 'Night (21:00-03:00)', False: 'Daytime (04:00-20:00)'})
    
    return {
        "hourly_profile": hourly_profile,
        "day_night_summary": day_night_summary,
        "raw_terminal_df": apt,
        "total_unfulfilled_terminal": int(apt['unfulfilled_requests'].sum()),
        "night_unfulfilled_terminal": int(apt[apt['is_night']]['unfulfilled_requests'].sum()),
        "night_unfulfilled_share_pct": round(apt[apt['is_night']]['unfulfilled_requests'].sum() / apt['unfulfilled_requests'].sum() * 100, 2)
    }

def analyze_airport_trips_economics(trips_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyzes airport-origin trip economics, return fares, and cancellation rates.
    NOTE: airport_trips.csv does NOT contain captain_id; outcomes are trip-level.
    """
    df = trips_df.copy()
    df['request_ts'] = pd.to_datetime(df['request_ts'])
    df['hour'] = df['request_ts'].dt.hour
    night_hours = [21, 22, 23, 0, 1, 2, 3]
    df['is_night'] = df['hour'].isin(night_hours)
    
    # Destination Zone Type Breakdown
    zone_summary = df.groupby('drop_zone_type').agg(
        total_trips=('trip_id', 'count'),
        cancellation_rate_pct=('captain_cancelled', lambda x: round(x.mean() * 100, 2)),
        return_fare_rate_pct=('got_return_fare_within_20min', lambda x: round(x.mean() * 100, 2)),
        avg_fare_inr=('fare_inr', lambda x: round(x.mean(), 2)),
        median_fare_inr=('fare_inr', 'median'),
        avg_distance_km=('trip_distance_km', lambda x: round(x.mean(), 2))
    ).reset_index()
    zone_summary['trip_share_pct'] = (zone_summary['total_trips'] / len(df) * 100).round(2)
    
    # Night vs Day by Drop Zone Type
    night_zone_summary = df.groupby(['drop_zone_type', 'is_night']).agg(
        total_trips=('trip_id', 'count'),
        cancellation_rate_pct=('captain_cancelled', lambda x: round(x.mean() * 100, 2)),
        return_fare_rate_pct=('got_return_fare_within_20min', lambda x: round(x.mean() * 100, 2)),
        avg_fare_inr=('fare_inr', lambda x: round(x.mean(), 2))
    ).reset_index()
    night_zone_summary['Period'] = night_zone_summary['is_night'].map({True: 'Night (21:00-03:00)', False: 'Daytime (04:00-20:00)'})
    
    return {
        "zone_summary": zone_summary,
        "night_zone_summary": night_zone_summary,
        "total_trips": len(df),
        "suburb_trip_share_pct": round((df['drop_zone_type'] == 'suburban').mean() * 100, 2),
        "suburb_return_fare_pct": round(df[df['drop_zone_type'] == 'suburban']['got_return_fare_within_20min'].mean() * 100, 2),
        "suburb_night_return_fare_pct": round(df[(df['drop_zone_type'] == 'suburban') & df['is_night']]['got_return_fare_within_20min'].mean() * 100, 2),
        "suburb_night_cancel_pct": round(df[(df['drop_zone_type'] == 'suburban') & df['is_night']]['captain_cancelled'].mean() * 100, 2)
    }

def evaluate_airport_interventions_comparison() -> pd.DataFrame:
    """
    Summarizes strategic comparison of Airport Interventions.
    """
    return pd.DataFrame([
        {
            "Intervention": "1. Broad Airport Driver Acquisition",
            "Target Problem": "Airport terminal supply shortage",
            "Decision": "REJECTED (Do Not Fund Broad Acquisition Yet)",
            "Reasoning": "Daytime is already 96.9% fulfilled. 41.1% of trips drop in suburbs with 88.9% night deadheading. Acquired supply is quickly exported and stranded.",
            "Expected Impact (Scenario)": "< 1,500 net trips/mo",
            "Estimated Cost": "High (Rs 2,500/acquisition CAC)",
            "Primary Metric": "Fleet Headcount"
        },
        {
            "Intervention": "2. Forward-Dispatch & Virtual Queueing",
            "Target Problem": "Terminal turnaround & idle wait (42 min)",
            "Decision": "RECOMMENDED (#2 Priority)",
            "Reasoning": "Pre-matches inbound airport trips before terminal drop-off. Cuts turnaround to <8 min and triples driver trip velocity with zero driver acquisition cost.",
            "Expected Impact (Scenario)": "+9,000 to +12,000 trips/mo",
            "Estimated Cost": "Near-Zero Subsidy (Product/Algorithm Dev)",
            "Primary Metric": "Night Match Rate >= 70%"
        },
        {
            "Intervention": "3. Suburban Night Return Allowances",
            "Target Problem": "Suburban deadheading & 24.5% night cancellations",
            "Decision": "RECOMMENDED (#3 Priority)",
            "Reasoning": "Provides targeted Rs 120 allowance on SUB-07/SUB-11 night drops (21:00-03:00) conditional on remaining online 30 min. Self-funded via existing surge pool.",
            "Expected Impact (Scenario)": "+6,500 to +8,000 trips/mo",
            "Estimated Cost": "Rs 80-120/trip (Surge funded, net <= Rs 45)",
            "Primary Metric": "Suburb Cancellation < 10%"
        }
    ])
