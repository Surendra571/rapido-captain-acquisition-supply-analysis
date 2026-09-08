"""
Segmentation module: funnel conversion segmented by channel, vehicle, city, device tier.
"""
import pandas as pd
import numpy as np

def summarize_activation(captains_df: pd.DataFrame, approvals_df: pd.DataFrame, activation_df: pd.DataFrame) -> pd.DataFrame:
    """Return A2O and R2A counts and rates for the full signup cohort."""
    total_signups = captains_df['captain_id'].nunique()
    approved_ids = set(approvals_df.loc[approvals_df['final_status'].eq('approved'), 'captain_id'])
    activated_ids = set(activation_df.loc[activation_df['first_order_ts'].notna(), 'captain_id'])
    approved_and_activated = approved_ids & activated_ids

    return pd.DataFrame([
        {
            'metric': 'A2O (signup to approved)',
            'numerator': len(approved_ids),
            'denominator': total_signups,
            'rate_pct': round(len(approved_ids) / total_signups * 100, 2),
        },
        {
            'metric': 'R2A (signup to first order)',
            'numerator': len(approved_and_activated),
            'denominator': total_signups,
            'rate_pct': round(len(approved_and_activated) / total_signups * 100, 2),
        },
        {
            'metric': 'Activation after approval',
            'numerator': len(approved_and_activated),
            'denominator': len(approved_ids),
            'rate_pct': round(len(approved_and_activated) / len(approved_ids) * 100, 2),
        },
    ])

def segment_funnel_by_column(captains_df: pd.DataFrame, approvals_df: pd.DataFrame, activation_df: pd.DataFrame, segment_col: str) -> pd.DataFrame:
    """Computes approval and activation rates segmented by any column in captains_df."""
    merged = captains_df.merge(approvals_df, on='captain_id', how='left').merge(activation_df, on='captain_id', how='left')
    
    summary = merged.groupby(segment_col).agg(
        total_signups=('captain_id', 'count'),
        all_docs_cleared=('docs_cleared', lambda x: (x == 6).sum()),
        approved=('final_status', lambda x: (x == 'approved').sum()),
        activated=('first_order_ts', lambda x: x.notnull().sum()),
        active_d30=('orders_d30', lambda x: (x > 0).sum())
    ).reset_index()
    
    summary['approval_rate_pct'] = (summary['approved'] / summary['total_signups'] * 100).round(2)
    summary['activation_rate_pct'] = (summary['activated'] / summary['approved'] * 100).round(2)
    summary['end_to_end_rate_pct'] = (summary['activated'] / summary['total_signups'] * 100).round(2)
    return summary.sort_values(by='total_signups', ascending=False)
