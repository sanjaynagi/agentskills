---
name: scientific-report
description: Create or restructure a self-contained HTML findings or analysis report in a readable scientific-paper style. Use for exploratory data science, experimental results, validation studies, benchmarking, and other evidence-led analyses that need an abstract, reproducible methods and scope, interpretable results, numbered exhibits, data provenance, and references. Do not use for general dashboards or reports without an analytical evidence structure. Pair with the `human` skill for prose.
---

# Scientific report

Turn an analysis into a single self-contained HTML page that a new reader can understand from top to bottom without prior context. Prioritise readability, interpretability, and scientific accuracy. Save a standalone HTML file unless the environment provides a suitable publishing tool.

Keep the workflow portable across Codex, Claude Code, and other skill-compatible agents. Resolve `assets/` and `scripts/` relative to this `SKILL.md`, not relative to the user's working directory. Do not depend on product-specific publishing tools or metadata.

## Structure

Build the page in this order. Number the sections in the headings and table of contents.

1. **Title block.** Write a clear, specific `<h1>`, followed by a one-sentence lede that states the report's question or purpose. Add a compact `.stat-strip` only when a few headline numbers genuinely help orientation.
2. **Summary.** Place a short bulleted summary directly below the title block. Each bullet states one finding in plain language and links to its supporting exhibit. Use severity colour only when severity is meaningful, and always state the meaning in words rather than relying on colour.
3. **Abstract.** Use no more than two short paragraphs. State what was analysed and on what data, then give the headline findings and any issues that need action. Do not include exhibits or citations.
4. **Methods and scope.** State how the data was produced and checked, the inclusion and exclusion rules, the scope, and anything held out. Keep this information in one place.
5. **Results sections.** Use one section per analysis. Open each with:
   - **Hypothesis.** State what was expected and why. For exploratory work, state the question or pattern being investigated without inventing a prior hypothesis.
   - **Methods.** Explain how it was tested in one or two sentences.
   - **Results.** State what was found and point to the numbered exhibits. Fold follow-up analyses into the narrative rather than labelling them as procedural steps.
6. **Conclusions.** Repeat or lightly consolidate the opening summary bullets. Do not introduce new evidence here.
7. **Glossary, optional.** Include a short definition list when specialist terms, acronyms, or similarly named measures would otherwise slow a non-specialist reader. Define only terms used in the report; do not turn it into a general reference.
8. **References and data.** List external sources in a numbered `<ol>`. Give each reference an anchor ID (`ref1`, `ref2`, and so on). State data provenance separately and always include it, even when there are no external references.

## Interpretability and scientific integrity

- Make each result answer four questions: what was compared or measured, on which observations, what was found, and why it matters.
- State denominators or analysis populations wherever a count, proportion, or rate could otherwise be misread. Report missing data and material exclusions when they affect interpretation.
- Report uncertainty when it is meaningful and available. Do not manufacture confidence intervals, significance tests, or formal hypotheses for an exploratory analysis that did not produce them.
- Distinguish observation from explanation. Use causal language only when the design supports it. Mark post hoc and exploratory interpretations as such.
- Prefer effect sizes and absolute differences over significance alone. If a statistical test is reported, name it and give enough context to interpret it.
- Separate evidence from recommendation: first state what the analysis shows, then state the operational implication.
- Keep one term per concept across prose, summary bullets, table headers, captions, and glossary. Define acronyms at first use.
- Use plain, direct language with the `human` skill. Prefer short sentences and concrete verbs. Discourage em dashes because they often hide sentence structure; use one only when it is clearer than a full stop, comma, colon, or parentheses.
- Use a neutral register. Do not sell the finding or use words such as “crucial”, “pivotal”, or “underscores”.

Apply these checks in proportion to the analysis. A descriptive or exploratory report does not need inferential statistics merely to look scientific.

## Citations

- Cite a named standard, vendor, dataset, repository, or source at its natural point of mention with `<sup class="cite"><a href="#ref1">[1]</a></sup>`.
- Match the bracket number to the source's position in the reference list. Reuse a number for repeated mentions of the same source.
- Do not cite inside the abstract. Do not treat the report's own data-provenance statement as an external citation.

