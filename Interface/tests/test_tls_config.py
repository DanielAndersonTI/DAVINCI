"""Tests for the optional extra CA bundle used behind TLS interception."""

import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "Experimento_Multiagente"))

from main_fewshot import _apply_ca_bundle  # noqa: E402


class CaBundleTests(unittest.TestCase):
	def setUp(self):
		self.temporary = tempfile.TemporaryDirectory()
		self.bundle = Path(self.temporary.name) / "extra.pem"
		self.bundle.write_text(
			"-----BEGIN CERTIFICATE-----\n-----END CERTIFICATE-----\n",
			encoding="utf-8",
		)

	def tearDown(self):
		self.temporary.cleanup()

	def test_sets_every_tls_variable_to_the_bundle(self):
		with patch.dict(os.environ, {"DAVINCI_CA_BUNDLE": str(self.bundle)}, clear=True):
			_apply_ca_bundle()
			for variable in ("SSL_CERT_FILE", "REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE"):
				self.assertEqual(os.environ[variable], str(self.bundle))

	def test_keeps_an_explicit_certificate_file(self):
		with patch.dict(
			os.environ,
			{"DAVINCI_CA_BUNDLE": str(self.bundle), "SSL_CERT_FILE": "caller.pem"},
			clear=True,
		):
			_apply_ca_bundle()
			self.assertEqual(os.environ["SSL_CERT_FILE"], "caller.pem")
			self.assertEqual(os.environ["REQUESTS_CA_BUNDLE"], str(self.bundle))

	def test_missing_bundle_leaves_the_environment_alone(self):
		missing = self.bundle.with_name("missing.pem")
		with patch.dict(os.environ, {"DAVINCI_CA_BUNDLE": str(missing)}, clear=True):
			with redirect_stdout(io.StringIO()):
				_apply_ca_bundle()
			self.assertNotIn("SSL_CERT_FILE", os.environ)
			self.assertNotIn("REQUESTS_CA_BUNDLE", os.environ)
			self.assertNotIn("CURL_CA_BUNDLE", os.environ)

	def test_absent_bundle_is_a_noop(self):
		with patch.dict(os.environ, {}, clear=True):
			_apply_ca_bundle()
			self.assertEqual(dict(os.environ), {})


if __name__ == "__main__":
	unittest.main()
