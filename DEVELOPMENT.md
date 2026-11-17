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

Merge the reviewed version change into `development`, then open a pull request from `development` to `main` and use a merge commit. Build and publish from the clean `main` checkout after its checks pass. Authenticate with `gh` and verify that the version is the intended new release and its tag is unused.

```sh
version=$(uv run --locked python -c 'from importlib.metadata import version; print(version("nbskill"))')
uv build
git tag -a "$version" -m "nbskill $version"
git push origin "refs/tags/$version"
uv run --locked python tools/release.py . \
  "dist/nbskill-$version-py3-none-any.whl" "dist/nbskill-$version.tar.gz" \
  --tag "$version" --latest --publish
```

The publisher verifies the local and remote tag against `HEAD` and uploads both artifacts before publishing the GitHub release. Omit `--publish` to keep a draft. Consumers update the package and tag pins together and commit their updated lockfiles.
