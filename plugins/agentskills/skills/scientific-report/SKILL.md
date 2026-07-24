---
name: scientific-report
description: Use when asked to produce or restructure an HTML findings/analysis report in a scientific-paper style (e.g. "make an HTML report", "write this up like a paper", "scientific report"). Builds a self-contained, theme-aware HTML page with an abstract, a methods/scope section, Hypothesis→Methods→Results sections, numbered and captioned tables/figures cross-referenced in the text, a bulleted summary, and references. Pairs with the `human` skill for prose.
---

# Scientific report

Turn an analysis into a single self-contained HTML page that reads like a scientific paper: a new reader should follow it top to bottom without prior context. Publish it as an Artifact.

## Non-negotiable structure

Build the page in this order. Number the sections (1, 2, 3…) in headings and in the table of contents.

1. **Title block.** A clear, specific `<h1>` (no status labels in it), a one-sentence lede, and an **infographic**: a compact strip of the headline numbers (`.stat-strip` in the template). This is the at-a-glance result.
2. **Abstract.** One concise section, two short paragraphs at most. Paragraph 1: what was tested and on what data. Paragraph 2: the headline results and the issues that need action. No exhibits, no citations to tables.
3. **Methods and scope.** How the data was produced and checked, the inclusion/exclusion rule, and the scope (counts, date range, what was held out). One place, stated once.
4. **Results sections**, one per analysis. Every one opens with three tagged sentences in this exact order:
   - **Hypothesis.** What we expected to be true and why (the thing being tested).
   - **Methods.** How we tested it. One or two sentences only. e.g. "We grouped every strain + panel + drug combination read two or more times and measured how well the repeat readings agree."
   - **Results.** What we found, in prose, pointing at the numbered exhibits ("Table 2 shows…", "see Figure 4"). Fold any follow-up analysis into this narrative as flowing prose; do not label it "Follow-up 1/2" or number the sub-steps. Bold a load-bearing sentence if it needs emphasis.
5. **Summary, twice.** A bulleted summary appears both **at the very top** (its own section directly below the title/infographic and above the abstract, so a reader sees the key findings first) and **again at the end**. Use the same bullets in both places. Bullet points only; each bullet states one finding and links back to the exhibit that supports it, colour-coded by severity. The up-front copy may forward-reference tables and figures that appear later, which is expected for an executive summary.
6. **References and data.** A numbered `<ol>` of any external standards/sources used, plus the provenance of the underlying data (source files/CSVs). Give each `<li>` an anchor id (`id="ref1"`, `id="ref2"`, …). Omit the section only if genuinely nothing was referenced; keep the data-provenance line regardless.

## Citations

- Where the text names a reference (a standard, a vendor, a dataset, a repository), cite it with a **superscript square-bracket link** to the matching entry in the references list: `<sup class="cite"><a href="#ref1">[1]</a></sup>`. The bracket number matches the reference's position in the `<ol>`.
- Cite at the natural point of mention (usually first mention in Methods, plus wherever a specific claim rests on that source). A number may be reused wherever the same source is mentioned. Do not cite inside the abstract.
- Style the marker small and superscript, e.g. `sup.cite { font-size: 0.72em; line-height: 0; } sup.cite a { text-decoration: none; font-weight: 600; }`, and give the reference items `scroll-margin-top` so the in-page jump lands cleanly.

## Tables and figures

- **Number everything** in one running sequence by order of appearance: Tables 1, 2, 3… and Figures 1, 2, 3… (independent counters). Use letter suffixes for tightly-related exhibits: Table 2a, Table 2b.
- **Every exhibit has a caption** that lets it stand alone: `<strong>Table N.</strong> <plain description>. Source: <where the data came from>.` **Table captions go ABOVE the table; figure captions go BELOW the figure** (scientific-paper convention). In CSS, a `.cap` immediately followed by the table needs its top margin removed and a bottom margin added (e.g. `p.cap:has(+ .table-wrap) { margin-top: 0; margin-bottom: 10px; }`).
- **Refer to every exhibit from the running text** by its number. An exhibit no sentence points to does not belong in the report.

## Layout

