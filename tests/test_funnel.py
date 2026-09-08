"""
Unit tests validating Onboarding Funnel arithmetic, constraints, and loss shares.
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from src.funnel import build_onboarding_funnel, compute_stage_timing_summary

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

@pytest.fixture(scope="module")
def raw_data():
    return {
        "captains": pd.read_csv(DATA_DIR / "captains.csv"),
        "doc_events": pd.read_csv(DATA_DIR / "doc_events.csv"),
        "approvals": pd.read_csv(DATA_DIR / "approvals.csv"),
        "activation": pd.read_csv(DATA_DIR / "activation.csv"),
    }

def test_funnel_arithmetic_consistency(raw_data):
    funnel = build_onboarding_funnel(
        raw_data["captains"], raw_data["doc_events"], raw_data["approvals"], mature_only=False
    )
    
    # 1. Stage drop must equal Eligible - Completed
    for idx, row in funnel.iterrows():
        assert row["Drop"] == row["Eligible Captains"] - row["Completed"]
        
    # 2. Stage conversion calculation
    for idx, row in funnel.iterrows():
        expected_conv = round((row["Completed"] / row["Eligible Captains"]) * 100, 2)
        assert row["Stage Conversion (%)"] == expected_conv
        
    # 3. Cumulative conversion calculation
    total_signups = funnel.loc[0, "Completed"]
    for idx, row in funnel.iterrows():
        expected_cum = round((row["Completed"] / total_signups) * 100, 2)
        assert row["Cumulative Conversion (%)"] == expected_cum
        
    # 4. Sum of all stage drops must equal total funnel loss (Signups - Approved)
    total_approved = funnel.loc[7, "Completed"]
    assert funnel["Drop"].sum() == total_signups - total_approved
    
    # 5. Share of total losses must sum to 100% (allowing small rounding tolerance)
    assert pytest.approx(funnel["Share of Total Losses (%)"].sum(), 0.1) == 100.0

def test_mature_cohort_funnel(raw_data):
    funnel_mature = build_onboarding_funnel(
        raw_data["captains"], raw_data["doc_events"], raw_data["approvals"], mature_only=True
    )
    assert funnel_mature.loc[0, "Completed"] == 22407, "Expected 22,407 mature signups prior to June 15"
    assert funnel_mature.loc[7, "Completed"] == 3938, "Expected 3,938 approvals in mature cohorts"

def test_approval_stage_requires_insurance_completion(raw_data):
    approvals = raw_data["approvals"].copy()
    approvals.loc[0, "final_status"] = "approved"

    funnel = build_onboarding_funnel(
        raw_data["captains"], raw_data["doc_events"], approvals, mature_only=False
    )

    assert funnel.loc[7, "Completed"] == 4206

def test_stage_timing_summary_has_nonnegative_percentiles(raw_data):
    timing = compute_stage_timing_summary(raw_data["captains"], raw_data["doc_events"])

    assert len(timing) == 6
    assert (timing["p25_days"] <= timing["median_days"]).all()
    assert (timing["median_days"] <= timing["p75_days"]).all()
