"""Tests for configuration and AI metadata in both PDF reports."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import Interface.server as server_module


RUN = {
	"run_id": "metadata-demo",
	"generated_at": "2026-11-23 12:00:00",
	"configuration": "c1",
	"ai_label": "DeepSeek (deepseek-chat)",
	"systems": [{"system_name": "Metadata Demo"}],
	"proposals": [{
		"system": "Metadata Demo",
		"agent_a": "Microservice,Responsibilities,Communicates With\nOrder Service,Manage orders,",
		"agent_b": "Microservice,Responsibilities,Communicates With\nOrder Service,Manage orders,",
		"consolidated": "Microservice,Responsibilities,Communicates With\nOrder Service,Manage orders,",
		"specification": "services:\n  - name: Order Service\n    responsibilities:\n      - Manage orders",
	}],
	"service_metrics": [
		{"system": "Metadata Demo", "proposal": "Consolidated", "precision": 1.0, "recall": 1.0, "f1_score": 1.0},
	],
	"interaction_metrics": [],
	"best_results": [{"system": "Metadata Demo", "best_services": "Consolidated (F1 1.0000)", "best_interactions": "-"}],
}


class PdfMetadataTests(unittest.TestCase):
	def test_full_report_prints_configuration_and_ai(self):
		pdf = server_module.build_pdf_report(RUN)
		self.assertTrue(pdf.startswith(b"%PDF-"))
		self.assertIn(b"Configuration: C1", pdf)
		self.assertIn(b"AI: DeepSeek \\(deepseek-chat\\)", pdf)
		self.assertIn(b"SYSTEM: Metadata Demo", pdf)

	def test_specification_pdf_prints_configuration_and_ai(self):
		pdf = server_module.build_pdf_specification(RUN)
		self.assertTrue(pdf.startswith(b"%PDF-"))
		self.assertIn(b"Configuration: C1", pdf)
		self.assertIn(b"AI: DeepSeek \\(deepseek-chat\\)", pdf)

	def test_run_without_metadata_prints_not_recorded(self):
		legacy = {**RUN}
		legacy.pop("configuration")
		legacy.pop("ai_label")
		pdf = server_module.build_pdf_report(legacy)
		self.assertIn(b"Configuration: not recorded", pdf)
		self.assertIn(b"AI: not recorded", pdf)

	def test_no_key_value_is_printed(self):
		secret = "sk-metadata-secret-value"
		run = {**RUN, "key_label": "Key 1", "provider": "deepseek"}
		report = server_module.build_pdf_report(run)
		specification = server_module.build_pdf_specification(run)
		self.assertNotIn(secret.encode(), report)
		self.assertNotIn(secret.encode(), specification)
		self.assertNotIn(b"Key 1", report)


class PersistedMetadataTests(unittest.TestCase):
	def make_run_dir(self, root, metadata=None):
		run_dir = root / "metadata demo" / "result_generalized_fewshot" / "run_20261123_120000_000000"
		run_dir.mkdir(parents=True)
		(run_dir / "proposta_a.csv").write_text(
			"Microservice,Responsibilities,Communicates With\nSaved A,Own A,B",
			encoding="utf-8",
		)
		(run_dir / "consolidada.csv").write_text(
			"Microservice,Responsibilities,Communicates With\nSaved Final,Own Final,A",
			encoding="utf-8",
		)
		if metadata is not None:
			(run_dir / "interface_run.json").write_text(json.dumps(metadata), encoding="utf-8")
		with patch.object(server_module, "RESULTS_DIR", root):
			report_run = server_module._persisted_report_run()
		return report_run, run_dir

	def test_restored_run_reads_configuration_and_ai_from_metadata(self):
		with tempfile.TemporaryDirectory() as temporary_dir:
			root = Path(temporary_dir)
			report_run, _ = self.make_run_dir(root, {
				"configuration": "c4",
				"provider": "gemini",
				"ai": "Gemini (gemini-flash-latest)",
				"model": "gemini-flash-latest",
				"key_label": "Key 2",
			})
		self.assertIsNotNone(report_run)
		self.assertEqual(report_run["configuration"], "c4")
		self.assertEqual(report_run["ai_label"], "Gemini (gemini-flash-latest)")
		self.assertEqual(report_run["systems"], [{"system_name": "metadata demo", "mode": "c4"}])
		pdf = server_module.build_pdf_report(report_run)
		self.assertIn(b"Configuration: C4", pdf)
		self.assertIn(b"AI: Gemini \\(gemini-flash-latest\\)", pdf)
		self.assertNotIn(b"Key 2", pdf)

	def test_restored_run_without_metadata_prints_not_recorded(self):
		with tempfile.TemporaryDirectory() as temporary_dir:
			root = Path(temporary_dir)
			report_run, _ = self.make_run_dir(root)
		self.assertIsNotNone(report_run)
		self.assertEqual(report_run["systems"], [{"system_name": "metadata demo"}])
		pdf = server_module.build_pdf_report(report_run)
		self.assertIn(b"Configuration: not recorded", pdf)
		self.assertIn(b"AI: not recorded", pdf)


if __name__ == "__main__":
	unittest.main()
