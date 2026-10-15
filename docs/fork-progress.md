# Sync learner progress to your own fork

Local `.learner/state.json` remains the default and is gitignored. GitHub storage is **optional**, requires explicit consent, and is supported only when the authenticated learner owns a **private fork** of `vmenezesdev/az-900-tutor`.

Set up `git` and [GitHub CLI](https://cli.github.com/) (authenticated with `gh auth login`). Create a private fork when your GitHub account/policy permits one. Add it as a remote, for example:

```sh
git remote add personal git@github.com:YOUR_USERNAME/az-900-tutor.git
python scripts/tutor.py status
python scripts/sync_progress.py --remote personal
# Only after reviewing the target and accepting private GitHub storage:
python scripts/sync_progress.py --remote personal --confirm
```

The command verifies GitHub fork parent and authenticated ownership using `gh api`, refuses public forks, and writes to the separate `learner-progress` branch of **your** fork. It does not add `.learner/` to your code branch or send a PR to upstream. Your progress history can contain sensitive personal assessment responses, and a private GitHub repo is still a third-party service accessible to authorized GitHub collaborators. Do not use GitHub sync if private storage is not appropriate.

Sync is manual, never triggered just by discovering a remote. The command checks the remote before uploading and rejects missing/mismatched remote evidence; concurrent pushes can fail safely. Resolve differences rather than force-pushing. A failed push leaves your local state untouched. Git history remains in the private fork; deleting a local file does not remove its remote history.

To **resume** in a fresh clone, fetch the branch and import the verified export into a new local state path (do not overwrite an existing state):

```sh
git fetch personal learner-progress
git show FETCH_HEAD:state.json > learner-progress.json
python scripts/tutor.py --state .learner/state.json import learner-progress.json
rm learner-progress.json
```

This example assumes `.learner/state.json` does not exist. If it does, choose another path and reconcile evidence manually. The temporary `learner-progress.json` is sensitive; keep it out of version control and delete it after importing. A private export/import remains the portable fallback if GitHub is unavailable.
