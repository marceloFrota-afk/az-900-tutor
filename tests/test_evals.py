import importlib.util
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
import json

spec = importlib.util.spec_from_file_location("eval_runner", Path(__file__).resolve().parents[1] / "evals/run.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class EvaluationTests(unittest.TestCase):
    def test_empty_run_never_passes_and_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "run.json"
            args = SimpleNamespace(output=path, condition="with-repository", model="synthetic-test")
            runner.prepare(args)
            result = runner.summarize(SimpleNamespace(input=path))
            self.assertEqual((result["passed"], result["failed"], result["not_evaluated"]), (0, 0, 10))
            with self.assertRaises(ValueError):
                runner.prepare(args)

    def test_missing_configuration_and_changed_prompts_cannot_pass(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "run.json"
            runner.prepare(SimpleNamespace(output=path, condition="baseline", model="synthetic-test"))
            run = runner.load(path)
            run.update(evaluator="synthetic judge", executed_at="2026-10-15")
            for row in run["cases"]:
                row["transcript"] = "Synthetic response; this fixture is not a model evaluation"
                for judgment in row["judgments"]:
                    judgment.update({"pass": True, "evidence": "synthetic fixture"})
            path.write_text(json.dumps(run), encoding="utf-8")
            self.assertEqual(runner.summarize(SimpleNamespace(input=path))["passed"], 0)
            run["model_settings"] = "Synthetic fixture, no model called"
            run["cases"][0]["learner_prompt"] = "artificially easier prompt"
            path.write_text(json.dumps(run), encoding="utf-8")
            result = runner.summarize(SimpleNamespace(input=path))
            self.assertEqual(result["not_evaluated"], 1)
            self.assertEqual(result["passed"], 9)
