| File Name          |   Rows |   Columns | Primary / ID Key   |   Duplicate IDs | Columns with Nulls                                                              |
|:-------------------|-------:|----------:|:-------------------|----------------:|:--------------------------------------------------------------------------------|
| captains.csv       |  25000 |         9 | captain_id         |               0 | None                                                                            |
| doc_events.csv     | 186282 |         7 | event_id           |               0 | failure_reason (166510)                                                         |
| approvals.csv      |  25000 |         5 | captain_id         |               0 | decision_ts (20359), last_stage_reached (4393)                                  |
| activation.csv     |   4206 |         5 | captain_id         |               0 | first_order_ts (102), orders_d7 (187), orders_d30 (834), online_hours_d30 (834) |
| nudges.csv         |  16314 |         6 | Composite / None   |               0 | None                                                                            |
| airport_hourly.csv |  10248 |         9 | Composite / None   |               0 | None                                                                            |
| airport_trips.csv  |  60000 |         9 | trip_id            |               0 | None                                                                            |