"""Every name another repository imports from this package still exists.

Seven repositories import ``actoris_harena`` and none of them pins it: each
installs this checkout editable (``pip install -e``) at whatever branch is
checked out, so a module moved or a name renamed here breaks them on their
next run, with nothing in THIS repo's suite to say so. That has happened:
``train_and_evaluate`` was renamed away while bimanual_garment_folding and
JA-TN still called it.

``SURFACE`` below is what each consumer imports, taken by parsing their source
(``from actoris_harena.x import y``, ``import actoris_harena.x``) plus the
names they reach through an alias (``ag_ar.build_agent``). It is checked with
``ast``, never by importing: half the surface is the sim stack (numpy<2,
pybullet, gym), which cannot be installed in the rig venv this suite runs in,
and an import would test the environment rather than the package.

A name is present when the module defines, assigns or imports it, re-exports
it through ``from ... import *``, or it is a submodule -- and, for the package
itself, when ``__init__._LAZY`` serves it. A failure names the consumer that
breaks. If the change is deliberate, update that consumer first and then its
row here; ``documents/compatibility.md`` says where each one lives.

NOT listed, because they are not on develop yet: so101_garment's branches
import ``analysis.features``, ``analysis.recordings`` and
``analysis.perturb.{STATE_BASELINES,patch_occlusion}``, which live on this
repo's ``dinovitac-ablations`` / ``tactile-crop-all-models`` branches. softgym
imports ``agent.oracle.rect_fabric.real2sim_smoothing``, which exists nowhere.

Run:  python -m unittest test.unit.test_consumer_surface
"""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PACKAGE = "actoris_harena"

