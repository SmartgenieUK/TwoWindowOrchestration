# SmartRetry contract

Aim: bound repeat GET and HEAD attempts for transient failures without replaying writes.
This is a pure policy function for teaching, not a production HTTP client.

`should_retry(method, status, attempt, max_attempts=3)` is called AFTER the current attempt fails or returns a status.
`attempt` is the 1-based current attempt. `max_attempts` includes the initial attempt.
For a budget of 3, attempts 1 and 2 may schedule another attempt; attempt 3 may not.
If attempt already exceeds the budget, return False.

Eligible methods: GET and HEAD only, after trimming whitespace and uppercasing.
Eligible HTTP statuses: 429, 500, 502, 503 and 504 only.
Every other valid method or valid status returns False. POST always returns False.
The budget must allow another attempt as well as satisfying method and status rules.

Method must be a non-empty string. Status must be an integer in 100..599.
Attempt and max_attempts must be positive integers. Booleans are not valid integers here.
Invalid inputs raise ValueError. No calls to the network, sleeping or other side effects.

Owner decision D001: 3 means total attempts, to cap work and downstream load.
Rejected option: 3 retries plus the first request, which permits 4 total attempts.
Reopen only if an owner changes the retry budget or the product requirement changes.

Acceptance: reviewer checks the diff and this contract, executes tests.test_acceptance,
and explains why `attempt == max_attempts` must return False.
Passing tests do not establish production readiness or prove exhaustive correctness.
