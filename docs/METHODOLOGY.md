# Two-window methodology

The aim is to reduce unnecessary human reading while preserving control and understanding.
Treat that benefit as a hypothesis to measure in your own work. Two windows alone do not
establish better judgement, lower cognitive debt or a productivity gain.

## Working agreement

The owner decides goals, consequential architecture and acceptable risk. The co-architect
prepares those decisions, records their rationale, issues bounded work and reviews returns.
The executor implements one brief at a time. Logs and evidence stay on disk.

The owner gets a verdict, a digest of at most five short lines and at most one decision
question per round. A digest must name material uncertainty, any failed check and residual
risk. It may link to evidence. The cap is a communication default, never permission to
conceal a risk. Human review expands when the consequences require it.

For new or consequential behaviour, add a short teach-back: “What does this change do,
where could it fail, and which check would reveal that?” The answer can be two sentences.
Documents preserve rationale; people still need a working mental model.

## One complete loop

1. Discuss one outcome and the owner constraints.
2. Record the chosen option, rejected alternative, reason and reopening trigger.
3. Issue a brief with owned paths, exclusions and reproducible acceptance checks.
4. Execute within scope. Return actual results and evidence, including failures.
5. Review the exact returned version. Inspect its semantics and challenge a likely failure.
6. Accept or reject with recorded evidence. Communicate the next decision concisely.

In this lab, lifecycle is `drafting → issued → returned → accepted | rejected`.
After rejection, the co-architect can reissue a new revision with the prior round archived.
At most one brief may be issued OR returned. Finishing review closes the loop.

## Files and writing rights

| Surface | Owner | Rule |
|---|---|---|
| Brief sections 1 and 2 | Co-architect | Freeze during execution; record revisions deliberately |
| Executor-summary input | Executor | 30-line cap; verdict first; actual evidence |
| Brief section 3 | Workflow helper | Copies the executor's handback on return |
| Review-notes input | Co-architect | Semantic, scope, risk and understanding findings |
| Brief section 4 | Workflow helper | Records the reviewer verdict and actual check output path |
| Status and index | Workflow helper | Serialised updates; index rebuilt from brief metadata |
| Product source | Executor while issued | Review freezes writes |

The Markdown brief is authoritative. INDEX.md is a convenient view, not a second source
of truth. A crash between the brief write and index write can leave the index stale;
`status` rebuilds it. This avoids pretending two file writes are a single transaction.

## What is enforced and what is agreed

The CLI enforces permitted lifecycle transitions, one active brief, summary length, local
file consistency and a successful reviewer-run acceptance suite before accepted status.
Atomic replacement prevents partially written individual files. An exclusive lock serialises
CLI updates. A stale lock needs deliberate investigation, not automatic deletion.

Prompts establish role boundaries. They do not stop an agent with filesystem permissions
from editing tests, forging a record or bypassing the helper. Hashes detect accidental drift
within the cooperative flow; they are not signatures. For team or high-risk adoption use
protected branches, required human review, trusted CI and separate permissions as appropriate.
Code under review can execute during tests. Use the usual isolation for untrusted code.

Two reviewers can share a blind spot, including across different model vendors. The
reviewer needs an independently reasoned acceptance case and the original intent. Running
the author's narrow tests again only repeats their coverage.

## Adoption scope

Try one bounded change on a branch. Keep context small, but let the reviewer open code and
logs when needed. Compress the owner's interface after examining evidence. There is no
promise of a noise-free reviewer context: checking evidence itself consumes context.

Use the full loop where ambiguity, consequence or handoff costs justify it. A trivial
rename may need only an ordinary diff review. Extra model turns and duplicated tests have
latency and usage costs. Track those alongside reading time and quality.

## Measure the next five comparable changes

Record owner review minutes, total elapsed minutes, material defects caught before acceptance,
rework after acceptance, decisions reopened without new evidence, model usage cost if visible,
and whether the owner can explain the behaviour the next day. Use the worksheet.
Keep difficulty and scope similar, alternate the two approaches where feasible and record
confounders. Five changes can inform a local decision; they cannot establish general efficacy.

## Aligned with devgenie-core (commit 4570188)

Each role now has a definition file (`docs/co-arch/ROLE_COARCH.md`, `ROLE_EXECUTOR.md`);
the startup prompt says how a session takes the role up, and the role file wins a conflict.
Carried over for this lab:

- **One team.** A brief is done when the outcome is accepted, not when one window stops.
  Every non-done return is constructive: finding, evidence, effect, smallest fix.
- **Check before work.** The executor checks the brief stands on its own before changing
  anything. A gap is handed back as `returned-deviation`, a brief defect, not an attempt.
- **Keep moving.** Work stops only for a named stop condition; anything else is one line
  in the record. Only the work that depends on a stop is parked.
- **Disagreements.** One exchange through the brief, then a fresh mediator, then the owner.
- **Kill criterion and attempt budget.** Every brief names when to stop; two unsuccessful
  attempts pause it for the owner.
- **LEARNED.md.** Owner interventions are the gold labels, distilled into one-line rules.

Left out, because they belong to a product repo rather than a teaching lab: the change
records (CR, Bug, HITL) and change-admission chain, model delegation scripts, desktop and
phone alerts, pull requests and deployment, and unattended loops. In devgenie-core an
unattended loop is allowed only per loop, in writing, with a cycle budget, and only for
decisions that are reversible, non-destructive, lean and inside the named objective.

## Refinements to the original supplied process

Preserved: separate roles, disk handoff, one work item, short owner digest, recorded rationale,
reviewer-run checks. Clarified: humans retain design authority; decisions can reopen with new
evidence; a manual wake-up is allowed; returned work counts as active; review covers intent
as well as tests. Added: version consistency, history, a comprehension check and measurement.
Replaced universal outcome claims such as “cures fatigue” with a testable design objective.
