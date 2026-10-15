"""Opt-in learner-progress sync to a verified personal GitHub fork.

Uses git CLI (no dependencies). Never writes progress to the upstream project.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from scripts import tutor
except ModuleNotFoundError:
    import tutor

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = "vmenezesdev/az-900-tutor"
PROGRESS_REF = "refs/heads/learner-progress"
PROGRESS_PATH = "state.json"


def git(*args, cwd=ROOT, check=True):
    result = subprocess.run(["git", *args], cwd=cwd, text=True, capture_output=True)
    if check and result.returncode:
        raise ValueError(f"Git command failed: git {args[0]} ({result.stderr.strip() or result.stdout.strip()})")
    return result


def parse_remote(url):
    """Return normalized GitHub owner/repo for common HTTPS and SSH remote forms."""
    match = re.fullmatch(
        r"(?:https://github\.com/|ssh://git@github\.com/|git@github\.com:)"
        r"([A-Za-z0-9-]+)/([A-Za-z0-9_.-]+?)(?:\.git)?/?", url.strip())
    return (match.group(1), match.group(2)) if match else None


def choose_remote(explicit=None):
    candidates = []
    remotes = git("remote").stdout.splitlines()
    if explicit and explicit not in remotes:
        raise ValueError(f"Remote {explicit!r} not configured")
    for name in ([explicit] if explicit else remotes):
        url = git("remote", "get-url", "--push", name).stdout.strip()
        parsed = parse_remote(url)
        if not parsed:
            if explicit:
                raise ValueError("Remote must be hosted on github.com")
            continue
        owner, repo = parsed
        if repo.lower() != "az-900-tutor" or owner.lower() == UPSTREAM.split("/")[0].lower():
            if explicit:
                raise ValueError("Refusing remote that is not a personal fork distinct from upstream")
            continue
        candidates.append((name, owner, repo))
    if not candidates:
        raise ValueError("No personal GitHub fork remote found. Add a fork remote and retry.")
    if len(candidates) > 1:
        raise ValueError("More than one fork remote found; pass --remote explicitly")
    return candidates[0]


def verify_fork(owner, repo):
    """gh api uses the current user's credentials; verify GitHub's parent metadata."""
    response = subprocess.run(
        ["gh", "api", f"repos/{owner}/{repo}", "--jq",
         "{is_fork: .fork, parent: .parent.full_name, owner: .owner.login}"],
        capture_output=True, text=True)
    if response.returncode:
        raise ValueError("Unable to verify fork with GitHub. Install/authenticate gh; no data uploaded.")
    try:
        info = json.loads(response.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid GitHub fork verification response") from exc
    if not info.get("is_fork") or info.get("parent", "").lower() != UPSTREAM.lower():
        raise ValueError("Remote is not a fork of the official AZ-900 Tutor repository")
    login = subprocess.run(["gh", "api", "user", "--jq", ".login"], capture_output=True, text=True)
    if login.returncode or login.stdout.strip().lower() != owner.lower() or info.get("owner", "").lower() != owner.lower():
        raise ValueError("Remote must belong to the authenticated learner, not another account")
    visibility = subprocess.run(["gh", "api", f"repos/{owner}/{repo}", "--jq", ".private"], capture_output=True, text=True)
    if visibility.returncode or visibility.stdout.strip() != "true":
        raise ValueError("Fork is public. Refusing to publish private learner evidence. Use a private fork or local export.")
    return f"{owner}/{repo}"


def prepare_payload(state_path):
    with tutor.state_lock(state_path):
        state = tutor.validate_state(tutor.read(state_path))
        return json.dumps(tutor.export_state(state), ensure_ascii=False, indent=2) + "\n"


def sync(state_path, remote=None, confirm=False):
    name, owner, repo = choose_remote(remote)
    target = verify_fork(owner, repo)
    if not confirm:
        return {"status": "dry_run", "remote": name, "repository": target,
                "branch": PROGRESS_REF, "message": "No upload. Pass --confirm to publish progress to the verified private fork."}
    payload = prepare_payload(state_path)
    # Temp orphan repository: keeps personal state completely out of the source working tree/index.
    with tempfile.TemporaryDirectory(prefix="az900-progress-") as directory:
        base = Path(directory)
        git("init", "-q", cwd=base)
        git("config", "user.name", "AZ-900 learner progress", cwd=base)
        git("config", "user.email", "learner-progress@users.noreply.github.com", cwd=base)
        git("remote", "add", "target", git("remote", "get-url", "--push", name).stdout.strip(), cwd=base)
        previous = git("fetch", "target", PROGRESS_REF, cwd=base, check=False)
        if previous.returncode == 0:
            git("checkout", "-q", "-b", "learner-progress", "FETCH_HEAD", cwd=base)
            existing = base / PROGRESS_PATH
            if existing.exists():
                old = tutor.import_state(json.loads(existing.read_text(encoding="utf-8")))
                current = tutor.import_state(json.loads(payload))
                if old != current and (len(old["events"]) > len(current["events"]) or any(e not in current["events"] for e in old["events"])):
                    raise ValueError("Remote has learner events missing locally. Resolve manually; refusing destructive overwrite.")
        else:
            # Do not confuse auth/network failures with a missing remote branch.
            probe = git("ls-remote", "--exit-code", "target", PROGRESS_REF, cwd=base, check=False)
            if probe.returncode not in (2,):
                raise ValueError("Could not establish whether progress branch exists; refusing upload")
            git("checkout", "-q", "--orphan", "learner-progress", cwd=base)
        (base / PROGRESS_PATH).write_text(payload, encoding="utf-8")
        git("add", "--", PROGRESS_PATH, cwd=base)
        staged = git("diff", "--cached", "--quiet", cwd=base, check=False)
        if staged.returncode == 0:
            return {"status": "unchanged", "repository": target, "branch": PROGRESS_REF}
        git("commit", "-qm", "Save learner progress", cwd=base)
        git("push", "target", f"HEAD:{PROGRESS_REF}", cwd=base)
    return {"status": "synced", "repository": target, "branch": PROGRESS_REF,
            "privacy": "Private fork only; GitHub account access still applies"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=ROOT / ".learner/state.json")
    parser.add_argument("--remote", help="Choose a specific personal fork remote")
    parser.add_argument("--confirm", action="store_true", help="Opt in to actual remote upload")
    args = parser.parse_args(argv)
    try:
        print(json.dumps(sync(args.state, args.remote, args.confirm), indent=2, ensure_ascii=False))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
