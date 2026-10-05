# Optional storage and retention

Interactive results can stay in the notebook or `results/<sub-analysis>/`. Freeze
checkpoints worth comparing, citing or sharing. External storage is optional.

## Configuration

Use the file selected by `DATA_SCIENCE_CONFIG`, or bundled
[config.yaml](../config.yaml) when unset. Resolve relative paths from that file;
null means unconfigured. Keep personal paths, provider, destination, profile and backend
options there; credentials stay in the storage tool's normal credential system.
Use the configured profile and options as defaults for reads from the same
backend as well as retention. Explicit task settings take precedence. Discover
the repository from task context; unconfigured storage does not block local analysis.

## Immutable checkpoints

A `run_id` identifies a deliberately frozen checkpoint of one sub-analysis,
possibly combining several cells and reused computations. Create one only when
retaining a version, using a unique UTC timestamp and short random suffix, e.g.
`20261002T143012Z-a7c3`. Cell edits, restarts and reruns do not require IDs.

Keep frozen outputs unchanged under `results/<sub-analysis>/<run-id>/`; use a new
ID for a changed version worth retaining and the same ID for an identical retry.
Identify the producing source with a clean Git revision or a snapshot of the
notebook, imported local helpers and environment files, including relevant
uncommitted changes. A link to a mutable notebook alone cannot identify an older
result. The notebook carries data provenance, parameters and interpretation.

## External retention

Use existing storage tooling with the configured provider and backend options.
Retain the selected checkpoint at a distinct prefix:

```text
<key-prefix>/experiments/<experiment-id>/results/<sub-analysis>/<run-id>/<relative-path>
```

Default an unset `key_prefix` to the repository directory name. Choose the
checkpoint's internal structure as useful. Keep a local manifest recording IDs,
UTC creation time, source revision or snapshot, retrievable storage locator, and
retained file paths, sizes and SHA-256 checksums; omit credentials and temporary
signed URLs. Link it from `experiment.yaml`. Verify retained evidence and report
incomplete retention honestly. Local analysis does not require external retention.
