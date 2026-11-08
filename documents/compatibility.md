# Compatibility: who imports actoris_harena, and what they rely on

Seven repositories import this package. **None of them pins it.** Each installs
a sibling `../actoris_harena` checkout in editable mode, so whatever branch is
checked out here is what they run. A module moved or a name renamed here breaks
them on their next run.

`test/unit/test_consumer_surface.py` holds the list of every `(module, name)`
each consumer imports and fails, naming the consumer, if any stops resolving.
The list was made by parsing each consumer's source, plus the names it reaches
through an alias (`ag_ar.build_agent`). **To change the surface on purpose,
update the consumer first, then its row in that test.**

## The consumers

| Repository | Side | How it installs this package | What it imports |
|---|---|---|---|
| `so101_garment` | rig | `hpc/provision_create.sh`: `pip install -e "../actoris_harena[rig]"` (its `install.sh` does not install it) | `recording.*`, `training.*`, `analysis.*`, `deploy.*`, `policies.*` (and the `harena_*` registry names), `web.{jobs,lifecycle,lifecycle_api,projects_api,roots_api,training_api,util}`, `sync`, `action_layout` |
| `ur3e_raven` | rig + sim | `install.sh`/`install.ps1` via `install.env`: `HARENA_URL=https://github.com/halid1020/actoris_harena.git` (redirects to st-cortex-lab), `HARENA_BRANCH=develop`, `[rig]` | `recording.*`, `training.destinations`, `web.session`, `outputs`, `action_layout`; the vendored Ravens/Transporter in `agent.bc.transporter.*`, `agent.{agent,trainable_agent,registration}`, `arena.{arena,registration}`, `utilities.transform`; and `import actoris_harena` for its side effect of setting `RAVENS_ASSETS_DIR` |
| `bimanual_garment_folding` | sim | README: `pip install -e ".[torch]"` in a sibling checkout on `develop` | the top-level lazy names, `api.*` (incl. `train_and_evaluate`), `utilities.{trajectory_dataset,perform_single,perform_parallel,visual_utils,save_utils,logger.logger_interface,torch_utils,networks.utils}`, `torch_utils`, `agent.{MPC_CEM,utilities.utils,oracle.builder,drl.sac.*}`, `registration.dataset`; it also reads the env var `actoris_harena_PATH` |
| `learning_garment_manipulation` | sim | `docker/Dockerfile` clones `develop` and runs `uv pip install -e ".[torch]"`; its CI deliberately does not install it | a subset of bimanual's |
| `JA-TN` (private) | sim | README: `develop` from st-cortex-lab; `setup.sh` assumes `env_setup.sh` was sourced | `TrainableAgent`, `register_agent`, `retrieve_config(config_dir=…)`, `build_arena`, `build_agent`, `evaluate`, `train_and_evaluate`, `api.build_transform`, `utilities.trajectory_dataset`, `utilities.networks.utils`, `arena.raven.tasks(.cameras)` |
| `PlaNet-ClothPick` (private) | sim | README: `pip install -e ".[torch]"` on `develop` | `Arena`, `Task`, `RLAgent`, `api.{build_agent,build_arena,evaluate,train_and_evaluate_single,train_plural_eval_single}`, `torch_utils`, `registration.dataset`, `agent.{oracle.builder,MPC_CEM,utilities.utils}`, `utilities.{save_utils,visual_utils,logger.logger_interface}` |
| `softgym` | sim | none (lazy import) | `agent.oracle.rect_fabric.real2sim_smoothing` |

`LaGarNet` and `DRAPER` still use the old `agent_arena` package from
`agent-arena-v0`, and do not import this one.

## Promises beyond import paths

These cannot be checked by an import scan, so they are written down here:

- **Install names.** The `[rig]`, `[sim]`, `[torch]` and `[realsense]` extras;
  the `actoris-harena` console script; installing from a sibling
  `../actoris_harena` on `develop`.
- **Environment.** `import actoris_harena` sets `ACTORIS_HARENA_PATH`,
  `RAVENS_ASSETS_DIR` and `DEFORMABLE_RAVEN_ASSETS_DIR`. It also sets the
  lowercase alias `actoris_harena_PATH`, because consumers' code reads that
  spelling. The package itself reads only the uppercase one.
- **Configs.** `retrieve_config(agent, arena, name)` resolves
  `configuration/train_and_evaluate/<agent>/<arena>/<name>.yaml`, where
  `<arena>` is a spec string such as `softgym|domain:…`. That is why about 240
  config files have `|`, `:` and `()` in their names, and why they cannot be
  renamed.
- **Behaviour.** `build_agent` with `config.oracle=True` goes to
  `OracleBuilder`. `train_and_evaluate(agent, arena, validation_interval,
  total_update_steps, eval_checkpoint)` keeps its pre-rename meaning: its fifth
  argument is a checkpoint, unlike `train_and_evaluate_single`'s.
- **Rig declaration.** The `set_*` hooks a rig's `rig_profile.py` calls
  (`set_gripper_columns`, `set_profile`, `set_recording_config_path`,
  `set_destinations_path`). The `rig.yaml` keys the console reads.

## Known gaps, recorded rather than invented

- **so101_garment is ahead of `develop`.** Its current branches import
  `analysis.features`, `analysis.recordings` and
  `analysis.perturb.{STATE_BASELINES,patch_occlusion}`. They also expect a
  `tiled=` argument on `HarenaTactileCropProcessorStep` and the `harena_dinovitac`
  / `*_crop` world-model policies. All of these live on this repo's
  `dinovitac-ablations` / `tactile-crop-all-models` branches. Until those merge,
  so101's unit tier has about 22 failures against `develop`.
- **softgym** imports `agent.oracle.rect_fabric.real2sim_smoothing`, which does
  not exist on any branch.
- **bimanual_garment_folding** and **learning_garment_manipulation** still import
  `agent_arena.api` in `real_robot/test/test_human_policy_folding.py`.

## Organisation follow-ups, deliberately not done yet

Each of these moves modules, so each needs a shim at every old path listed
above:

- Merging the duplicate sim homes: loggers (5 places), `torch_utils` (2),
  registries (4) and datasets (3).
- Adding `__init__.py` to the 49 sim directories that rely on namespace
  packages.
- Deduplicating the ~12.5 MB of Raven assets shared by `arena/raven` and
  `arena/deformable_raven`.
- Renaming files with typos or CamelCase names (`hd5f`, `dreamerV2`,
  `intermidate`, …).
- A `src/` layout.
