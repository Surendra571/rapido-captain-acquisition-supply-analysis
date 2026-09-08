| Check                          | Result                                           |   Count | Status   | Interpretation                                               |
|:-------------------------------|:-------------------------------------------------|--------:|:---------|:-------------------------------------------------------------|
| 1. Primary Key Uniqueness      | 0 duplicates across 4 primary entities           |   25000 | PASS     | Relational integrity verified.                               |
| 2. Chronological Ordering      | 0 inversions (Signup <= Decision <= First Order) |   25000 | PASS     | Valid temporal lifecycle.                                    |
| 3. Airport Hourly Balance      | Requests == Fulfilled + Unfulfilled (0 mismatch) |   10248 | PASS     | 100% closed marketplace accounting.                          |
| 4. Document Attempt Bounds     | Max attempt_no == 3                              |  186282 | PASS     | Within 3-attempt platform policy.                            |
| 5. Activation Referential Link | 100% of activated captains exist in approved set |    4206 | PASS     | Zero unauthorized drivers taking rides.                      |
| 6. ERickshaw Permit Exemption  | 0 PERMIT events for ERickshaws                   |    4756 | PASS     | 5-doc workflow for ERickshaw; 6-doc for Auto/Cab.            |
| 7. Cohort Maturity Isolation   | 1,297 in_progress captains strictly >= June 15   |    1297 | PASS     | 15-day maturity window required for steady-state conversion. |