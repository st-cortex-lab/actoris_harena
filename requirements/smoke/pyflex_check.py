"""Does pyflex render on this machine? Exit 0 only if it does.

A bare ``pyflex.init`` can succeed and still render nothing, and a wrong EGL
device dies with a segfault rather than an error. So this builds a real SoftGym
cloth arena through ``actoris_harena`` (as the method repositories do), resets
it, takes a few random actions, and fails unless every RGB frame has content
and the cloth actually moved.

    source env.sh <any dir>; python pyflex_check.py [--arena <spec>] [--out f.png]
"""

import argparse
import os
import sys

import numpy as np
from dotmap import DotMap

DEFAULT = ("softgym|domain:rainbow-rectangular-fabrics,initial:crumpled,"
           "action:pixel-pick-and-place(1),task:flattening,disp:False")


def rgb_of(info):
    obs = info["observation"]
    rgb = obs["rgb"] if isinstance(obs, dict) else obs
    return np.asarray(rgb)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arena", default=DEFAULT)
    ap.add_argument("--steps", type=int, default=3)
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    print("EGL_GPU =", os.environ.get("EGL_GPU", "<unset>"))

    import actoris_harena as ah

    arena = ah.build_arena(a.arena, DotMap({"ray": False, "disp": False}))
    arena.set_eval()
    info = arena.reset({"eid": 0, "save_video": False})
    frames = [rgb_of(info)]
    rng = np.random.default_rng(0)
    for _ in range(a.steps):
        info = arena.step(rng.uniform(-0.8, 0.8, size=4).astype(np.float32))
        frames.append(rgb_of(info))

    stds = [float(f.std()) for f in frames]
    moved = float(np.abs(frames[-1].astype(float) - frames[0].astype(float)).mean())
    print("frame shape", frames[0].shape, "std per frame", [round(s, 1) for s in stds],
          "mean change", round(moved, 2))
    if a.out:
        import cv2
        cv2.imwrite(a.out, cv2.cvtColor(np.concatenate(frames, 1).astype(np.uint8),
                                        cv2.COLOR_RGB2BGR))
    if min(stds) < 1.0:
        sys.exit("FAIL: a frame is blank -- pyflex rendered nothing")
    if moved < 0.5:
        sys.exit("FAIL: the cloth did not move -- the simulation is not stepping")
    print("PASS: pyflex renders and simulates")


if __name__ == "__main__":
    main()
