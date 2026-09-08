"""
Data loading module with explicit data types and timestamp parsing.
"""
from pathlib import Path
import pandas as pd
from typing import Dict, Optional

DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def load_captains(data_dir: Optional[Path] = None) -> pd.DataFrame:
    d = Path(data_dir) if data_dir else DEFAULT_DATA_DIR
    df = pd.read_csv(d / "captains.csv")
    df['signup_ts'] = pd.to_datetime(df['signup_ts'])
    return df

def load_doc_events(data_dir: Optional[Path] = None) -> pd.DataFrame:
    d = Path(data_dir) if data_dir else DEFAULT_DATA_DIR
    df = pd.read_csv(d / "doc_events.csv")
    df['event_ts'] = pd.to_datetime(df['event_ts'])
    return df

def load_approvals(data_dir: Optional[Path] = None) -> pd.DataFrame:
    d = Path(data_dir) if data_dir else DEFAULT_DATA_DIR
    df = pd.read_csv(d / "approvals.csv")
    df['decision_ts'] = pd.to_datetime(df['decision_ts'])
    return df

def load_activation(data_dir: Optional[Path] = None) -> pd.DataFrame:
    d = Path(data_dir) if data_dir else DEFAULT_DATA_DIR
    df = pd.read_csv(d / "activation.csv")
    df['first_order_ts'] = pd.to_datetime(df['first_order_ts'])
    return df

def load_nudges(data_dir: Optional[Path] = None) -> pd.DataFrame:
    d = Path(data_dir) if data_dir else DEFAULT_DATA_DIR
    df = pd.read_csv(d / "nudges.csv")
    df['sent_ts'] = pd.to_datetime(df['sent_ts'])
    return df

def load_airport_hourly(data_dir: Optional[Path] = None) -> pd.DataFrame:
    d = Path(data_dir) if data_dir else DEFAULT_DATA_DIR
    df = pd.read_csv(d / "airport_hourly.csv")
    df['hour_ts'] = pd.to_datetime(df['hour_ts'])
    return df

def load_airport_trips(data_dir: Optional[Path] = None) -> pd.DataFrame:
    d = Path(data_dir) if data_dir else DEFAULT_DATA_DIR
    df = pd.read_csv(d / "airport_trips.csv")
    df['request_ts'] = pd.to_datetime(df['request_ts'])
    return df

def load_all_data(data_dir: Optional[Path] = None) -> Dict[str, pd.DataFrame]:
    """Load all 7 raw CSV files into a dictionary of DataFrames."""
    return {
        "captains": load_captains(data_dir),
        "doc_events": load_doc_events(data_dir),
        "approvals": load_approvals(data_dir),
        "activation": load_activation(data_dir),
        "nudges": load_nudges(data_dir),
        "airport_hourly": load_airport_hourly(data_dir),
        "airport_trips": load_airport_trips(data_dir),
    }
