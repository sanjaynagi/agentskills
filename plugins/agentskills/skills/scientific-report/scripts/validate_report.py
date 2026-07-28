#!/usr/bin/env python3
"""Validate structural and interpretability requirements of a scientific report."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


PLACEHOLDERS = (
    "REPORT TITLE",
    "ORGANISATION",
    "Report subtitle",
    "Report category",
    "A headline finding",
    "Specialist term",
    "where the data came from",
)
EXHIBIT_RE = re.compile(r"\b(Table|Figure)\s+([A-Z]\d+|\d+[a-z]?)\b", re.IGNORECASE)
REF_ID_RE = re.compile(r"ref(\d+)$")


class ReportParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.fragment_links: list[str] = []
        self.external_resources: list[str] = []
        self.captions: list[str] = []
        self.text_chunks: list[str] = []
        self.narrative_chunks: list[str] = []
        self.abstract_text: list[str] = []
        self.table_header_scopes: list[str | None] = []
        self.tables = 0
        self.in_caption = 0
        self.in_abstract = 0
        self.section_stack: list[str | None] = []
        self.caption_buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = dict(attrs_list)
        if element_id := attrs.get("id"):
            self.ids.append(element_id)
        if tag == "section":
            section_id = attrs.get("id")
            self.section_stack.append(section_id)
            if section_id == "abstract":
                self.in_abstract += 1
        if tag == "a" and (href := attrs.get("href", "")).startswith("#"):
            self.fragment_links.append(href[1:])
        if tag in {"img", "script", "link", "iframe", "video", "audio", "source"}:
            url = attrs.get("src") or attrs.get("href")
            if url and urlparse(url).scheme in {"http", "https"}:
                self.external_resources.append(url)
        if tag == "p" and "cap" in attrs.get("class", "").split():
            self.in_caption += 1
            self.caption_buffer = []
        if tag == "table":
            self.tables += 1
        if tag == "th":
            self.table_header_scopes.append(attrs.get("scope"))

    def handle_endtag(self, tag: str) -> None:
        if tag == "section" and self.section_stack:
            section_id = self.section_stack.pop()
            if section_id == "abstract":
                self.in_abstract -= 1
        if tag == "p" and self.in_caption:
            self.captions.append(" ".join(self.caption_buffer).strip())
            self.caption_buffer = []
            self.in_caption -= 1

    def handle_data(self, data: str) -> None:
        clean = " ".join(data.split())
        if not clean:
            return
        self.text_chunks.append(clean)
        if self.in_caption:
            self.caption_buffer.append(clean)
        else:
            self.narrative_chunks.append(clean)
        if self.in_abstract:
            self.abstract_text.append(clean)


def exhibit_sequence(labels: list[str], kind: str) -> list[str]:
    return [number.lower() for label, number in labels if label.lower() == kind.lower()]


def sequence_errors(numbers: list[str]) -> list[str]:
    errors: list[str] = []
    groups: dict[str, list[int]] = {}
    for number in numbers:
        match = re.fullmatch(r"([a-z]?)(\d+)([a-z]?)", number, re.IGNORECASE)
        if not match:
            errors.append(number)
            continue
        prefix, base, _ = match.groups()
        groups.setdefault(prefix.upper(), []).append(int(base))
    for prefix, values in groups.items():
        first_occurrences = list(dict.fromkeys(values))
        if first_occurrences != list(range(1, max(first_occurrences) + 1)):
            label = f"appendix {prefix}" if prefix else "main"
            errors.append(f"{label}: {', '.join(map(str, first_occurrences))}")
    return errors


def validate(path: Path) -> tuple[list[str], list[str]]:
    source = path.read_text(encoding="utf-8")
    parser = ReportParser()
    try:
        parser.feed(source)
        parser.close()
    except Exception as exc:
        return [f"HTML could not be parsed: {exc}"], []

    errors: list[str] = []
    warnings: list[str] = []
    id_counts = Counter(parser.ids)
    duplicate_ids = sorted(element_id for element_id, count in id_counts.items() if count > 1)
    if duplicate_ids:
        errors.append(f"Duplicate IDs: {', '.join(duplicate_ids)}")

    missing_targets = sorted(set(parser.fragment_links) - set(parser.ids))
    if missing_targets:
        errors.append(f"Broken fragment links: {', '.join('#' + item for item in missing_targets)}")

    if parser.external_resources:
        errors.append("External resources violate self-containment: " + ", ".join(parser.external_resources))

    for placeholder in PLACEHOLDERS:
        if placeholder.casefold() in source.casefold():
            errors.append(f"Unreplaced template placeholder: {placeholder!r}")

    if not re.search(r'class=["\'][^"\']*\blede\b', source):
        warnings.append("No title-block lede found.")
    if not re.search(r"\b(data provenance|underlying data|source data)\b", source, re.IGNORECASE):
        errors.append("No explicit data-provenance statement found.")
    if not re.search(r"<th\b[^>]*\bscope=[\"'](?:col|row)[\"']", source, re.IGNORECASE):
        if parser.tables:
            warnings.append("Tables have no scoped header cells.")
    elif any(scope not in {"col", "row", "colgroup", "rowgroup"} for scope in parser.table_header_scopes):
        warnings.append("One or more table headers lack a valid scope attribute.")

    caption_labels: list[tuple[str, str]] = []
    for caption in parser.captions:
        match = EXHIBIT_RE.search(caption)
        if not match:
            errors.append(f"Caption lacks a Table/Figure number: {caption[:80]!r}")
            continue
        caption_labels.append((match.group(1), match.group(2)))
        if "source:" not in caption.casefold():
            warnings.append(f"Exhibit caption has no source: {match.group(1)} {match.group(2)}")

    for kind in ("Table", "Figure"):
        numbers = exhibit_sequence(caption_labels, kind)
        if len(numbers) != len(set(number.casefold() for number in numbers)):
            errors.append(f"Duplicate {kind.lower()} numbers in captions.")
        if problems := sequence_errors(numbers):
            errors.append(f"{kind} numbering is not sequential from 1 ({'; '.join(problems)}).")

    full_text = " ".join(parser.text_chunks)
    narrative_text = " ".join(parser.narrative_chunks)
    for kind, number in caption_labels:
        mentions = re.findall(rf"\b{re.escape(kind)}\s+{re.escape(number)}\b", narrative_text, re.IGNORECASE)
        if not mentions:
            message = f"{kind} {number} is not referenced outside its caption."
            if number[0].isalpha():
                warnings.append(message)
            else:
                errors.append(message)

    abstract = " ".join(parser.abstract_text)
    if re.search(r"\[\d+\]", abstract):
        errors.append("The abstract contains a numbered citation.")

    ref_ids = sorted(int(match.group(1)) for item in parser.ids if (match := REF_ID_RE.fullmatch(item)))
    cited_refs = sorted({int(number) for number in re.findall(r'href=["\']#ref(\d+)["\']', source)})
    if ref_ids != cited_refs:
        errors.append(f"Reference IDs and citations differ: listed={ref_ids}, cited={cited_refs}")

    dash_count = source.count("—")
    if dash_count:
        warnings.append(f"Found {dash_count} em dash(es); keep only where clearer than simpler punctuation.")

    if not re.search(r"\b(denominator|out of|n\s*=|sample|observations?|records?|rows?)\b", full_text, re.IGNORECASE):
        warnings.append("No obvious analysis population or denominator found; confirm that quantities are interpretable.")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    if not args.report.is_file():
        parser.error(f"not a file: {args.report}")

    errors, warnings = validate(args.report)
    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARNING: {message}")
    if errors:
        print(f"\nValidation failed with {len(errors)} error(s) and {len(warnings)} warning(s).")
        return 1
    print(f"Validation passed with {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