# consumer -> module (relative to actoris_harena; "" is the package) -> names.
# An empty tuple means the module itself is imported.
SURFACE: "dict[str, dict[str, tuple[str, ...]]]" = {
    "so101_garment": {
        "action_layout": ("gripper_columns", "set_gripper_columns"),
        "analysis": ("attention", "gradients", "phases", "report", "slides"),
        "analysis.diffusion": (
            "DEFAULT_SEED",
            "SEED_FIELDS",
            "pinned",
            "plan",
            "sampler_spread",
        ),
        "analysis.inference": ("Inference",),
        "analysis.paths": ("analysis_dir", "content_name"),
        "analysis.perturb": (
            "BASELINES",
            "baseline_frame",
            "chunk_delta",
            "occlusion",
            "ranking",
        ),
        "analysis.phases": ("spans_of",),
        "analysis.report": ("PHASE_INK", "shade_phases"),
        "analysis.sources": ("DatasetSource", "RunSource", "_to_hwc_uint8"),
        "deploy.chunk_metrics": ("compare", "summarise"),
        "deploy.chunk_sweep": (
            "SPEC_HELP",
            "SweepSpecError",
            "cell_label",
            "expand_grid",
        ),
        "deploy.chunking": (
            "ChunkingError",
            "DEFAULT_BLEND_WINDOW",
            "DEFAULT_ENSEMBLE_WEIGHT",
            "DEFAULT_EXECUTE_RATIO",
            "STRATEGIES",
        ),
        "deploy.policy_client": ("LocalActionSource", "RemoteActionSource"),
        "deploy.policy_log": (
            "OUTCOMES",
            "RunLog",
            "runs_root",
            "score",
            "trial_verdicts",
        ),
        "deploy.policy_rig": ("FrameCache", "RAMP_S", "TwinRig", "parse_camera_map"),
        "deploy.policy_run": ("RunControl",),
        "deploy.policy_wire": ("WireError", "decode_request", "encode_chunk"),
        "deploy.sweep_journal": (
            "append_row",
            "done_keys",
            "journal_for",
            "load_rows",
            "row_key",
        ),
        "policies": (),
        "policies.act.modeling_act": ("HarenaActPolicy",),
        "policies.common.tactile": (
            "HarenaTactileCropProcessorStep",
            "TACTILE_CAMERAS",
            "crop_and_restore",
        ),
        "policies.dreamzero": ("metrics",),
        "policies.dreamzero.modeling_dreamzero": ("HarenaDreamzeroPolicy",),
        "policies.fastwam.modeling_fastwam": ("HarenaFastwamPolicy",),
        "policies.fastwam_predict.configuration_fastwam_predict": (
            "HarenaFastwamPredictConfig",
        ),
        "policies.fastwam_predict.modeling_fastwam_predict": (
            "HarenaFastwamPredictPolicy",
        ),
        "policies.loading": ("ensure_registered",),
        "recording": ("camera_profile", "features"),
        "recording.audio_cue": ("AudioCue",),
        "recording.camera_controls": (
            "CONTROL_NAMES",
            "EXPOSURE_AUTO",
            "apply_controls",
            "read_controls",
        ),
        "recording.camera_profile": ("CameraProfile", "set_profile"),
        "recording.cameras": ("CameraCapture",),
        "recording.collection_settings": (
            "SelectionError",
            "is_resumable_dataset",
            "read_existing_streams",
            "resolve_new_selection",
            "resolve_resume_selection",
            "selection_to_teleop_flags",
        ),
        "recording.config": ("load_recording_config", "set_recording_config_path"),
        "recording.dataset_check": (
            "DatasetDamaged",
            "dataset_integrity",
            "ensure_loadable",
            "repair_phantom_episodes",
        ),
        "recording.dataset_edit": (
            "ReadOnlyDatasetError",
            "compact_dataset",
            "read_episode_lengths",
            "read_soft_deleted",
            "saved_episode_total",
            "surviving_indices",
            "writability_problem",
            "write_soft_deleted",
        ),
        "recording.dataset_read": (
            "camera_label",
            "decode_episode_frames",
            "episode_video_path",
            "playable_window",
            "read_episode_joints",
            "read_episode_row",
            "video_keys",
        ),
        "recording.dataset_view": (
            "CAMERA_PREFIX",
            "COMPOSITE_SIZE",
            "PI05_SLOT_ORDER",
            "ViewError",
            "build_composite_video",
            "build_view",
            "camera_keys",
            "composite_grid",
            "filtered_info",
            "pi05_rename_map",
            "short_name",
            "split_selection",
            "view_slug",
        ),
        "recording.depth": ("DepthWriter",),
        "recording.device_faults": ("bus_gone",),
        "recording.episode_recorder": ("EpisodeRecorder", "RecorderState"),
        "recording.features": (
            "ACTION_EE_KEY",
            "ACTION_FRESH_S",
            "OBS_EE_KEY",
            "RobotSchema",
            "TELEOP_ACTIVE_KEY",
            "assemble_frame",
            "build_action",
            "build_dataset_features",
            "build_observation_state",
            "pose_to_vec7",
        ),
        "recording.monitor_server": (
            "DEFAULT_MAX_WIDTH",
            "DEFAULT_QUALITY",
            "DEFAULT_VIEW_FPS",
            "MonitorServer",
            "MonitorSource",
            "joint_snapshot",
        ),
        "recording.monitor_wire": (
            "BOUNDARY",
            "allowed_keys_for",
            "encode_frame_batch",
            "encode_jpeg",
            "key_refusal",
            "mjpeg_part",
        ),
        "recording.realsense_camera": ("RealSenseCapture",),
        "recording.usb_topology": (
            "UsbLocation",
            "device_location",
            "directory_location",
            "group_by_hub",
            "parse_sysfs_path",
        ),
        "sync": ("TimestampedHistory", "interp_pose", "lerp", "select_interp"),
        "training": ("metrics",),
        "training.destinations": (
            "KINDS",
            "dataset_dir",
            "destination",
            "load_destinations",
            "load_runs",
            "manifest_dir",
            "reachable",
            "remember_run",
            "rsync_argv",
            "save_runs",
            "set_destinations_path",
            "ssh_argv",
            "stage_dir",
        ),
        "training.matrix": (
            "COLUMNS",
            "MatrixError",
            "POLICIES",
            "POLICY_NAMES",
            "PORTED_FROM",
            "TWIN_OF",
            "format_rows",
            "make_row",
            "parse_rows",
            "parse_slots",
            "policy_available",
            "resolved",
            "row_cameras",
            "row_refusals",
            "unavailable_message",
        ),
        "training.progress": ("parse_log", "parse_resumes", "resolve_steps"),
        "training.runs": ("view_dir_name", "with_measurements"),
        "web.jobs": (
            "MAX_JOBS",
            "add_job_routes",
            "finish",
            "new_job",
            "prune_jobs",
            "refuse_while_busy",
        ),
        "web.lifecycle": (
            "directory_size",
            "is_working_dir",
            "read_dataset_meta",
            "valid_dataset_name",
        ),
        "web.lifecycle_api": ("add_lifecycle_routes",),
        "web.projects_api": ("add_project_routes",),
        "web.roots_api": (
            "add_root_routes",
            "initial_root",
            "root_required",
            "unmount_own",
        ),
        "web.training_api": ("add_training_routes",),
        "web.util": ("in_executor", "preinit_tqdm_lock", "revalidate_assets"),
    },
    "ur3e_raven": {
        "": (),
        "action_layout": ("gripper_columns", "set_gripper_columns"),
        "agent.agent": ("Agent",),
        "agent.bc.transporter.models.resnet": ("Name2ResNet", "ResNet43_8s"),
        "agent.bc.transporter.models.transport": ("Transport",),
        "agent.bc.transporter.transporter": ("OriginalTransporterAgent",),
        "agent.bc.transporter.utils": ("utils",),
        "agent.bc.transporter.utils.utils": ("apply_rotations_to_tensor",),
        "agent.registration": ("AGENTS",),
        "agent.trainable_agent": ("TrainableAgent",),
        "arena.arena": ("Arena",),
        "arena.registration": ("ARENAS",),
        "outputs": ("output_root",),
        "recording": ("features",),
        "recording.audio_cue": ("AudioCue", "resolve_player"),
        "recording.camera_profile": ("CameraProfile", "profile", "set_profile"),
        "recording.collection_settings": ("selection_to_teleop_flags",),
        "recording.config": (
            "load_recording_config",
            "recording_config_path",
            "set_recording_config_path",
        ),
        "recording.depth": ("DepthWriter", "write_realsense_meta"),
        "recording.episode_recorder": ("EpisodeRecorder", "RecorderState"),
        "recording.features": ("RobotSchema", "build_dataset_features"),
        "recording.frames": ("FrameStore", "TimedFrameStore"),
        "recording.monitor_server": (
            "CollectionStatus",
            "MonitorServer",
            "joint_snapshot",
        ),
        "recording.monitor_wire": (
            "BOUNDARY",
            "allowed_keys_for",
            "encode_jpeg",
            "mjpeg_part",
        ),
        "recording.realsense_camera": ("RealSenseCapture",),
        "training.destinations": ("set_destinations_path",),
        "utilities.transform.transporter_net_transformer": (
            "TransporterNetTransformer",
        ),
        "web.session": ("teleop_argv",),
    },
    "bimanual_garment_folding": {
        "": (
            "Agent",
            "Arena",
            "RLAgent",
            "Task",
            "TrainableAgent",
            "TrajectoryDataset",
            "build_agent",
            "build_arena",
            "evaluate",
            "get_arena_class",
            "register_agent",
            "register_arena",
            "retrieve_config",
            "save_video",
            "train_and_evaluate",
        ),
        "agent": ("MPC_CEM",),
        "agent.drl.sac.networks": ("Critic",),
        "agent.drl.sac.replay_buffer": ("ReplayBuffer",),
        "agent.drl.sac.vanilla_sac": ("Actor", "Critic", "VanillaSAC"),
        "agent.oracle.builder": ("OracleBuilder",),
        "agent.utilities.utils": (),
        "api": (
            "build_agent",
            "build_arena",
            "build_transform",
            "evaluate",
            "get_arena_class",
            "register_agent",
            "register_arena",
            "retrieve_config",
            "retrieve_config_from_path",
            "run",
            "train_and_evaluate",
            "train_and_evaluate_single",
            "train_plural_eval_single",
        ),
        "registration.dataset": (),
        "torch_utils": ("np_to_ts", "ts_to_np"),
        "utilities.logger.logger_interface": ("Logger",),
        "utilities.networks.utils": ("np_to_ts", "ts_to_np"),
        "utilities.perform_parallel": (
            "setup_arenas",
            "setup_arenas_with_class",
            "step_arenas",
        ),
        "utilities.perform_single": ("perform_single",),
        "utilities.save_utils": ("save_colour", "save_depth", "save_mask"),
        "utilities.torch_utils": ("np_to_ts",),
        "utilities.trajectory_dataset": ("TrajectoryDataset",),
        "utilities.visual_utils": (
            "draw_pick_and_place",
            "plot_image_trajectory",
            "plot_pick_and_place_trajectory",
            "save_numpy_as_gif",
            "save_video",
        ),
    },
    "learning_garment_manipulation": {
        "": (
            "Agent",
            "Arena",
            "RLAgent",
            "Task",
            "TrainableAgent",
            "TrajectoryDataset",
            "build_agent",
            "build_arena",
            "evaluate",
            "get_arena_class",
            "register_agent",
            "register_arena",
            "retrieve_config",
            "save_video",
        ),
        "agent": ("MPC_CEM",),
        "agent.oracle.builder": ("OracleBuilder",),
        "agent.utilities.utils": (),
        "api": (
            "build_agent",
            "build_arena",
            "build_transform",
            "evaluate",
            "get_arena_class",
            "register_arena",
            "retrieve_config",
            "run",
            "train_and_evaluate_single",
            "train_plural_eval_single",
        ),
        "registration.dataset": (),
        "torch_utils": ("np_to_ts", "ts_to_np"),
        "utilities.logger.logger_interface": ("Logger",),
        "utilities.networks.utils": ("np_to_ts", "ts_to_np"),
        "utilities.perform_parallel": (
            "setup_arenas",
            "setup_arenas_with_class",
            "step_arenas",
        ),
        "utilities.save_utils": ("save_mask",),
        "utilities.torch_utils": ("np_to_ts",),
        "utilities.trajectory_dataset": ("TrajectoryDataset",),
        "utilities.visual_utils": (
            "draw_pick_and_place",
            "plot_image_trajectory",
            "plot_pick_and_place_trajectory",
            "save_numpy_as_gif",
            "save_video",
        ),
    },
    "JA-TN": {
        "": (
            "TrainableAgent",
            "build_agent",
            "build_arena",
            "evaluate",
            "register_agent",
            "retrieve_config",
            "train_and_evaluate",
        ),
        "api": ("build_agent", "build_transform"),
        "arena.raven.tasks": ("cameras",),
        "utilities.networks.utils": (),
        "utilities.trajectory_dataset": ("TrajectoryDataset",),
    },
    "PlaNet-ClothPick": {
        "": ("Arena", "RLAgent", "Task", "register_agent", "register_arena"),
        "agent": ("MPC_CEM",),
        "agent.oracle.builder": ("OracleBuilder",),
        "agent.utilities.utils": (),
        "api": (
            "build_agent",
            "build_arena",
            "evaluate",
            "train_and_evaluate_single",
            "train_plural_eval_single",
        ),
        "registration.dataset": (),
        "torch_utils": ("np_to_ts", "ts_to_np"),
        "utilities.logger.logger_interface": ("Logger",),
        "utilities.save_utils": ("save_mask",),
        "utilities.visual_utils": (
            "draw_pick_and_place",
            "plot_pick_and_place_trajectory",
            "save_numpy_as_gif",
            "save_video",
        ),
    },
}


