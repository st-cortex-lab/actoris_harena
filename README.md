# Actoris Harena

**Authors:** Halid Abdulrahim Kadi (Lead), Dr Kasim Terzić (PhD Supervisor), and Dr John Oyekan (Postdoc Advisor)

*University of St Andrews, UK* and *University of York, UK*

> **Note:** This project was formerly called **Agent Arena**. It was renamed **Actoris Harena** (Latin for "The Actor's Arena") to avoid a naming conflict.

[![DOI](https://zenodo.org/badge/933415395.svg)](https://doi.org/10.5281/zenodo.14876793)
[![ArXiv](https://img.shields.io/badge/ArXiv-2504.06468-b31b1b.svg)](https://arxiv.org/abs/2504.06468)

![Actoris Harena Plot](assets/agent-arena.jpg)

The shared robot-learning framework of the St CORTEX Lab. Robot repositories
use it to collect, curate, train and deploy. Research repositories use it to
run control algorithms on simulated benchmarks.

**⚠️ For ROS integration, use the ROS branches (`ros1-noetic`, `ros2-humble`).**

---

1. [What this is](#1-what-this-is)
2. [Install it for a robot repository](#2-install-it-for-a-robot-repository)
3. [Install it for the simulated arenas](#3-install-it-for-the-simulated-arenas)
4. [The console](#4-the-console)
5. [Using the simulated arenas](#5-using-the-simulated-arenas)
6. [Tests and lint](#6-tests-and-lint)
7. [Where things are](#7-where-things-are)
8. [Compatibility with the repositories that use it](#8-compatibility-with-the-repositories-that-use-it)

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

A rig **declares** its facts once, at import: camera profile, recording
config, training destinations, gripper columns. The package refuses, rather
than guessing, until it has been told (see `src/common/rig_profile.py` in
either robot repo).

## 3. Install it for the simulated arenas

Use Linux with a GPU. Running on a CPU is strictly not recommended. It has been
validated on Ubuntu 20.04, 22.04 and 24.04.

```bash
conda create --name actoris-harena python=3.10
conda activate actoris-harena
pip install -e ".[sim,torch]"
source env_setup.sh        # activates the env and exports the asset paths
python -c "import actoris_harena, os; print(os.environ['RAVENS_ASSETS_DIR'])"
```

`[torch]` alone is what the sim consumers' READMEs and Docker images install.
Keep using it there.

**SoftGym** (skip it if you don't need it): use the lab's modified version.

1. Clone [halid1020/softgym, branch py3.10](https://github.com/halid1020/softgym/tree/py3.10).
2. Follow its [setup tutorial](https://github.com/halid1020/softgym/blob/py3.10/README.md). Its Docker container only *compiles* the simulator; run experiments outside it.
3. Download the initial-state data files it names.

**Other benchmarks:** install them as they instruct, and wrap each one in an
adapter class that implements the `Arena` interface.

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
documents/                                                  provenance, compatibility, sim notes
```

`CLAUDE.md` is the detailed, file-by-file guide.

## 8. Compatibility with the repositories that use it

Seven repositories import this package, and none of them pins a version.
`documents/compatibility.md` lists each one, how it installs the package and
what it imports. `test/unit/test_consumer_surface.py` fails, naming the
consumer, if any of those imports stops resolving. Moving or renaming a module
therefore starts in the consumer.
