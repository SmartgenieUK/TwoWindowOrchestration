# Claude Code setup

Use two local Claude Code terminal sessions in the SAME copy of this lab.
Install and sign in using your organisation's approved process before the lesson.
From the lab directory, run `claude` in terminal A and `claude` in terminal B.
In A enter `/coarch`. In B, after the brief is issued, enter `/executor`.
The included .claude/commands files are thin pointers to the common role prompts.
Official docs confirm this older command format remains supported. For new deployment,
you can wrap the same prompts as project skills using your current team conventions.

Portable fallback in A: "Read and follow docs/co-arch/prompts/COARCH-STARTUP.md."
Portable fallback in B: "Read and follow docs/co-arch/prompts/EXECUTOR-STARTUP.md."
These one-time role selections work without custom commands. Do not paste handoffs.
When the executor finishes, wake A with "Review the returned brief from disk."
When A reissues, wake B with "Process the issued brief from disk."
Do not allow both windows to write code at once. Keep normal permission protections.

Official reference checked 9 October 2026: https://code.claude.com/docs/en/skills
A desktop or cloud session without this same local filesystem is not interchangeable.