def _source(module: str) -> "Path | None":
    """The file defining ``module``, its directory if it is a namespace
    package (the sim tree has many), or None if it does not exist."""
    rel = Path(*module.split("."))
    for candidate in (REPO / rel / "__init__.py", REPO / f"{rel}.py"):
        if candidate.is_file():
            return candidate
    return REPO / rel if (REPO / rel).is_dir() else None


def _absolute(module: str, is_package: bool, node: ast.ImportFrom) -> str:
    if not node.level:
        return node.module or ""
    parts = module.split(".") if is_package else module.split(".")[:-1]
    parts = parts[: len(parts) - (node.level - 1)]
    return ".".join(parts + ([node.module] if node.module else []))


def _lazy_names(tree: ast.Module) -> "set[str]":
    for node in tree.body:
        target = getattr(node, "target", None) or (
            node.targets[0] if isinstance(node, ast.Assign) else None
        )
        if isinstance(target, ast.Name) and target.id == "_LAZY":
            value = node.value  # type: ignore[attr-defined]
            return {k.value for k in value.keys if isinstance(k, ast.Constant)}
    return set()


def names_in(module: str, _seen: "set[str] | None" = None) -> "set[str] | None":
    """Every name ``from module import <name>`` could find, or None if the
    module does not exist."""
    seen = _seen if _seen is not None else set()
    if module in seen:
        return set()
    seen.add(module)
    source = _source(module)
    if source is None:
        return None
    names: "set[str]" = set()
    directory = source if source.is_dir() else None
    if source.is_file():
        is_package = source.name == "__init__.py"
        directory = source.parent if is_package else None
        tree = ast.parse(source.read_text(encoding="utf-8", errors="replace"))
        if module == PACKAGE:
            names |= _lazy_names(tree)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                names.add(node.name)
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = (
                    node.targets if isinstance(node, ast.Assign) else [node.target]
                )
                for target in targets:
                    names |= {n.id for n in ast.walk(target) if isinstance(n, ast.Name)}
            elif isinstance(node, ast.Import):
                names |= {(a.asname or a.name).split(".")[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom):
                origin = _absolute(module, is_package, node)
                for alias in node.names:
                    if alias.name != "*":
                        names.add(alias.asname or alias.name)
                    elif origin.startswith(PACKAGE):
                        names |= names_in(origin, seen) or set()
    if directory is not None:
        for child in directory.iterdir():
            if child.suffix == ".py":
                names.add(child.stem)
            elif child.is_dir() and child.name != "__pycache__":
                names.add(child.name)
    return names


class TestEveryConsumerStillFindsWhatItImports(unittest.TestCase):
    def test_every_listed_module_and_name_exists(self) -> None:
        for consumer, modules in SURFACE.items():
            for short, wanted in modules.items():
                module = f"{PACKAGE}.{short}" if short else PACKAGE
                with self.subTest(consumer=consumer, module=module):
                    found = names_in(module)
                    self.assertIsNotNone(
                        found, f"{consumer} imports {module}, which is gone"
                    )
                    lost = sorted(set(wanted) - (found or set()))
                    self.assertEqual(
                        lost, [], f"{consumer} imports these from {module}"
                    )


class TestTheCheckerCanFail(unittest.TestCase):
    """A guard that cannot fail guards nothing."""

    def test_a_missing_module_is_reported(self) -> None:
        self.assertIsNone(names_in(f"{PACKAGE}.no_such_module"))

    def test_a_missing_name_is_reported(self) -> None:
        self.assertNotIn("no_such_name", names_in(f"{PACKAGE}.action_layout") or set())

    def test_a_lazy_name_is_found_without_importing_the_sim_stack(self) -> None:
        self.assertIn("train_and_evaluate", names_in(PACKAGE) or set())

    def test_a_star_import_is_followed(self) -> None:
        # registration.dataset re-exports by `from ... import *` chains in the
        # sim tree; PlaNet-ClothPick star-imports it.
        self.assertTrue(names_in(f"{PACKAGE}.registration.dataset"))


if __name__ == "__main__":
    unittest.main()
