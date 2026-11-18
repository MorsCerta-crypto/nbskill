# Local development

Use [WORKFLOW.md](WORKFLOW.md) for branch, review, and release policy. Install dependencies and hooks in this order after cloning.

```sh
uv sync --locked
uv run --locked pre-commit install
python3 .github/workflow_guard.py install
```

Run both suites with `uv run --locked pre-commit run --all-files`. The hooks run notebook tests serially because some cells use subprocesses and shared execution state. You can also run each suite separately.

```sh
uv run --locked pytest -q
uv run --locked nbdev-test --n-workers 0 --pause 1
```

GitHub Actions installs the locked environment under Python 3.13, runs both suites, and verifies that notebook exports match the committed package. The source policy runs as a separate check. [Checks](.github/workflows/test.yml) · [Source policy](.github/workflows/source-policy.yml)

## GitHub releases

Update `__version__` in `nbskill/__init__.py`, the installation pins in `nbs/index.ipynb`, and `CHANGELOG.md`. Regenerate exports and the README, then run the checks.

```sh
uv run --locked nbdev-export
uv run --locked nbdev-readme
uv run --locked pre-commit run --all-files
```

Open the pull request with the Fastship command in [DEV.md](DEV.md) and merge it after review and the required checks. From the clean, reviewed `main` checkout, verify the package version and that the remote tag is unused. Build once locally to check the distributions, then push the version tag.

```sh
version=$(uv run --locked python -c 'from importlib.metadata import version; print(version("nbskill"))')
uv build
git tag -a "$version" -m "nbskill $version"
git push origin "refs/tags/$version"
```

The [package release workflow](.github/workflows/package-release.yml) checks the tag against `main` and the package version, builds the wheel and source distribution, and attaches them to the GitHub release. Consumers update the package and tag pins together and commit their updated lockfiles.
