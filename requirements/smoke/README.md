# Smoke runs behind the pins

`../sim-py310.txt` is the environment in which every method repository's documented
entry points ran, briefly, without error. This directory is that check, so it can
be rerun after a pin moves.

    <root>/actoris_harena  JA-TN  PlaNet-ClothPick  LaGarNet  DRAPER  bimanual_garment_folding
    <root>/datasets/{all_garment_mix,all_garments_multi_primitive_alignment}

    bash actoris_harena/requirements/smoke/smoke_all.sh <root>          # all steps
    ONLY="planet_train planet_eval" bash .../smoke_all.sh <root>        # a rerun
    sbatch viking_smoke.sbatch                                          # on Viking

Each step runs the repository's own script through `smoke_run.py`, which cuts
evaluation and validation to one episode; `jatn_conf/` and
`lagarnet_run/configuration/` are the repositories' configs with tiny step counts.
Every step logs to `<root>/logs/<step>.log` and the run ends with PASS/FAIL per step.
The first step, `pyflex_render` (`pyflex_check.py`), builds a cloth arena, steps it
and fails on a blank frame. If it fails, every simulator step after it will too:
check `EGL_GPU` (README section 3) before anything else. It runs on its own too:
`source env.sh .; python pyflex_check.py`.

**Point the experiment trees away from real data.** bimanual's and PlaNet's
`resolve_save_root` pick a root per hostname (on Viking, the live experiment tree
in `/mnt/scratch`), so `smoke_all.sh` exports `SAVE_ROOT`. Garment tasks also
cache goals and keys into `assets/` and `data/cloth_funnel/init_states`; make
those a symlink farm (`cp -rs <real>/assets <root>/farm/assets`) so a run adds
files to the farm, never to the real tree.

Known, and not code: `imports_draper` fails on an EL8 cluster (pyrealsense2 needs
glibc >= 2.29; DRAPER runs on an Ubuntu robot PC), and `lagarnet_eval` stops at
pants, whose `multi-pants-*.hdf5` initial states were on neither test machine.
