# Keeping this fork current

The Sync upstream GitHub Action checks `jmfernandes/robin_stocks`'s `master`
branch daily at 12:23 UTC, and can also be run manually from the Actions tab.
GitHub may delay scheduled runs or disable schedules after 60 days without
repository activity; re-enable the workflow in Actions if necessary.

It merges upstream into this fork's `master`, installs the merged package,
and runs `tests/test_fork_compatibility.py` before pushing. It never resets
the fork or force-pushes. Existing custom commits remain in history.
Git follows the package directory rename when merging upstream additions.
New upstream Python files and imports are adapted from `robin_stocks` to
`calcap_robin_stocks` by `tools/normalize_upstream.py`. Namespace collisions
stop the run for manual resolution.

A merge conflict, failed test, or rejected push stops the workflow without
changing the remote branch. Review failed runs in Actions, resolve conflicts
locally, run the offline checks, and push the resolution. Changes that Git can
merge automatically may still require review; these checks cover Calcap's
custom filtering and transfer pagination, not all Robinhood API behavior.

Local check (no brokerage credentials or API access required):

```sh
python -m unittest discover -s tests -p test_fork_compatibility.py -v
```

Calcap uses an editable local submodule, so remote updates do not automatically
update a running checkout. Pull this fork's `master` inside `robin_stocks_src`,
then commit the updated submodule pointer in the parent Calcap repository.
