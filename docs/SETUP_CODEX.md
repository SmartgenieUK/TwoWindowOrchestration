# Codex setup

Use two local Codex CLI terminal sessions in the SAME copy of this lab.
Install and sign in using your organisation's approved process before the lesson.
From the lab directory, run `codex` in terminal A and `codex` in terminal B.
Codex reads this project's AGENTS.md. Select a role explicitly in each session:

A: "Read and follow docs/co-arch/prompts/COARCH-STARTUP.md. Act as co-architect."
B, after issue: "Read and follow docs/co-arch/prompts/EXECUTOR-STARTUP.md. Act as executor."

This uses ordinary file-reading prompts. It does not depend on a Claude slash command
or a model-specific API. You can package the same prompts as local Codex skills later.
When the executor finishes, wake A with "Review the returned brief from disk."
When A reissues, wake B with "Process the issued brief from disk."
Do not relay output between sessions. Keep normal approval and sandbox protections.
A cloud task or separate worktree has a different filesystem: that requires an explicit
Git/artifact handoff and is outside this same-directory exercise.

Official references checked 9 October 2026:
https://learn.chatgpt.com/docs/codex/cli
https://learn.chatgpt.com/docs/agent-configuration/agents-md
https://learn.chatgpt.com/docs/build-skills

Mixed pair: run Claude Code in A and Codex in B, or reverse them. Keep both in the same
local lab directory and use the same role prompts. Model diversity can add perspective;
it does not establish independent judgement or guarantee that a defect will be caught.
