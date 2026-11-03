# Local development

Install the development dependencies and activate the Git hooks after cloning:

```sh
uv sync --locked
uv run --locked pre-commit install
```

Every commit runs the full Python and notebook test suites locally. The notebook tests run serially because some examples use subprocesses and shared execution state. A failing test blocks the commit. Pre-commit tests the staged changes and temporarily stashes unstaged changes.

Run the hooks manually before committing:

```sh
uv run --locked pre-commit run --all-files
```

Run either suite separately:

```sh
uv run --locked pytest -q
uv run --locked nbdev-test --n-workers 0 --pause 1
```

GitHub Actions only builds and deploys the documentation on pushes to `main` or manual dispatch. The deployment runs `nbdev-docs` and publishes `_docs` to the `gh-pages` branch, which is the repository's existing Pages source. It does not run either test suite.

## GitHub releases with Fastship

Publish a reviewed current version from a clean `main` checkout. The package version is owned by the notebook source; regenerate exports and README before building. Existing release tags remain unchanged.

```sh
uv run --locked nbdev-export
uv run --locked nbdev-readme
uv run --locked pre-commit run --all-files
uv build
git tag -a 0.0.18 -m 'nbskill 0.0.18'
git push origin 0.0.18
uv run --locked python tools/release.py . dist/nbskill-0.0.18-py3-none-any.whl dist/nbskill-0.0.18.tar.gz --tag 0.0.18 --latest --publish
```

The publisher uses Fastship's `Release` for configuration, changelog notes and GitHub access. It verifies a clean checkout and that HEAD matches the local and remote tags, uploads every artifact to a draft, then publishes. Without `--publish`, the release stays a draft. Replace the version, tag and filenames together for each future release. Use an authenticated `gh` client and never store tokens in project files. `ship-release` also uploads to PyPI and is not used here.

Use `ship-pr` for a reviewed change intended for the default branch; it creates and immediately merges the pull request. Run the local checks before calling it. Consumers pin both `nbskill==0.0.18` and the matching GitHub source tag as shown in README, commit their lockfile, and use `uv sync --locked`.
