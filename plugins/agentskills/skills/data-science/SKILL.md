---
name: data-science
description: Conduct or resume exploratory data-science research in live marimo notebooks with Pixi. Use for investigating questions, organising experiments, validating findings and leaving reproducible evidence and handoffs. For report-only requests, use scientific-report instead.
---

# Data science

Use a live marimo notebook as the research workspace and Pixi for its environment.
Use `marimo-pair` to connect, inspect, edit and execute live notebooks; make live
edits through pair. These instructions work with Claude Code and Codex; resolve
bundled paths relative to this file.

## Start or resume

Find the relevant experiment, read its `experiment.yaml` and linked notebooks,
and inspect existing evidence before repeating work. Recover the question and
unfinished work, then state what the next investigation will resolve.

For new experiments or incremental adoption of existing work, read
[references/structure.md](references/structure.md) and adapt
[assets/experiment.yaml](assets/experiment.yaml). Preserve stable experiment IDs
and useful existing structure; create only what is needed. Use the experiment's
Pixi manifest and lockfile, or its explicitly shared Pixi project, for notebook
and batch execution. Record dependency changes there.

## Investigate

- State the question or hypothesis and what would support or weaken it. Mark
  post hoc ideas.
- Keep detailed data definitions and provenance in the notebook: sources and
  snapshots, retrieval details, cohorts, variables, exclusions, reference
  versions, parameters, seeds and influential compute settings.
- Check what can change the answer: units, missingness, duplicates, joins,
  denominators, selection and leakage. Preserve original evidence and make
  transformations explicit.
- Examine alternative explanations and sensitivity to reasonable analytical
  choices. Address dependence, confounding and multiple testing where relevant;
  report uncertainty without adding unnecessary statistical tests.
- Always inspect all outputs, including every rendered visual and its underlying
  values. Place interpretation beside evidence, with denominators and uncertainty
  visible. Distinguish observation from interpretation; successful execution is
  not scientific validation, and association does not establish causation.

Choose computations that resolve uncertainty. Reuse existing caches and expensive
outputs when appropriate, recording the reuse. Save useful exploratory work as
notebook cells and preserve negative and inconclusive findings.

## Checkpoint and hand off

At meaningful checkpoints, save the notebook and update the thin five-field
record: `id`, `aims`, `findings`, `limitations`, `links`. Link findings to evidence;
keep detailed provenance and next steps in the notebook. Group output files by
sub-analysis, choosing deeper structure as the investigation develops.

Before calling an analysis complete, check that saved cells reproduce important
outputs in a fresh process without disrupting the live session. Use substantive
assertions or tests for shared analytical logic when they improve confidence.
If full replay is impractical, state what was replayed, what was reused and what
remains unverified. Report findings and their practical limits, and leave clear
next steps.

For deliberately retained immutable checkpoints or configured external data
access, read [references/retention.md](references/retention.md). A `run_id` belongs
to an intentionally frozen checkpoint, not every cell execution or rerun.
