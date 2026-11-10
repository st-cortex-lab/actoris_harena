# Releasing actoris-harena to PyPI

`.github/workflows/publish.yml` builds the sdist and wheel and checks them:
`twine check --strict`, `tool/check_wheel.py`, and a `[rig]` install from the
wheel alone. Then it uploads them. Uploads use **trusted publishing**: PyPI
trusts this repository's workflow through OIDC, so no API token is stored.

## Once: register the publisher

Do this on both <https://test.pypi.org> and <https://pypi.org>, signed in as
the account that will own the project. Go to *Your projects → Publishing →
Add a new pending publisher*, choose GitHub, and enter:

| Field | TestPyPI | PyPI |
|---|---|---|
| PyPI project name | `actoris-harena` | `actoris-harena` |
| Owner | `st-cortex-lab` | `st-cortex-lab` |
| Repository name | `actoris_harena` | `actoris_harena` |
| Workflow name | `publish.yml` | `publish.yml` |
| Environment name | `testpypi` | `pypi` |

On GitHub, create the two environments of the same names under *Settings →
Environments*. To require an approval before the real upload, add a required
reviewer to `pypi`.

The first successful upload turns the pending publisher into the project's
publisher. Add co-maintainers on pypi.org afterwards.

## Each release

1. Bump `version` in `pyproject.toml` (for example `0.4.0` → `0.4.1`) on a
   branch, and merge it into `develop` and `main` as usual.
2. Tag `main` and push the tag. The tag must equal `v` + the version, or the
   build job refuses:

   ```bash
   git tag v0.4.1 main && git push origin v0.4.1
   ```

3. The workflow uploads to TestPyPI, then to PyPI. Check the release:

   ```bash
   python -m venv /tmp/check && /tmp/check/bin/pip install "actoris-harena[rig]==0.4.1"
   /tmp/check/bin/actoris-harena --help
   ```

To try the pipeline without releasing, run the workflow by hand
(*Actions → publish → Run workflow*). That uploads to TestPyPI only, and
`skip-existing` means rerunning it for an unchanged version is harmless.
A version cannot be uploaded twice to the same index, so a fix after a
release is always a new version number.
