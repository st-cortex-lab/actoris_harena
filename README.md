# Actoris Harena

**Authors:** Halid Abdulrahim Kadi (Lead), Dr Kasim Terzić (PhD Supervisor), and Dr John Oyekan (Postdoc Advisor)

*University of St Andrews, UK* and *University of York, UK*

> **Note:** This project was formerly called **Agent Arena**. It was renamed **Actoris Harena** (Latin for "The Actor's Arena") to avoid a naming conflict.

[![DOI](https://zenodo.org/badge/933415395.svg)](https://doi.org/10.5281/zenodo.14876793)
[![ArXiv](https://img.shields.io/badge/ArXiv-2504.06468-b31b1b.svg)](https://arxiv.org/abs/2504.06468)

![Actoris Harena Plot](https://raw.githubusercontent.com/st-cortex-lab/actoris_harena/main/assets/agent-arena.jpg)

The shared robot-learning framework of the St CORTEX Lab. Robot repositories
use it to collect, curate, train and deploy. Research repositories use it to
run control algorithms on simulated benchmarks.

![Recording on the dual SO-101 rig, then curating and replaying an episode in the console](https://raw.githubusercontent.com/st-cortex-lab/actoris_harena/main/documents/media/rig_collection_console.gif)

*Real-rig data collection and visualisation. First, an episode recorded on the
dual SO-101 rig, with every camera stream and each joint's follower reading
beside its command. Then the [console](#4-the-console) browsing a collection
drive and replaying a UR3e episode: RGB, depth, joint state and command, and
per-joint velocity and acceleration over the whole episode.*

For ROS 1 Noetic and ROS 2 Humble, see [With ROS](#with-ros) in section 3.

---

1. [What this is](#1-what-this-is)
2. [Install it for a robot repository](#2-install-it-for-a-robot-repository)
3. [Install it for the simulated arenas](#3-install-it-for-the-simulated-arenas)
4. [The console](#4-the-console)
5. [Using the simulated arenas](#5-using-the-simulated-arenas)
6. [Tests and lint](#6-tests-and-lint)
7. [Where things are](#7-where-things-are)
8. [Compatibility with the repositories that use it](#8-compatibility-with-the-repositories-that-use-it)
9. [Where the rig pipeline came from](#9-where-the-rig-pipeline-came-from)

---

## 1. What this is

One package, `actoris_harena`, with **two bodies of code whose dependencies
cannot be installed together**:

| | The rig pipeline | The simulated arenas |
|---|---|---|
| What | recording, dataset curation, VLA training, policy deployment, the browser console, the policies the lab trains | Agent/Arena benchmark framework: SoftGym cloth, Ravens, dm_control, gym, and about twenty-five agents |
| Used by | `so101_garment`, `ur3e_raven` | `bimanual_garment_folding`, `learning_garment_manipulation`, `JA-TN`, `PlaNet-ClothPick`, `softgym` |
| Runs beside | LeRobot: numpy>=2.0,<2.3, Python>=3.12 | numpy<2.0, gym 0.26.2, robosuite 1.4.1 |
| Extra | `[rig]` | `[sim]` (+ `[torch]`) |

pip cannot satisfy both sets of pins in one environment, so install exactly
one. `import actoris_harena` is lazy for the same reason: a robot's venv can
import `actoris_harena.recording` without the sim stack.

## 2. Install it for a robot repository

The package has **no venv of its own**. It installs editable into the robot
repo's venv, because that venv pins the LeRobot checkout and the hardware
libraries. Clone it beside the robot repo, on `develop`:

```bash
git clone -b develop https://github.com/st-cortex-lab/actoris_harena.git ../actoris_harena
<rig>/venv/bin/pip install -e "../actoris_harena[rig]"
# a rig with a RealSense also:
<rig>/venv/bin/pip install -e "../actoris_harena[rig,realsense]"
```

`ur3e_raven/install.sh` does this for you. Being editable, the robot repo
imports whatever branch is checked out here.

To use the pipeline without changing it, install the release from PyPI into
the same venv instead:

```bash
pip install "actoris-harena[rig]"            # or "actoris-harena[rig,realsense]"
```

A rig **declares** its facts once, at import: camera profile, recording
config, training destinations, gripper columns. The package refuses, rather
than guessing, until it has been told (see `src/common/rig_profile.py` in
either robot repo).

## 3. Install it for the simulated arenas

Use Linux with a GPU. Running on a CPU is strictly not recommended. It has been
validated on Ubuntu 20.04, 22.04 and 24.04.

Install from the pinned lock, `requirements/sim-py310.txt`. It is the newest set
that holds numpy<2, gym 0.26 and Python 3.10 (pyflex is built for cp310), and every
method repository's smoke run in section 8 passes against exactly these versions:

```bash
conda create --name harena-sim python=3.10 -y
conda activate harena-sim
pip install -r requirements/sim-py310.txt     # or requirements/<method>.txt, below
pip install -e . --no-deps
python -c "import actoris_harena, os; print(os.environ['RAVENS_ASSETS_DIR'])"
```

`requirements/` holds one file per method repository: `ja-tn.txt`,
`planet-clothpick.txt`, `lagarnet.txt`, `magpie.txt` (bimanual_garment_folding) and
`draper.txt`. Each is the lock plus what that repository imports on top. The header
of `sim-py310.txt` says why each ceiling is where it is: torch 2.12.1, opencv 4.11,
and open3d 0.18 (newer wheels need glibc 2.31 and will not install on an EL8 cluster).

Without a clone, `pip install "actoris-harena[sim,torch]"` installs the PyPI
release; from a clone, `pip install -e ".[sim,torch]"` does the same. On Python
3.10+ either way's direct pins are the lock's, but only the lock also pins every
transitive dependency, so prefer it.
`[torch]` alone is what older sim consumers' READMEs and Docker images install.

**pyflex must render on the NVIDIA GPU.** Headless, it renders through EGL on
the device `EGL_GPU` names. Without it, EGL picks its default display, which on
a desktop session (Wayland especially) or a hybrid-GPU laptop is Mesa, and pyflex
segfaults. The lab's SoftGym `setup.sh` sets `EGL_GPU` to the NVIDIA device of the
first visible CUDA GPU (`PyFlex/egl_device.py`), and so does `env_setup.sh`. To
check a machine:

```bash
source requirements/smoke/env.sh .    # or your repo's setup.sh
python requirements/smoke/pyflex_check.py   # builds a cloth arena, steps it, checks frames
```

A pyflex window (`disp:True`) goes through GLX instead, so it also needs
`__GLX_VENDOR_LIBRARY_NAME=nvidia __NV_PRIME_RENDER_OFFLOAD=1`, which
`env_setup.sh` also sets.

**SoftGym** (skip it if you don't need it): use the lab's modified version.

1. Clone [halid1020/softgym, branch py3.10](https://github.com/halid1020/softgym/tree/py3.10).
2. Follow its [setup tutorial](https://github.com/halid1020/softgym/blob/py3.10/README.md). Its Docker container only *compiles* the simulator; run experiments outside it.
3. Download the initial-state data files it names.

**Other benchmarks:** install them as they instruct, and wrap each one in an
adapter class that implements the `Arena` interface.

### With ROS

ROS is installed from the OS packages, and its Python must match the env:

| ROS | OS | Python | Env |
|---|---|---|---|
| ROS 2 Humble | Ubuntu 22.04 | 3.10 | `harena-sim`, from the lock (above) |
| ROS 1 Noetic | Ubuntu 20.04 | 3.8 | `pip install -e ".[sim,torch]"` in a python=3.8 env, which takes the package's `python_version < '3.10'` pins |

```bash
conda activate harena-sim            # or the python 3.8 env, for Noetic
source /opt/ros/humble/setup.bash    # or /opt/ros/noetic/setup.bash
```

DRAPER's UR3e machine is set up this way, on Humble. The old `ros1-noetic` and
`ros2-humble` branches used RoboStack conda env files. RoboStack no longer
builds either distro for Python 3.10, which pyflex needs, so those branches are
merged and retired.

## 4. The console

One browser page for every robot on the machine. It imports no hardware code:
anything that touches a device runs as a subprocess, under that rig's own
interpreter.

```bash
actoris-harena rigs add ../so101_garment     # a directory holding a rig.yaml
actoris-harena rigs list
actoris-harena console --port 8000 [--rig so101] [--dir <collection dir>]
```

Each rig declares what the console may start in its `rig.yaml`: its
interpreter, its agent and teleop scripts, its cameras and its schema. The
optional `session` block lists the inputs, sensor view and execute flag its
teleop accepts.

## 5. Using the simulated arenas

```python
import actoris_harena as ah

config = ah.retrieve_config("planet-clothpick", "<arena spec>", "default")  # packaged configs
arena = ah.build_arena("<arena spec>", config)
agent = ah.build_agent("planet-clothpick", config, save_dir="results")
ah.train_and_evaluate_single(agent, arena, validation_interval=1000, total_update_steps=100_000)
```

Each consumer registers its own classes with `ah.register_agent(name, cls)` and
`ah.register_arena(name, cls)` before calling `build_*`. A name that is not
registered, given `config.oracle=True`, is built by the oracle builder.

## 6. Tests and lint

The tiers are listed cheapest first, as in the robot repos. They run through a
rig's interpreter: given `PY=`, or the first sibling `../*/venv` that can import
the package.

```bash
make test-unit          # test/unit: pure Python, ~30 s
make test-integration   # test/integration: builds real models
RIG_OUTPUT_DIR=~/Projects/so101_garment/outputs make test-integration   # + the checkpoint test
make lint               # pre-commit: black, isort, flake8, mypy, then test-unit
make check-wheel        # builds a real wheel and checks it carries every data file
```

Linting covers the rig pipeline only. It deliberately leaves out the ~64k-line
sim tree, whose history is shared with the dataset and ROS branches. The sim
checks in `test/sim/` are run by hand, under `[sim]`.

## 7. Where things are

```
actoris_harena/
  recording/ training/ analysis/ deploy/ web/ policies/    the rig pipeline
  rigs.py cli.py sync.py outputs.py action_layout.py
  agent/ arena/ utilities/ configuration/ registration/    the simulated arenas
  api.py                                                    the sim entry points
test/unit/ test/integration/                                the rig pipeline's tiers
test/sim/                                                   hand-run sim checks
tool/                                                       scripts (mostly sim)
conf/                                                       Hydra configs for tool/hydra_*.py
documents/                                                  sim notes, the retired npz pipeline
```

`CLAUDE.md` is the detailed, file-by-file guide.

## 8. Compatibility with the repositories that use it

These repositories build on this package. **None of them pins it.** Each one
installs a sibling `../actoris_harena` checkout in editable mode, so whatever
branch is checked out here is what they run.

| Repository | Side | How it installs this package | What it imports |
|---|---|---|---|
| [`so101_garment`](https://github.com/st-cortex-lab/so101_garment) | rig | `hpc/provision_create.sh`: `pip install -e "../actoris_harena[rig]"` | `recording.*`, `training.*`, `analysis.*`, `deploy.*`, `policies.*` (and the `harena_*`/`so101_*` registry names), `web.*`, `sync`, `action_layout` |
| [`ur3e_raven`](https://github.com/st-cortex-lab/ur3e_raven) | rig + sim | `install.sh`/`install.ps1` from `install.env` (`HARENA_BRANCH=develop`, `[rig]`) | `recording.*`, `training.destinations`, `web.session`, `outputs`, `action_layout`; the Ravens/Transporter code in `agent.bc.transporter.*`, `agent.*`, `arena.*`, `utilities.transform`; and `import actoris_harena` for the `RAVENS_ASSETS_DIR` it sets |
| `bimanual_garment_folding` (MAGPIE) | sim | `requirements/magpie.txt` | the top-level names, `api.*` (incl. `train_and_evaluate`), `utilities.*`, `torch_utils`, `agent.{MPC_CEM,utilities.utils,oracle.builder,drl.sac.*}`, `registration.dataset`; it reads `actoris_harena_PATH` |
| `learning_garment_manipulation` | sim | Dockerfile: `uv pip install -e ".[torch]"` on `develop` | a subset of the above |
| [`JA-TN`](https://github.com/st-cortex-lab/JA-TN) | sim | `requirements/ja-tn.txt` | `TrainableAgent`, `retrieve_config(config_dir=…)`, `build_*`, `evaluate`, `train_and_evaluate`, `utilities.{trajectory_dataset,networks.utils}`, `arena.raven.tasks` |
| [`PlaNet-ClothPick`](https://github.com/st-cortex-lab/PlaNet-ClothPick) | sim | `requirements/planet-clothpick.txt` | `Arena`, `Task`, `RLAgent`, `api.*`, `torch_utils`, `registration.dataset`, `agent.*`, `utilities.*` |
| [`LaGarNet`](https://github.com/st-cortex-lab/LaGarNet) | sim + real | `requirements/lagarnet.txt` | `TrainableAgent`, `api.*` with spec-string arenas, `agent.utilities.torch_utils`, `utilities.{trajectory_dataset,perform_parallel,visual_utils,transform.*,utils}`, `registration.dataset` |
| [`DRAPER`](https://github.com/st-cortex-lab/DRAPER) | real (ROS 2) | `requirements/draper.txt` | `retrieve_config`, `build_agent`, `utilities.visual_utils` |
| [`softgym`](https://github.com/st-cortex-lab/softgym) | sim | none (a lazy import) | `agent.oracle.rect_fabric.real2sim_smoothing` |

`requirements/smoke/` runs each sim repository's documented entry points, on tiny
configs, against `requirements/sim-py310.txt`; every one passed there on a
workstation and on Viking before the lock was written (its README lists the two
known, data-only exceptions). Rerun it before moving a pin.

`test/unit/test_consumer_surface.py` lists every `(module, name)` these
repositories import. It fails if any of them stops resolving. **To move or
rename something, update the callers first, then that table.** It cannot check
these other promises:

- **Install names:** the `[rig]`, `[sim]`, `[torch]` and `[realsense]` extras,
  the `actoris-harena` script, and `requirements/<method>.txt`, which the method
  repositories' READMEs install from.
- **Environment:** `import actoris_harena` sets `ACTORIS_HARENA_PATH`,
  `RAVENS_ASSETS_DIR` and `DEFORMABLE_RAVEN_ASSETS_DIR`, plus the lowercase alias
  `actoris_harena_PATH` that callers' code reads.
- **Configs:** `retrieve_config(agent, arena, name)` resolves
  `configuration/train_and_evaluate/<agent>/<arena>/<name>.yaml`. Here `<arena>`
  is a spec string such as `softgym|domain:…`, which is why about 240 config
  files have `|`, `:` and `()` in their names and cannot be renamed.
- **Behaviour:**
  - `build_agent` with `config.oracle=True` goes to `OracleBuilder`.
  - `build_arena("softgym|domain:…")` builds from the spec string through
    `ArenaBuilder` when the name is not a registered arena, as before c061b3c.
  - `Arena.set_log_dir(logdir)` works with one argument.
  - `train_and_evaluate` hands `agent.train` the arena itself, not a list.
  - `train_and_evaluate(agent, arena, validation_interval, total_update_steps,
    eval_checkpoint)` takes a checkpoint as its fifth argument;
    `train_and_evaluate_single` takes a flag there instead.
- **Rig declaration:** the `set_*` hooks a rig's profile module calls, and the
  `rig.yaml` keys the console reads.
- **Legacy identifiers:** checkpoints and launch scripts carry them, so they
  stay:
  - the `so101_*` policy and processor names;
  - the `so101-metric` log line;
  - `$SO101_OUTPUT_DIR`, and the `so101_outputs` / `so101_manifests` scratch
    directories.

**Known gaps:**

- softgym imports `agent.oracle.rect_fabric.real2sim_smoothing`, which exists
  on no branch.
- learning_garment_manipulation still imports `agent_arena.api` in
  `real_robot/test/test_human_policy_folding.py`.
- PyG (`torch-scatter`/`torch-sparse`, only bimanual's VCD baseline) has no wheel
  that loads on glibc < 2.32, and pyrealsense2 (DRAPER) none for glibc < 2.29.

**Not done yet, deliberately.** Each item moves modules, so each needs a shim at
every path above:

- merging the duplicate sim loggers, `torch_utils`, registries and datasets;
- the 49 sim directories without an `__init__.py`;
- the ~12.5 MB of Raven assets duplicated between `arena/raven` and
  `arena/deformable_raven`;
- renaming files with typos or CamelCase names;
- a `src/` layout.

## 9. Where the rig pipeline came from

The rig pipeline was written in `so101_garment` and moved here so a second
robot could use it without forking it. It was **copied**, not grafted with
`git subtree` or `git filter-repo`. Grafting would have rewritten this
repository's history and pulled ~64k lines of unrelated simulation commits into
every future `git log`.

`so101_garment` still holds the per-line history. Most of the measured claims in
this repo's `CLAUDE.md` cite commits there. To read a file's history, find its
former path under `src/common/` in that repository and run `git log --follow`
on it there.

| Area | Moved in | From `so101_garment` at |
|---|---|---|
| `sync.py`, `deploy/{chunking,chunk_metrics,chunk_sweep,sweep_journal}.py`, `recording/{camera_controls,device_faults}.py` | stage 3a | `83f56db` |
| `deploy/{policy_run,policy_wire,policy_client,policy_log,policy_rig}.py` | stage 3b | `0fd77dd` |
| `recording/{depth,drift,usb_topology,fault_report,audio_cue,dataset_check,dataset_edit,dataset_read,collection_settings}.py` + `recording/sounds/` | stage 3c | `6719bec` |
| `web/{roots,util,jobs,lifecycle,projects}.py` | stage 3d | `878d8ee` |
| `recording/{dataset_view,camera_profile}.py` | stage 3e | `0080538` |
| `training/{destinations,matrix,metrics,progress,runs}.py` | stage 3f | `ec49dda` |
| `analysis/*`, `outputs.py`, `action_layout.py` | stage 3g | `3d04f70` |
| `recording/{cameras,realsense_camera,frames}.py` | stage 3h | `657706b` |
| `recording/config.py` | stage 3i | `b522983` |
| `recording/features.py` | stage 3j | `cc2b669` |
| `web/{roots_api,lifecycle_api,projects_api,training_api}.py`, `recording/monitor_wire.py` | stage 4 | `0c544e0` |
| `recording/episode_recorder.py` | stage 3m | `a532cf8` |
| `policies/*`, `tool/port_policies.py`, `tool/measure_tactile_border.py` | stage 5 | `d22de3a` |
| `rigs.py`, `cli.py`, `web/console.py` | stage 4 | new here |
