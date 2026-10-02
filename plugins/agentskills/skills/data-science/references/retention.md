# Optional output retention

Ordinary interactive results can stay in the notebook or under
`results/<sub-analysis>/`. Freeze outputs when they are worth comparing, citing or
sharing. External storage is optional and uses the active user configuration.

## Run IDs

`run_id` identifies a deliberately retained output checkpoint of one sub-analysis.
It is not a notebook session ID or a log of every execution. A checkpoint can
combine outputs from several cells and reused expensive computations.

Create an ID when intentionally freezing a checkpoint. If changed inputs, methods
or parameters produce another version worth retaining, give that checkpoint a new
ID. Cell edits, slider changes, kernel restarts and parameter changes do not create
IDs by themselves. Retry retention of the exact same checkpoint with the same ID.

Use a UTC timestamp and short random suffix, such as `20261002T143012Z-a7c3`, and
check uniqueness. Local frozen outputs can live at
`results/<sub-analysis>/<run-id>/`. Preserve them unchanged and continue exploration
in working files. A changed retained result belongs to a new checkpoint.

## Evidence and source

Retain the producing source version as well as useful outputs. A clean committed
Git revision can identify the source; otherwise snapshot the notebook, imported
local helpers and environment files, including any relevant uncommitted changes.
Keep source snapshots distinguishable from outputs. The notebook retains data
provenance, parameters and interpretation. Link the checkpoint from the experiment
record. A link to today's mutable notebook alone does not identify an older result.

## External storage

Read provider, destination, profile, key prefix and backend options from the active
configuration. Use existing storage tooling; this skill supplies conventions, not
an upload implementation. If storage is unconfigured, retain locally. Upload the
selected output checkpoint rather than the entire experiment directory.

Within the configured destination, use this key pattern:

```text
<key-prefix>/experiments/<experiment-id>/results/<sub-analysis>/<run-id>/<relative-path>
```

When `key_prefix` is unset, use the repository directory name. `relative-path` is
relative to the frozen checkpoint, so the human or agent can choose its internal
structure. Keep each retained checkpoint at a distinct prefix.

Generate a local checkpoint `manifest.yaml` containing the run ID, experiment ID,
sub-analysis, creation time in UTC, source revision or snapshot reference, resolved
storage locator, and retained file paths, sizes and SHA-256 checksums. Exclude the
manifest itself from its checksum list. Include backend location options needed
for retrieval, but omit credentials and temporary signed URLs.

Upload and verify the selected files, then upload the manifest last to mark a
complete checkpoint. Preserve the same manifest for an identical retry. Link the
local manifest from `experiment.yaml`; it remains useful after large local output
copies are removed. Report incomplete retention instead of marking it complete.
