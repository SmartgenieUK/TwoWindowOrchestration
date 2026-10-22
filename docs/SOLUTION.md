# SmartRetry solution

Read this after the exercise. The error is `attempt <= max_attempts`.
Replace it with `attempt < max_attempts` in src/retry_policy.py.

The function runs after the current attempt. At attempt 3 of a budget of 3, allowing a
retry schedules attempt 4. The inclusive comparison therefore exceeds the budget by one.
For a budget of 3 the answers are True, True, False, False for attempts 1 through 4.
For a budget of 1, the initial request uses the entire budget, so no retry is allowed.

Expected corrected results: 6 basic tests pass and 18 acceptance test methods pass.
The original six tests cover early attempts, a successful request, a POST, a client error
and HEAD. They never reach the budget limit. The acceptance suite checks that limit,
the one-attempt case and the invariant that a budget of N permits N minus 1 retries.

Example owner receipt:

```text
done
The policy now stops at the total-attempt limit.
Reviewer reran 18 acceptance tests and inspected the boundary.
Evidence: docs/co-arch/BRIEF-001-retry-budget.md
Remaining limit: policy function only; no HTTP integration.
No decision needed.
```

Production extensions need a separate brief: total elapsed budget, delay and jitter,
Retry-After handling, cancellation, observability and operation-specific safety. A GET
label alone does not prove that a badly designed endpoint has no side effects. Do not
reuse this teaching policy as a complete client implementation.
