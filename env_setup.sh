#!/usr/bin/env bash
# Activate the SIMULATION environment (the [sim] extra).
#
# There are two environments and they are not interchangeable. This one runs
# the benchmark arenas: numpy<2, gym 0.26, robosuite, pybullet, dm_control.
#
# The RIG pipeline -- the collection / visualisation / training / deployment
# code the robot repos import -- lives in the same package but runs beside
# LeRobot under numpy>=2 on Python >=3.12, and is installed into each robot
# repo's own venv with:
#
#     pip install -e "/path/to/actoris_harena[rig]"
#
# Do not install [sim] and [rig] into one environment. MEASURED: LeRobot pins
# numpy>=2.0,<2.3 and the sim stack pins numpy<2.0, so pip cannot satisfy both.
# `import actoris_harena` is lazy precisely so that a venv with only [rig]
# installed can reach actoris_harena.recording without any of the above.

# The environment built from requirements/sim-py310.txt (README, section 3).
# Set ACTORIS_HARENA_CONDA_ENV to use another one.
conda deactivate
conda activate "${ACTORIS_HARENA_CONDA_ENV:-harena-sim}"

export PYTORCH_JIT=0
# Keep ~/.local's packages from shadowing the lock's pins.
export PYTHONNOUSERSITE=1
# pyflex renders headless through EGL, on the EGL device EGL_GPU names. Unset,
# it takes EGL's default display, which on a desktop session (Wayland
# especially) or a hybrid-GPU laptop is Mesa, and Mesa's shader compiler
# rejects pyflex's shaders, so it segfaults. The simulator's setup script picks
# the NVIDIA device of the first visible CUDA GPU (PyFlex/egl_device.py); keep
# that choice, and run the same probe here if it has not been run. This is NOT
# $CUDA_VISIBLE_DEVICES: those are physical GPU ids, not EGL device indices.
if [ -z "${EGL_GPU:-}" ] && [ -f "${PYFLEXROOT:-}/egl_device.py" ]; then
    _egl_gpu=$(python3 "$PYFLEXROOT/egl_device.py" 2>/dev/null) && export EGL_GPU=$_egl_gpu
    unset _egl_gpu
fi
# A pyflex WINDOW (disp:True) goes through GLX instead; point that at NVIDIA too.
export __GLX_VENDOR_LIBRARY_NAME=nvidia __NV_PRIME_RENDER_OFFLOAD=1

### Actoris-Harena
export ACTORIS_HARENA_PATH=${PWD}/actoris_harena
export PYTHONPATH=${ACTORIS_HARENA_PATH}/../:$PYTHONPATH

### Raven
export RAVENS_ASSETS_DIR=${ACTORIS_HARENA_PATH}/arena/raven/environments/assets

### Deformable Raven
export DEFORMABLE_RAVEN_ASSETS_DIR=${ACTORIS_HARENA_PATH}/arena/deformable_raven/src/assets