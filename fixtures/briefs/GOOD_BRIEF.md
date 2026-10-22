# A brief the executor can build from

This is BRIEF-001 exactly as `python tools/workflow.py new` writes it, with a note on what
each line is for. The executor's check before work looks for five things: an outcome,
owned paths, an out-of-scope list, a kill criterion and re-runnable checks, none of them
contradicting `docs/CONTRACT.md`. A brief missing any of them goes back as
`returned-deviation` (see `DEVIATION_BRIEF.md`).

## 1 Context and decision

```text
D001: max_attempts includes the first request. Budget 3 means 3 total attempts.
Reason: bounded downstream load. Rejected: 3 retries after the initial request.
Reopen if the owner changes the budget or requirement. The lab pre-agrees this decision.
```

| Line | What it gives the executor |
|---|---|
| D001 | The owner's decision, so the executor never has to guess what "3" means. |
| Reason / Rejected | Why this option, and the alternative that was turned down. Stops the decision being reopened without new evidence. |
| Reopen if | The only conditions that justify revisiting it. |

## 2 Brief

```text
Objective: implement the bounded retry policy in docs/CONTRACT.md.
Owned product path: src/retry_policy.py.
Out of scope: network I/O, delays, write-method retries, dependencies, test or tool edits.
Executor: run basic and acceptance checks; report actual results.
Reviewer: inspect the diff and contract; independently run tests.test_acceptance.
Boundary: attempt == max_attempts must return False.
Understanding: explain total attempts versus additional retries.
Kill criterion: stop if the fix needs any file outside the owned path.
Attempt budget: 2 unsuccessful delivery attempts, then the brief pauses for the owner.
```

| Line | Required? | What it gives the executor |
|---|---|---|
| Objective | Yes: outcome | One outcome, pointing at the written contract rather than restating it. |
| Owned product path | Yes: owned paths | The only file it may change. |
| Out of scope | Yes: out-of-scope list | Binding, even when an adjacent fix looks easy. |
| Executor checks | Yes: re-runnable checks | `workflow.py check --suite basic` and `--suite acceptance`, with actual results reported. |
| Reviewer | Recommended | What acceptance will look like, so nothing is a surprise. |
| Boundary | Recommended | The one case most likely to be wrong. |
| Understanding | Recommended | What the owner must be able to explain afterwards. |
| Kill criterion | Yes | When to stop rather than grow the change. |
| Attempt budget | Recommended | Two failed deliveries, then the owner decides. A brief defect is not an attempt. |
