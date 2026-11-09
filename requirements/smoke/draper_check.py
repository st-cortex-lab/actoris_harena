"""Import DRAPER's interface modules with ROS 2 stubbed: proves everything they
take from actoris_harena (and the pip-installable rest) resolves."""
import sys, types, importlib
ROS = ("rclpy", "rcc_msgs", "std_msgs", "cv_bridge", "sensor_msgs", "geometry_msgs",
       "ament_index_python", "moveit", "moveit_msgs", "launch", "launch_ros", "ur_msgs",
       "shape_msgs", "tf2_ros", "builtin_interfaces")


class _Any(types.ModuleType):
    __path__ = []
    def __getattr__(self, attr):
        if attr.startswith("__"):
            raise AttributeError(attr)
        return type(attr, (), {"__init__": lambda *a, **k: None})


class RosStubs:
    """Any ROS 2 (apt-only) package imports as an empty stub."""
    def find_module(self, name, path=None):
        return self if name.split(".")[0] in ROS else None
    def find_spec(self, name, path=None, target=None):
        import importlib.util
        return importlib.util.spec_from_loader(name, self) if name.split(".")[0] in ROS else None
    def create_module(self, spec):
        return _Any(spec.name)
    def exec_module(self, module):
        pass


sys.meta_path.insert(0, RosStubs())
# setup.sh puts the workspace (the repo's parent) on PYTHONPATH and the code is
# imported as <repo>.interface.<module>; older checkouts import it flat.
import os
iface = os.path.abspath(sys.argv[1]); repo = os.path.dirname(iface)
packaged = os.path.exists(os.path.join(repo, "__init__.py")) and not os.environ.get("DRAPER_FLAT")
sys.path.insert(0, os.path.dirname(repo) if packaged else iface)
prefix = os.path.basename(repo) + ".interface." if packaged else ""
for m in ["utils", "control_interface", "human_interface", "agent_arena_interface"]:
    importlib.import_module(prefix + m); print("ok  ", prefix + m)
