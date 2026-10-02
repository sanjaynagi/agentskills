# Experiment structure

Use one folder per coherent research question. Related hypotheses, parameter
changes and follow-up figures normally belong to the same experiment. Start
another when its question can usefully stand alone.

## Layout

```text
<repo>/
  experiments/
    <experiment-id>/
      experiment.yaml
      pixi.toml
      pixi.lock
      notebooks/
        analysis.py
      scripts/                    # optional experiment-specific batch helpers
      config/                     # optional analytical parameters
      data/                       # optional retained analytical inputs
      resources/                  # optional supporting materials
      tests/                      # optional substantive logic tests
      results/
        <sub-analysis>/
          ...                     # choose useful filenames and substructure
          <run-id>/               # optional frozen output checkpoint
            ...
      .local/                     # ignored, disposable downloads and scratch
  workflows/                      # reusable analytical workflows, when needed
  src/                            # shared Python code, when reuse warrants it
  docs/                           # cross-experiment conventions and notes
```

Create directories as needed. A new experiment starts with its record, notebook
and Pixi environment. Adapt to existing repository conventions rather than
reorganising old work simply to fit this example.

## IDs and discovery

Use `YYYY-MM-DD-short-topic` for new experiment IDs and folder names. The date is
the creation date; use lowercase letters, digits and hyphens. Check uniqueness,
adding a descriptive suffix if necessary. Keep the ID fixed as the aim evolves.
Existing experiments can keep their folder names as stable IDs.

Prefer a flat `experiments/` directory. Link related experiments from their
records rather than requiring a topic hierarchy or a catalogue. To locate prior
work, search folder names, experiment records and notebook source.

## Thin record

Copy `../assets/experiment.yaml`, resolving it from this reference's directory.
Keep the initial schema to five fields:

- `id`: the stable experiment identifier, matching its folder name.
- `aims`: a short list of research questions or aims.
- `findings`: a short list of observations and appropriately qualified conclusions.
- `limitations`: a short list of material limits on the evidence.
- `links`: descriptive labels mapped to relative paths or URLs.

Resolve record-relative links from the experiment directory. Useful links include
the entry notebook, output checkpoints, reports and related experiments. Update
the summary at meaningful checkpoints. Empty findings mean none have been recorded;
do not invent conclusions to fill the template.

The notebook contains the analytical detail and next steps. Add a README only when
a complex experiment needs navigation beyond the record's links.

## Files and environments

Start with `notebooks/analysis.py`; split into descriptively named notebooks when
that improves readability. Numeric prefixes are useful only for a real sequence.
Resolve analytical paths from an explicit experiment root, not an incidental
caller working directory. Saved notebooks should remain relocatable.

Use a Pixi project per experiment by default. Use a shared project when explicitly
appropriate and link its manifest from the experiment record. Keep the manifest
and lockfile with the source. Select supported platforms for the actual workload;
avoid machine-specific installation paths in saved code.

Experiment-specific helpers belong in `scripts/`; promote them to shared modules
or `workflows/` when another experiment actually needs them. Analytical parameters
belong in the experiment's `config/` when they warrant a separate file. Personal
paths, profiles and storage destinations belong only in the skill's active user
configuration, not in the analytical parameter files.

Use `data/` for retained inputs used by code, including reference sequences and
curated annotations. Use `resources/` for papers, protocols, manuals or explanatory
materials. Derived outputs belong in `results/`. Shared materials can remain in
existing shared directories and be linked from the notebook.

Keeping a file locally does not imply tracking it in Git or uploading it with
results. Keep disposable files under `.local/` and ignore that directory. Choose
tracking of retained inputs explicitly; large downloaded inputs normally remain
ignored. Input provenance belongs in the notebook, with extra manifests only when
they help manage files.

Group results by sub-analysis, with related figures, tables and interpretation
together. Let the human or agent decide useful names and deeper structure as the
investigation develops.
