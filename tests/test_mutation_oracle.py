"""Offline adversarial controls for the mutation oracle (no Lean required)."""
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

FILE = Path(__file__).resolve().parents[1] / "tools" / "check_v02_mutations.py"
spec = importlib.util.spec_from_file_location("mutation_oracle", FILE)
oracle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oracle)
ORIGINAL = "def checked : Bool := true\n\ntheorem gate_sound : checked = true := by\n  rfl\n"
OLD, NEW = "def checked : Bool := true", "def checked : Bool := false"


class MutationOracleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / "Example.lean"
        self.source.write_text(ORIGINAL)
        self.ledger = self.root / "result.json"

    def run_oracle(self, invoke):
        with patch.object(oracle, "ROOT", self.root), \
             patch.object(oracle, "LEDGER", self.ledger), \
             patch.object(oracle, "CASES", [("test", self.source, OLD, NEW)]), \
             patch.object(oracle, "EXPECTED", {"test": "gate_sound"}), \
             patch.object(oracle, "invoke", side_effect=invoke):
            result = oracle.main()
        return result, json.loads(self.ledger.read_text())

    @staticmethod
    def fake_lean(file):
        if OLD in file.read_text():
            return subprocess.CompletedProcess([], 0, "", "")
        return subprocess.CompletedProcess(
            [], 1, f"{file}:4:3: error: proof goal not discharged", "")

    def test_green_baseline_then_theorem_error(self):
        code, result = self.run_oracle(self.fake_lean)
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["cases"][0]["theorem_errors"][0]["line"], 4)

    def test_red_baseline_stops_mutation_campaign(self):
        calls = []
        def broken(file):
            calls.append(file.read_text())
            return subprocess.CompletedProcess([], 1, "", "missing toolchain")
        code, result = self.run_oracle(broken)
        self.assertEqual(code, 1)
        self.assertEqual(result["status"], "HARNESS_FAILURE")
        self.assertEqual(len(calls), 1)
        self.assertNotIn("mutant_exit", result["cases"][0])

    def test_always_green_checker_is_rejected(self):
        code, result = self.run_oracle(
            lambda file: subprocess.CompletedProcess([], 0, "", ""))
        self.assertEqual(code, 1)
        self.assertEqual(result["cases"][0]["status"], "SURVIVED")

    def test_import_error_does_not_count_as_kill(self):
        def broken(file):
            if OLD in file.read_text():
                return subprocess.CompletedProcess([], 0, "", "")
            return subprocess.CompletedProcess(
                [], 1, f"{file}:1:1: error: unknown module prefix", "")
        code, result = self.run_oracle(broken)
        self.assertEqual(code, 1)
        self.assertEqual(result["cases"][0]["status"], "INCONCLUSIVE")

    def test_wrong_file_error_does_not_count_as_kill(self):
        def broken(file):
            if OLD in file.read_text():
                return subprocess.CompletedProcess([], 0, "", "")
            return subprocess.CompletedProcess([], 1, "/tmp/Other.lean:4:1: error: bad", "")
        code, result = self.run_oracle(broken)
        self.assertEqual(code, 1)
        self.assertEqual(result["cases"][0]["status"], "INCONCLUSIVE")

    def test_stderr_is_preserved_in_receipt(self):
        def error_on_stderr(file):
            if OLD in file.read_text():
                return subprocess.CompletedProcess([], 0, "", "")
            return subprocess.CompletedProcess(
                [], 1, "", f"{file}:4:1: error: unsolved goals")
        code, result = self.run_oracle(error_on_stderr)
        self.assertEqual(code, 0)
        self.assertIn("unsolved goals", result["cases"][0]["mutant_stderr"])

    def test_baseline_and_mutant_share_exact_path(self):
        calls = []
        def record(file):
            calls.append((str(file), file.read_text()))
            return self.fake_lean(file)
        code, _ = self.run_oracle(record)
        self.assertEqual(code, 0)
        self.assertEqual(calls[0][0], calls[1][0])
        self.assertIn(OLD, calls[0][1])
        self.assertIn(NEW, calls[1][1])

    def test_ambiguous_source_target_is_harness_failure(self):
        self.source.write_text(ORIGINAL + "\n" + OLD)
        code, result = self.run_oracle(self.fake_lean)
        self.assertEqual(code, 1)
        self.assertEqual(result["status"], "HARNESS_FAILURE")


if __name__ == "__main__":
    unittest.main()
