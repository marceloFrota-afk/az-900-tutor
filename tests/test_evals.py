import importlib.util
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

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
