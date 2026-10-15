"""Tests for private-fork remote selection and safe, opt-in sync."""
import subprocess
import unittest
from unittest.mock import patch

from scripts import sync_progress


def result(out="", code=0, err=""):
    return subprocess.CompletedProcess([], code, out, err)


class SyncProgressTests(unittest.TestCase):
    def test_remote_parsing(self):
        for url in ("https://github.com/alice/az-900-tutor.git",
                    "git@github.com:alice/az-900-tutor.git",
                    "ssh://git@github.com/alice/az-900-tutor"):
            self.assertEqual(sync_progress.parse_remote(url), ("alice", "az-900-tutor"))
        self.assertIsNone(sync_progress.parse_remote("https://evil.example/alice/az-900-tutor"))
        self.assertIsNone(sync_progress.parse_remote("https://github.com/alice/other"))

    def test_reject_upstream_or_ambiguous_remotes(self):
        def fake_git(*args, **kwargs):
            if args == ("remote",):
                return result("origin\npersonal\n")
            return result("https://github.com/" + ("vmenezesdev" if args[-1] == "origin" else "alice") + "/az-900-tutor.git")
        with patch.object(sync_progress, "git", side_effect=fake_git):
            self.assertEqual(sync_progress.choose_remote(), ("personal", "alice", "az-900-tutor"))
            with self.assertRaisesRegex(ValueError, "Refusing"):
                sync_progress.choose_remote("origin")

    def test_private_fork_required(self):
        with patch.object(sync_progress.subprocess, "run", side_effect=[
            result('{"is_fork":true,"parent":"vmenezesdev/az-900-tutor","owner":"alice"}'),
            result("alice\n"), result("false\n")]):
            with self.assertRaisesRegex(ValueError, "public"):
                sync_progress.verify_fork("alice", "az-900-tutor")

    def test_dry_run_never_prepares_or_uploads(self):
        with patch.object(sync_progress, "choose_remote", return_value=("personal", "alice", "az-900-tutor")), \
             patch.object(sync_progress, "verify_fork", return_value="alice/az-900-tutor"), \
             patch.object(sync_progress, "prepare_payload", side_effect=AssertionError("read/upload forbidden")):
            self.assertEqual(sync_progress.sync("nonexistent.json")["status"], "dry_run")


if __name__ == "__main__":
    unittest.main()
