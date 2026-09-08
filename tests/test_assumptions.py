"""
Unit tests validating foundational assumptions, schema integrity, and referential constraints.
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from src.segmentation import summarize_activation
from src.airport import analyze_airport_mismatch_comprehensive
from src.campaign import evaluate_camp_wa_002_rigorous

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

@pytest.fixture(scope="module")
def datasets():
    return {
        "captains": pd.read_csv(DATA_DIR / "captains.csv"),
        "doc_events": pd.read_csv(DATA_DIR / "doc_events.csv"),
        "approvals": pd.read_csv(DATA_DIR / "approvals.csv"),
        "activation": pd.read_csv(DATA_DIR / "activation.csv"),
        "nudges": pd.read_csv(DATA_DIR / "nudges.csv"),
        "airport_hourly": pd.read_csv(DATA_DIR / "airport_hourly.csv"),
        "airport_trips": pd.read_csv(DATA_DIR / "airport_trips.csv"),
    }

def test_captain_id_uniqueness(datasets):
    caps = datasets["captains"]
    assert len(caps) == caps["captain_id"].nunique(), "captain_id must be unique in captains.csv"
    assert len(caps) == 25000, "captains.csv must contain exactly 25,000 records"

def test_approvals_referential_integrity(datasets):
    caps = datasets["captains"]
    apps = datasets["approvals"]
    assert len(apps) == len(caps), "approvals.csv must have 1:1 record count with captains.csv"
    assert set(apps["captain_id"]) == set(caps["captain_id"]), "Foreign key mismatch between approvals and captains"

def test_activation_referential_integrity(datasets):
    apps = datasets["approvals"]
    act = datasets["activation"]
    approved_ids = set(apps[apps["final_status"] == "approved"]["captain_id"])
    act_ids = set(act["captain_id"])
    assert act_ids == approved_ids, "activation.csv must exactly match approved captains in approvals.csv"
    assert len(act) == 4206, "Expected exactly 4,206 approved captains in activation.csv"

def test_airport_hourly_balancing(datasets):
    hourly = datasets["airport_hourly"]
    mismatch = hourly["requests"] != (hourly["fulfilled_requests"] + hourly["unfulfilled_requests"])
    assert mismatch.sum() == 0, "Hourly requests must equal fulfilled + unfulfilled requests"

def test_airport_trips_validity(datasets):
    trips = datasets["airport_trips"]
    assert (trips["trip_distance_km"] <= 0).sum() == 0, "All trip distances must be strictly positive"
    assert (trips["fare_inr"] <= 0).sum() == 0, "All fares must be strictly positive"
    assert set(trips["captain_cancelled"].unique()).issubset({0, 1}), "captain_cancelled must be binary (0 or 1)"
    assert set(trips["got_return_fare_within_20min"].unique()).issubset({0, 1}), "got_return_fare must be binary"

def test_document_attempt_limit(datasets):
    assert datasets["doc_events"]["attempt_no"].max() <= 3

def test_chronological_integrity(datasets):
    caps = datasets["captains"].copy()
    apps = datasets["approvals"].copy()
    acts = datasets["activation"].copy()
    
    caps["signup_ts"] = pd.to_datetime(caps["signup_ts"])
    apps["decision_ts"] = pd.to_datetime(apps["decision_ts"])
    acts["first_order_ts"] = pd.to_datetime(acts["first_order_ts"])
    
    m = caps.merge(apps, on="captain_id").merge(acts, on="captain_id", how="left")
    
    # Decision strictly after signup
    valid_dec = m[m["decision_ts"].notnull()]
    assert (valid_dec["decision_ts"] < valid_dec["signup_ts"]).sum() == 0, "decision_ts must be >= signup_ts"
    
    # First order strictly after decision
    valid_order = m[m["first_order_ts"].notnull()]
    assert (valid_order["first_order_ts"] < valid_order["decision_ts"]).sum() == 0, "first_order_ts must be >= decision_ts"

def test_a2o_r2a_summary_uses_approved_and_activated_cohorts(datasets):
    summary = summarize_activation(
        datasets["captains"], datasets["approvals"], datasets["activation"]
    ).set_index("metric")

    assert summary.loc["A2O (signup to approved)", "numerator"] == 4206
    assert summary.loc["R2A (signup to first order)", "numerator"] == 4104
    assert summary.loc["R2A (signup to first order)", "denominator"] == 25000

def test_airport_profile_excludes_non_terminal_zones(datasets):
    result = analyze_airport_mismatch_comprehensive(datasets["airport_hourly"])
    terminal_rows = result["raw_terminal_df"]

    assert terminal_rows["zone_type"].eq("airport_terminal").all()
    assert terminal_rows["requests"].sum() == 136814

def test_campaign_reports_pre_nudge_timing_audit(datasets):
    nudges = datasets["nudges"].copy()
    nudges["sent_ts"] = pd.to_datetime(nudges["sent_ts"])
    result = evaluate_camp_wa_002_rigorous(
        datasets["captains"], datasets["doc_events"], datasets["approvals"], nudges
    )

    assert result["treated_pre_nudge_dl_rc_rate_pct"] == 100.0
    assert "control timing remains unaligned" in result["timing_audit"]
    risk_set = result["time_aligned_risk_set"]
    assert risk_set["outcome_horizon_days"] == 14
    assert risk_set["treated_n"] > 0
    assert risk_set["control_n"] > 0
    assert risk_set["treated_n"] > 0
