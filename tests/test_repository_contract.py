"""Validate the completed submission without API calls or model downloads."""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUBMISSION = ROOT / "report" / "individual"


class SubmissionContractTest(unittest.TestCase):
    def test_notebook_ran_and_is_clean(self):
        notebook = json.loads((SUBMISSION / "day01_lab.ipynb").read_text(encoding="utf-8"))
        code = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
        self.assertTrue(code)
        self.assertTrue(any(cell.get("outputs") for cell in code))
        self.assertTrue(all(not any(o.get("output_type") == "error" for o in cell.get("outputs", [])) for cell in code))
        source = "\n".join("".join(cell["source"]) for cell in code)
        self.assertNotIn("raise NotImplementedError", source)
        self.assertIsNone(re.search(r"sk-[A-Za-z0-9_-]{20,}", source))

    def test_report_is_consistent(self):
        report = json.loads((SUBMISSION / "lab1_report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["seed"], 1002)
        self.assertEqual(len(report["predictions"]), 10)
        self.assertTrue(report["checks"])
        self.assertTrue(all(report["checks"].values()))
        self.assertGreaterEqual(len(report["results"]), 5)
        self.assertNotIn("student_id", report)

    def test_written_report_exists(self):
        report = SUBMISSION / "2A202603371_NguyenVanDang.md"
        self.assertTrue(report.is_file())
        self.assertIn("AI log", report.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
