# test/sim — hand-run checks for the simulated arenas

These are scripts, not a test tier. Each is run on its own, under the **`[sim]`**
environment (`source env_setup.sh`; numpy<2, gym 0.26, pybullet, softgym), and
prints or renders what it checks. Nothing collects them:

- `make test-unit` discovers `test/unit/` only, and these could not import there,
  because the rig venv has none of the sim stack.
- They are named `check_*.py` rather than `test_*.py` so that `unittest discover`
  run from anywhere skips them. The robot repos do the same for hardware checks.
  The prefix was not simply dropped, because names like `raven.py` or
  `environment.py` would shadow real modules when a script is run directly.

They came from `test/*.py` and `tool/tests/`. Some already reference paths that
no longer exist, such as `../scripts/yamls/`, a config tree removed before they
moved. They are kept as a record of how each arena was exercised, not as a
guarantee that it still runs.

    python test/sim/check_raven.py