- **No callout boxes.** Do not wrap findings, tables, or figures in bordered/shadowed cards. Write findings as plain prose paragraphs. A key sentence can lead with a bolded clause, but it stays in the flow of text, not in a box.
- **No title heading above a table or figure.** The exhibit's only label is its caption beneath it. Any framing you would have put in a heading ("First check: …") goes into the caption instead, where a leading clause may be bold: `<strong>Table 2a. First check: off-scale ceilings that belong to a different panel.</strong> <rest of caption>. Source: …`.
- **Enumerated sub-points are bullet lists, not boxes.** When a section breaks a finding into causes, factors, or cases, use a plain bullet list with a bolded lead per item. Do not give each bullet its own embedded figure; keep the shared figure (if any) once, at section level.
- **Collapsible sections.** Wrap each section's body in `<details open>` with the numbered heading in a `<summary>`, so a reader can fold sections away. Keep them open by default. Style the summary with a rotating chevron (`::before` marker) and remove the native disclosure triangle. Note this changes CSS child selectors: target `section > details > p` and use class selectors (e.g. `.lead`) rather than `section > .lead`.
- **One shared content width for text and exhibits.** Text and exhibits must align to the same left and right edges. Define one width variable (e.g. `--measure: 900px`) and apply it to both the prose blocks and the exhibit wrappers, so neither is narrower than the other. Prefer a generous measure (roughly 850–950px) that lets wide tables fit without shrinking the text; a genuinely over-wide table can still scroll inside its own `overflow-x: auto` wrapper. Do not shrink figures/tables to a narrow text column, and do not leave text narrower than the exhibits.

## Prose

- Write the text with the **`human` skill**: plain, direct, scientific. Invoke it (or apply its rules) on the narrative before publishing.
- **No status pills or badges in headings** ("Action needed", "Mostly explained"). Severity belongs in the prose and, if useful, in the summary bullets' colour.
- Neutral register. State the finding; do not sell it. No "crucial", "pivotal", "underscores".

## Build workflow

1. **Start from `template.html`** in this skill's directory. Copy it, then replace the content between `<main>` and `</main>` and the nav list, keeping the CSS. It already carries everything this style needs: theme variables with a `@media (prefers-color-scheme: dark)` block and `[data-theme]` overrides; the shared `--measure` width; a sticky table-of-contents nav; collapsible `<details>`/`<summary>` sections with a chevron marker; the `.stat-strip` infographic; `.table-wrap`/`table` and a `.cap` caption class (with the table-caption-above rule); a `.figure` wrapper (no border or shadow); div-based chart primitives (`.bar-row`, `.stack`); superscript `sup.cite` citations; a `.summary` bullet list; and a `.refs` list. Do not add bordered/shadowed content cards. If you build from scratch instead, reproduce the same structure and constraints.
2. **Self-contained only.** Inline all CSS/JS, embed any images as data URIs. No external requests (no CDN, fonts, or scripts). Do not add `<!DOCTYPE>`, `<html>`, `<head>`, or `<body>` tags — the Artifact wrapper injects them. Start the file with `<title>`.
3. **Theme-aware.** Keep the dark/light blocks so the page renders correctly in either theme.
4. **Verify before publishing.** Check tag balance (`<div>`/`</div>`, `<table>`/`</table>`, `<section>`, `<p>`), scan for em dashes (expect zero), and confirm the Figure/Table numbers are sequential with no gaps and each is referenced in text.
5. **Publish with the `Artifact` tool.** Set a stable `<title>`, a one-sentence `description`, a `favicon` emoji kept constant across redeploys, and a short `label` (max 60 chars). To update an existing report, pass the same `url` so the link is preserved.

## Verification snippet

```bash
f=report.html
echo "div:   $(grep -o '<div' $f|wc -l) / $(grep -o '</div>' $f|wc -l)"
echo "table: $(grep -o '<table' $f|wc -l) / $(grep -o '</table>' $f|wc -l)"
echo "p:     $(grep -o '<p[ >]' $f|wc -l) / $(grep -o '</p>' $f|wc -l)"
echo "em dashes (want 0): $(grep -o '—' $f|wc -l)"
grep -o '<strong>Table [0-9a-z]*\.' $f; grep -o '<strong>Figure [0-9]*\.' $f
```
