---
name: build
description: Use when writing, reviewing, or planning code in ginkgo - a condensed engineering-standards lens (planning, style, testing, refactoring) with an emphasis on avoiding unnecessary complexity and verbose code.
---

# Build

Reliable, maintainable code with clear structure and explicit contracts. Correctness and clarity beat cleverness.

**Keep it simple, by default.** Avoid unnecessary complexity, over-engineering, and premature abstraction. Don't factor shared logic unless it genuinely improves clarity, and never introduce a generic framework to cover a case that doesn't exist yet. Write the smallest, plainest version that is correct - prefer a few direct lines over a clever one-liner or an extra layer of indirection. Remove dead code as soon as you see it.

**Plan before large changes.** Read `docs/architecture/index.md` for orientation if it exists. For significant work, write a short plan (problem, proposed solution, tradeoffs, success criteria) and align with the user before implementing.

**Structure.** Modular, cohesive, clear separation of concerns. Small, focused functions; thin orchestration, heavy logic in helpers. Explicit names, no abbreviations, obvious control flow. Type hints on all functions; keyword-only params internally. `@dataclass(kw_only=True)` for state containers, with private fields and read-only properties for derived values.

**Comments and docs, minimally.** Comment intent, never restate syntax. Skip comments on trivial (1-3 line) code. NumPy-style docstrings on public symbols only - one-line summary, Parameters, Returns; keep them short unless the logic actually warrants more.

**Be terse in code, not just in comments.** Verbose code is a defect, not a stylistic preference: unnecessary branches, redundant checks, restated conditions, and boilerplate that a helper or the language already handles all cost a reader time for no gain. If a function is getting long, ask whether it's doing too much before assuming it needs a comment to explain itself.

**Testing.** Simple, direct assertions that fail fast. No defensive tests, no masking failures.

Act as a maintainer of the whole codebase, not just the feature you're on. Whenever you notice a defect, dead code, or incoherence (mismatched naming, contradicting logic, stale docs, duplicated paths) - even outside the scope of the current task - report it to the user as soon as you notice it. Don't fix it silently and don't stay quiet because it's not what you were asked about.
