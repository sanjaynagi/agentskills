from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from unittest import TestCase, main

sys.path.insert(0, str(Path(__file__).parent))

from validate_report import validate


VALID_REPORT = """
<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Agreement analysis</title></head>
<body>
<header><h1>Repeat measurements were consistent</h1>
<p class="lede">This report tests agreement between repeated measurements.</p></header>
<section id="abstract"><p>We analysed 20 observations. Agreement was high.</p></section>
<section id="methods"><p>We included a sample of 20 observations from one dataset
using the published protocol<sup class="cite"><a href="#ref1">[1]</a></sup>.</p></section>
<section id="results"><p>Figure 1 shows all 20 observations. Table 1 gives their values.</p>
<div class="figure"><div role="img" aria-label="Twenty observations by agreement group"></div>
<p class="cap"><strong>Figure 1.</strong> Agreement group for 20 observations. Source: analysis.csv.</p></div>
<p class="cap table-cap"><strong>Table 1.</strong> Measurement values. Source: analysis.csv.</p>
<div class="table-wrap"><table><thead><tr><th scope="col">Group</th></tr></thead>
<tbody><tr><td>A</td></tr></tbody></table></div></section>
<section id="refs"><ol><li id="ref1">Published protocol.</li></ol>
<p><strong>Data provenance.</strong> Generated from analysis.csv, version 1.</p></section>
</body></html>
"""


class ValidateReportTests(TestCase):
    def run_validation(self, source: str) -> tuple[list[str], list[str]]:
        with TemporaryDirectory() as directory:
            report = Path(directory) / "report.html"
            report.write_text(source, encoding="utf-8")
            return validate(report)

    def test_valid_report_passes(self) -> None:
        errors, warnings = self.run_validation(VALID_REPORT)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_structural_problems_fail(self) -> None:
        source = VALID_REPORT.replace(
            '<section id="methods">',
            '<section id="methods"><a href="#missing">Broken</a><div id="results"></div>',
        ).replace("Agreement analysis", "REPORT TITLE")
        errors, _ = self.run_validation(source)
        combined = "\n".join(errors)
        self.assertIn("Duplicate IDs", combined)
        self.assertIn("Broken fragment links", combined)
        self.assertIn("Unreplaced template placeholder", combined)

    def test_em_dash_is_only_a_warning(self) -> None:
        errors, warnings = self.run_validation(VALID_REPORT.replace("Agreement was high.", "Agreement was high—consistently."))
        self.assertEqual(errors, [])
        self.assertTrue(any("em dash" in warning for warning in warnings))

    def test_uncited_exhibit_fails(self) -> None:
        source = VALID_REPORT.replace("Figure 1 shows all 20 observations. ", "")
        errors, _ = self.run_validation(source)
        self.assertIn("Figure 1 is not referenced outside its caption.", errors)

    def test_appendix_exhibit_numbers_are_supported(self) -> None:
        source = VALID_REPORT.replace(
            "</section>\n<section id=\"refs\">",
            '<p>Table A1 gives supporting values.</p>'
            '<p class="cap"><strong>Table A1.</strong> Supporting values. Source: appendix.csv.</p>'
            "</section>\n<section id=\"refs\">",
        )
        errors, _ = self.run_validation(source)
        self.assertEqual(errors, [])

    def test_uncited_appendix_exhibit_is_only_a_warning(self) -> None:
        source = VALID_REPORT.replace(
            "</section>\n<section id=\"refs\">",
            '<p class="cap"><strong>Table A1.</strong> Supporting values. Source: appendix.csv.</p>'
            "</section>\n<section id=\"refs\">",
        )
        errors, warnings = self.run_validation(source)
        self.assertEqual(errors, [])
        self.assertIn("Table A1 is not referenced outside its caption.", warnings)


if __name__ == "__main__":
    main()
