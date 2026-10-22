# SmartRetry lab rules

Product aim: bounded retries without replaying writes. See docs/CONTRACT.md.
Python 3.10+ standard library only. All commands run from this directory.
The deliberately flawed starting fixture is a teaching aid. Read your role definition
(docs/co-arch/ROLE_COARCH.md or ROLE_EXECUTOR.md), then its startup prompt under
docs/co-arch/prompts, before changing anything. The role file wins if they disagree.
Co-architect reviews and records decisions; executor edits only src/retry_policy.py.
Tests, tools and the contract are reviewer-owned. Never weaken tests to get green.
One issued OR returned brief at a time. Pause implementation during review.
tools/workflow.py owns lifecycle metadata and INDEX.md. Use its commands for transitions.
No deployment, external services, credentials, destructive git commands or installations.
This is a cooperative workflow, not a sandbox or permission boundary.
Run `python -m unittest tests.test_workflow -v` to test the helper.
The lab's product acceptance tests intentionally fail until the defect is repaired.