## Tables and figures

- Number tables and figures independently by order of appearance. Use letter suffixes only for tightly related exhibits such as Table 2a and Table 2b.
- Give every exhibit a standalone caption with its source. Put table captions above tables and figure captions below figures.
- Refer to every exhibit from the narrative by number. Remove any exhibit that the prose does not interpret.
- Spell out caption acronyms and use exactly the same variable names as the prose and headers.
- Do not add a separate title heading above an exhibit. Put the framing in its caption.
- Use table headers with `scope="col"` or `scope="row"`. Give charts an accessible label and preserve their values in nearby prose or a table. Never use colour as the sole carrier of meaning.

## Layout

- Do not wrap findings or exhibits in shadowed callout cards. Keep findings in the prose flow.
- Use bullet lists for causes, factors, or cases rather than a grid of boxes.
- Wrap section bodies in `<details open>` with their numbered headings in `<summary>`.
- Align prose and exhibits to the same shared width. Let genuinely wide tables scroll inside an `overflow-x: auto` wrapper.
- Keep inline CSS and JavaScript, embed images as data URIs, and make no external requests.
- Preserve light and dark theme variables.

## Build workflow

1. Copy `assets/template.html`. Replace the content inside `<main>` and update the navigation while keeping the CSS and page structure. Remove optional elements that do not help the report.
2. Use the template as an HTML fragment only when a publishing tool explicitly requires one. Otherwise add a standards-compliant document wrapper with language, charset, viewport, title, and body elements.
3. Reconcile repeated numbers against their source table or calculation. Check totals, denominators, percentages, and displayed precision.
4. Run `python3 /path/to/scientific-report/scripts/validate_report.py REPORT.html`, resolving the script from this skill's directory. Fix all errors. Review warnings rather than suppressing them mechanically.
5. Read the finished report from top to bottom as a new reader. Confirm that each section explains its purpose, every exhibit is interpreted, specialist terms are defined or removed, and conclusions do not outrun the evidence.
6. Run the review passes below, then triage and apply their findings.

## Review passes

Review the finished report through each lens below before delivery. Each lens is independent — a finding from one should not be assumed to cover another.

If the environment provides a subagent or task-dispatch tool (for example Claude Code's `Agent` tool), launch one reviewer per lens in parallel. Give each reviewer only the report file, the lens description below, and read-only tools — it should return a short list of findings (location, issue, suggested fix) and make no edits itself. If no such tool is available, work through the same lenses yourself as separate sequential passes rather than one combined read; a single read-through tends to miss what a dedicated pass catches.

- **Clarity and interpretability.** Read as a new, non-specialist reader. Flag any claim that is not traceable to a specific exhibit, any undefined term or acronym, any sentence that needs a second read, and any place prose and exhibit drift apart.
- **Numerical/reporting consistency.** Check that every number is stated the same way everywhere it appears (value, precision, units). Recompute totals, denominators, and percentages against their source table. Flag any figure repeated with a different value or rounded inconsistently.
- **Statistical rigour and overclaiming.** Check that causal language is used only where the design supports it, that uncertainty is reported where meaningful and not manufactured where it is not, and that conclusions do not go beyond what the results section actually shows.
- **Reference checker.** Check that every major external claim (standard, vendor, dataset, prior result) has a citation, that citation numbers match their position in the reference list, and that no reference is unused or duplicated under a different number.
- **Table and figure reviewer.** Check that every table and figure renders correctly, sits close to its first mention, has consistent spacing from surrounding prose, and has a caption that is accurate, placed correctly (above tables, below figures), and does not duplicate a heading.

Fix clear errors directly. Use judgement on stylistic suggestions. Flag anything that depends on information only the user has (for example, a claim needing a citation you cannot find) rather than silently dropping it or inventing a source.

## Delivery

- When publishing through a tool, follow that tool's current document-wrapper and metadata requirements.
- Otherwise save a complete standalone HTML file and give the user its path.
- Keep the output self-contained and verify it in both light and dark themes when visual inspection is available.
