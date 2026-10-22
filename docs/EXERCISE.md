# Participant worksheet

## Before running anything

For `max_attempts=3`, write the expected result after attempts 1, 2, 3 and 4.
What does a retry budget of 1 allow? Why would a POST be out of scope here?

## During the exercise

Record the command and result you actually observed. Keep failure logs. Point to the
exact expression that disagrees with the contract. Do not change the acceptance tests.
After the executor returns, let only the reviewer run the acceptance step.

## Owner receipt

Verdict:
Behaviour:
Evidence:
Remaining risk:
Next step:
One owner question, only if needed:

## Teach-back with the transcript closed

Explain the difference between 3 total attempts and 3 retries. Name one limitation of
this policy function that you would address before production. Describe the evidence
that would make you reject a confident “done” claim.

## Quick self-check

Did you see a green test result and still find a defect? Did the short digest preserve
the important failure? Can you recover the selected policy from disk? Can you explain
the change without asking the agent to explain it again?

## Five-change measurement sheet

Copy one record for each comparable change. Leave unknown values blank.

| Field | Entry |
|---|---|
| Date and change | |
| Approach and tool pairing | |
| Scope or difficulty | |
| Owner review minutes | |
| Total elapsed minutes | |
| Material defects caught before acceptance | |
| Rework after acceptance | |
| Decisions reopened without new evidence | |
| Model usage or cost, if visible | |
| Can owner explain behaviour the next day | |
| Confounders | |

Reflection: did less reading preserve enough understanding? If not, change the review
boundary or teach-back before tightening the summary further.
