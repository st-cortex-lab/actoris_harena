import importlib, sys, traceback
ok = True
for m in sys.argv[1:]:
    try:
        importlib.import_module(m); print("ok  ", m)
    except Exception:
        ok = False; print("FAIL", m); traceback.print_exc(limit=-3)
sys.exit(0 if ok else 1)
