# SmartRetry two-window lab

A hands-on companion to **AI coding without the overload**, Sachin Mundra, SmartGenie.
Maven Lightning Lesson, Thursday 22 October 2026, 16:00–17:00 UK (BST), 11:00–12:00 US Eastern (EDT).

The small codebase contains an intentional retry-budget defect. The six basic tests pass;
the reviewer acceptance suite catches it. You will practise a written brief, an evidence
handoff, a fresh review and a short owner receipt. No production systems or network calls.

## Start in two minutes

Clone this repository or unzip the kit, and open a terminal in its top folder. You need Python 3.10 or later.
No packages to install, no API key and no account needed for the offline path.
On Windows use `py -3` in place of `python` if necessary. On macOS/Linux use `python3`
if `python` is unavailable. All commands below are relative to this directory.

```bash
python --version
python -m unittest tests.test_basic -v
python -m unittest tests.test_acceptance -v
```

Expected: 6 basic tests pass; 4 of 18 acceptance test methods fail. The invariant test
contains multiple subtests, so unittest reports more individual failures. That is the exercise.

## Choose your route

| Route | Start here | Access needed |
|---|---|---|
| Claude Code in both roles | [Claude setup](docs/SETUP_CLAUDE.md) | Two authenticated local Claude Code sessions |
| Codex in both roles | [Codex setup](docs/SETUP_CODEX.md) | Two authenticated local Codex CLI sessions |
| One of each | Use each tool's setup for the selected role | Both tools, same directory |
| Offline or watch along | Run the deterministic replay below | Python only |

Keep both sessions in the SAME physical directory. Separate cloud tasks and separate
worktrees do not share the handoff files automatically. Normal tool permissions still apply.
There is no unattended dispatcher. A short wake-up message starts the next agent turn.

## Try it yourself after the session

The lesson demos this loop live. To close it yourself, allow about ten minutes:

1. Read `docs/CONTRACT.md` and predict the final attempt. Run the basic and acceptance
   tests until the failing boundary is clear.
2. Create and issue a brief with the commands below. In your executor session, fix only
   `src/retry_policy.py`, then run checks and return an honest handback.
3. In the reviewer session, inspect the code against the contract, rerun acceptance
   checks and record review notes. Accept only when behaviour and evidence agree.
4. Close the transcript and explain why attempt 3 cannot retry. Write a one-line
   verdict plus a digest of five lines or fewer.

Stretch: name one production risk this tiny policy does not cover. Do not add it to the brief.

```bash
python tools/workflow.py new
python tools/workflow.py issue
python tools/workflow.py check --suite acceptance
```

After the fix, the executor writes `docs/co-arch/executor-summary.txt`:

```text
done
Changed: src/retry_policy.py
Checks: [the command you actually ran and its result]
Evidence: [path returned by workflow.py check]
Limit: policy function only, with no network integration.
Question: none
```

Replace the bracketed descriptions with actual evidence, then run:

```bash
python tools/workflow.py return --summary docs/co-arch/executor-summary.txt
```

The reviewer writes `docs/co-arch/review-notes.txt`. Each of these lines needs a real finding:

Use `python tools/workflow.py diff` to inspect the source change against the starter without Git.

```text
Scope: [what the diff changes and whether it stays within the brief]
Intent: [how the behaviour satisfies the contract]
Risk: [remaining limitations or concerns]
Understanding: [why the final permitted attempt cannot schedule another]
```

Then, in the reviewer session:

```bash
python tools/workflow.py review --verdict accepted --notes docs/co-arch/review-notes.txt
python tools/workflow.py status
```

The helper reruns the 18 acceptance tests. It refuses acceptance after a failing run, a
non-done handback or file drift. The text in review notes remains a human/agent assertion,
not an independently verified fact. Use `--verdict rejected` to record a rejection, then
`issue` to reopen that brief. Old handbacks and verdicts remain in its History section.

## Reliable presenter replay

```bash
python tools/demo.py run
```

This exercises the whole loop in a temporary copy and cleans it up afterwards. It labels
itself **scripted replay**. It makes no AI calls and reports real Python test results.

For a paused demo, use a new destination each time:

```bash
python tools/demo.py start --dest ../SmartRetry_rehearsal_1
python tools/demo.py reject --root ../SmartRetry_rehearsal_1
python tools/demo.py repair --root ../SmartRetry_rehearsal_1
```

The start command refuses to overwrite an existing directory. The repair command applies
the supplied solution in that rehearsal copy only. For a live agent demo, stop after
rejection, issue the brief in the rehearsal copy and ask the executor to repair it instead.
Allow at most 90 seconds of live waiting before switching to the labelled replay.

### Prepared briefs

[`fixtures/briefs/GOOD_BRIEF.md`](fixtures/briefs/GOOD_BRIEF.md) explains, line by line, what a
brief must include. [`fixtures/briefs/DEVIATION_BRIEF.md`](fixtures/briefs/DEVIATION_BRIEF.md) is
a brief with deliberate gaps. To show the executor's check before work, issue it in a fresh copy:

```bash
python tools/demo.py deviation --dest ../SmartRetry_deviation_1
```

Then start the executor in that folder. It should change nothing and hand back
`returned-deviation`. If it stalls, the command prints the scripted fallback handback to return.

## What to take to your own repository

Copy the role definitions (`docs/co-arch/ROLE_*.md`), the role prompts, LEARNED.md and TEMPLATE.md. Adapt the contract, owned paths and acceptance
commands to one real task. `workflow.py new` is intentionally seeded for this teaching
example; adapt it before treating it as a general-purpose task manager.
Read [METHODOLOGY.md](docs/METHODOLOGY.md) for the process and its limits.
Read [EXERCISE.md](docs/EXERCISE.md) for the worksheet. Solutions are separate.

## Verification

```bash
python -m unittest tests.test_workflow -v
python tools/demo.py run
```

The first tests the orchestration helper. The second demonstrates failed and successful
product acceptance. Running discovery across *all* tests on the starter code will fail
because the product defect is deliberate. That is not a broken installation.

This lab has no external dependencies. Supplied code and documentation are MIT licensed
(see LICENSE). Third-party research remains with its original publishers.
