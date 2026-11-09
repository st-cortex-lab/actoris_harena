"""Run a method repo's own entry script with evaluation and validation cut
to SMOKE_TRIALS episodes (default 1). Nothing in the repo is modified: the
wrap is applied to actoris_harena.api's evaluate/validate, which every
train/eval entry point reaches.

    python smoke_run.py path/to/script.py [script args...]
"""
import os
import runpy
import sys

N = int(os.environ.get("SMOKE_TRIALS", "1"))

import actoris_harena.api as api  # noqa: E402


def _cut(fn, getters):
    def wrapped(agent, arena, *a, **k):
        for g in getters:
            orig = getattr(arena, g)
            setattr(arena, g, lambda orig=orig: list(orig())[:N])
        return fn(agent, arena, *a, **k)
    wrapped.__wrapped__ = fn
    return wrapped


api.evaluate = _cut(api.evaluate, ["get_eval_configs"])
api.validate = _cut(api.validate, ["get_val_configs"])

script = os.path.abspath(sys.argv[1])
sys.argv = [script] + sys.argv[2:]
sys.path.insert(0, os.path.dirname(script))

# SMOKE_SET="module:attr=value;..." points a repo constant (a config dir) at
# the scratch copies without editing the repo.
import importlib  # noqa: E402

for item in filter(None, os.environ.get("SMOKE_SET", "").split(";")):
    target, value = item.split("=", 1)
    mod, attr = target.split(":")
    setattr(importlib.import_module(mod), attr, value)
print(f"[smoke] {script} with {N} eval/val trial(s)", flush=True)
runpy.run_path(script, run_name="__main__")
print("[smoke] OK", flush=True)
