# A brief the executor should return

Illustrative, authored for the workshop. `python tools/demo.py deviation --dest <new dir>`
issues the two sections below as BRIEF-001 in a fresh copy. The executor's check before
work should fail and it should hand back `returned-deviation` without changing any file.
`DEVIATION_HANDBACK.txt` shows the expected handback and doubles as the scripted fallback.
The demo copy leaves this folder out, so a live executor cannot read the answer.

What is wrong with it, against the executor's check before work:

| Check | Problem |
|---|---|
| No contradiction with the contract | "Three retries after the first request" is the option D001 rejected. |
| Owned paths | None named: "touch whatever makes sense". |
| Out-of-scope list | None, and it invites backoff and jitter, which the lab rules out. |
| Kill criterion | None. |
| Re-runnable checks | "Make sure the tests pass" names no command or suite. |

## 1 Context and decision

Users say failed requests give up too early.
Decision: give clients three retries after the first request.

## 2 Brief

Objective: tidy up the retry logic so a request gets three retries after the first try.
The fix is probably small, so touch whatever makes sense.
Add exponential backoff and jitter while you are in there if it helps.
Make sure the tests pass.
