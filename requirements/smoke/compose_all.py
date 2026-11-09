import sys
from pathlib import Path
from hydra import initialize_config_dir, compose
conf = Path(sys.argv[1]).resolve() / "conf"
bad = []
names = sorted(p.relative_to(conf).with_suffix("").as_posix() for p in (conf / (sys.argv[2] if len(sys.argv) > 2 else "sim_exp")).rglob("*.yaml"))
with initialize_config_dir(str(conf), version_base=None):
    for n in names:
        try: compose(config_name=n)
        except Exception as e: bad.append((n, str(e).splitlines()[0][:160]))
print(f"{len(names) - len(bad)}/{len(names)} sim_exp configs compose")
for n, e in bad: print("  BAD", n, "--", e)
