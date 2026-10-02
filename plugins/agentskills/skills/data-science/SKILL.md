---
name: data-science
description: Conduct or resume exploratory data-science research using marimo pair and Pixi. Use for investigating hypotheses, developing notebook analyses, organising experiments, validating findings, and leaving reproducible evidence and research handoffs. For report-only requests, use scientific-report instead.
---

# Data science

Use a live marimo notebook as the research workspace and Pixi for its environment.
Leave an experiment another person or agent can find, understand and continue.
The notebook records data, definitions, methods and provenance; a thin YAML record
summarises the aims, findings, limitations and useful links.

These instructions work with Claude Code and Codex. Resolve bundled paths relative
to this `SKILL.md`. Use the `marimo-pair` skill for connecting to notebooks,
writing and executing code, and viewing outputs.

## Configuration

Read the configuration file selected by `DATA_SCIENCE_CONFIG`, or the bundled
[config.yaml](config.yaml) when that variable is unset. Use one active configuration
file, without merging personal defaults from other locations. Resolve relative
configured paths from that file's directory. Bundled null values mean unconfigured.

All user-, machine- and deployment-specific settings belong there: repository
location, artifact destination, profile and backend options. Keep credentials in
the storage tool's normal credential system. Discover the repository from the task
context when no location is configured; an explicit task target takes precedence.
An unconfigured artifact destination does not prevent local analysis.

## Start or resume

1. Locate the relevant experiment and read `experiment.yaml` and its linked
   notebooks. Inspect existing results before repeating an investigation.
2. For a new experiment, read [references/structure.md](references/structure.md)
   and adapt [assets/experiment.yaml](assets/experiment.yaml). Create only the
   directories needed now. Preserve existing experiment IDs and useful structure.
3. Use the experiment's Pixi manifest and lockfile, or its explicitly shared Pixi
   project. Keep notebook and batch execution in the intended environment. Record
   dependency changes in that manifest and lockfile. Avoid a second dependency
   specification inside a notebook using a project environment.
4. Identify the intended live notebook through marimo pair. Read its current cells,
   outputs, errors and relevant dependencies before editing. The active runtime
   is authoritative; edit a live notebook through marimo pair rather than its
   `.py` file. File edits are appropriate when the notebook is not running.

Recover the current question, prior evidence and unfinished work. State what the
next investigation will resolve. Retain useful scratch work as saved notebook
cells; scratch bindings alone are not a durable analysis.

## Explore and validate

- State the hypothesis and what would support or weaken it. For open exploration,
  state the question without inventing a prior hypothesis. Mark post hoc ideas.
- Record input sources or snapshots, retrieval details, cohort and variable
  definitions, exclusions, reference versions and relevant parameters in the
  notebook. Record seeds for stochastic work and influential compute settings.
- Check the aspects that can change the answer: units, missingness, duplicates,
  join cardinality, denominators, selection effects and leakage. Keep original
  evidence intact and make transformations explicit.
- Investigate plausible alternative explanations and sensitivity to reasonable
  analytical choices. Account for dependence, confounding and multiple testing
  when they matter to the question. Report meaningful uncertainty without adding
  statistical tests merely to make descriptive work look formal.
- Distinguish observation, interpretation and recommendation. Keep negative and
  inconclusive findings. A successful execution does not establish scientific
  validity, and an association alone does not establish causation.
- Inspect outputs, not just execution status. For important visual results, inspect
  the rendered figure as well as its source values. Put interpretation beside
  evidence and make uncertainty and denominators visible.

Choose the next computation based on what would resolve uncertainty. Reuse the
tooling's existing caches and retained expensive outputs, recording that reuse.
Keep expensive computation separate from cheap presentation where useful, and
use existing batch workflows for work that should survive an interactive session.
This skill does not implement persistent computation caching or a job scheduler.

## Pair and checkpoint

Keep the notebook focused on the current question, important outputs and their
interpretation. Read current cell state before replacing code; consider reactive
dependents before executing an expensive change. Avoid incidental in-place
mutations of notebook-owned objects from scratch execution.

Coordinate one agent responsible for edits to a live notebook at a time. The
human can continue steering and editing; inspect fresh state before acting on
their changes. Separate investigations can use separate notebooks.

At meaningful checkpoints, save useful cells and update the experiment record.
Keep its five fields thin: `id`, `aims`, `findings`, `limitations`, `links`. The
notebook carries the detailed provenance and next steps. Link findings to useful
evidence through notebook sections, output paths or reports.

Group output files by sub-analysis; let the investigation determine deeper
structure. For deliberately frozen outputs or optional external retention, read
[references/retention.md](references/retention.md). Do not create a run ID for
every cell execution or require uploads to complete an experiment.

## Complete and hand off

Check that saved cells reproduce the important outputs from a fresh process before
treating an analysis as complete. Use substantive assertions in the notebook and
tests for shared analytical logic when they improve confidence. Match verification
to the change; do not add tests that merely mirror implementation details.

If a full replay is impractical, state what was replayed, which expensive outputs
were reused and what remains unverified. Do not imply that reused stages were run.
Preserve the saved notebook and outputs; use a separate process for replay rather
than disrupting the user's live session unnecessarily.

Update findings and limitations, link the evidence, and leave clear next steps in
the notebook. Report the outcome and the practical limits of the evidence. Use
`scientific-report` when an available reporting skill fits the requested deliverable;
a separate report or catalogue is not required for every investigation.
