# agentskills

Portable Codex and Claude Code skills, packaged as a dual-compatible plugin.

## Skills

- **build** - condensed engineering-standards lens (planning, style, testing) with an emphasis on avoiding unnecessary complexity and verbose code.
- **human** - rewrites text to be plain, direct, and free of AI-writing tells.
- **data-science** - exploratory research with marimo pair and Pixi, thin experiment records, scientific validation, and optional output retention.
- **scientific-report** - builds a self-contained, theme-aware HTML report that emphasises readability, interpretability, and scientific accuracy. Includes an HTML template and validator.

## Claude Code

```
/plugin marketplace add sanjaynagi/agentskills
/plugin install agentskills@agentskills
```

The plugin also carries a Codex manifest. Its skills and bundled resources use portable Markdown, HTML, and Python 3 rather than agent-specific tools.

The data-science skill uses Pixi and the separately installed marimo-pair skill for live notebook work. Personal settings can live in one YAML file selected with `DATA_SCIENCE_CONFIG`; the bundled configuration is unconfigured.
