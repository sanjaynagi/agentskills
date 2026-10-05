# Experiment structure

Use one folder per coherent research question. Related hypotheses and parameter
changes normally stay together; start another experiment when its question can
stand alone. Adapt existing work incrementally rather than reorganising it to
fit this example.

```text
experiments/<experiment-id>/
  experiment.yaml
  pixi.toml
  pixi.lock
  notebooks/analysis.py
  results/<sub-analysis>/...
  data/          # optional retained analytical inputs
  resources/     # optional papers, protocols and supporting materials
  scripts/       # optional experiment-specific batch helpers
  config/        # optional analytical parameters
  tests/         # optional substantive logic tests
  .local/        # optional ignored, disposable downloads and scratch
```

Create directories only as needed. Shared environments, materials and code can
remain in existing locations; link them rather than duplicate them. Promote
helpers to shared modules or workflows when actual reuse warrants it. Group
results by sub-analysis; the human or agent chooses useful names and deeper
structure.

## IDs and records

For new IDs and folder names, use `YYYY-MM-DD-short-topic` with the creation date,
lowercase letters, digits and hyphens; check uniqueness. Keep IDs stable as aims
evolve. Existing folder names can remain their IDs. Find prior work by searching
folder names, records and notebook source; link related experiments from records.

Adapt [the record template](../assets/experiment.yaml), keeping five fields:

- `id`: stable identifier matching the folder name.
- `aims`: short list of research questions.
- `findings`: observations and appropriately qualified conclusions.
- `limitations`: material limits on the evidence.
- `links`: descriptive labels mapped to relative paths or URLs.

Resolve relative links from the experiment directory. Link the entry notebook,
useful outputs, reports or related experiments. Empty findings are valid. The
notebook owns analytical detail, provenance and next steps.

## Portable files

Use an experiment Pixi project by default; link an explicitly shared manifest
from the record when appropriate. Keep its manifest and lockfile with the source.
Resolve notebook paths from an explicit experiment root so saved work remains
relocatable. Split notebooks when useful; numeric prefixes imply a real sequence.

Inputs used by code belong in `data/`, supporting materials in `resources/`, and
derived outputs in `results/`. Local retention does not imply Git tracking or
external storage; choose tracking explicitly and normally ignore large downloads
and disposable scratch. Keep personal paths and storage settings in the active
user configuration, separate from analytical parameters.
