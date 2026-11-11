# source env.sh <repo-dir>   -- harena-sim + softgym + the repo on PYTHONPATH,
# i.e. what each repo's setup.sh does, minus activating that repo's own env.
: "${PROJECTS:=$HOME/Projects}"
: "${SOFTGYM_DIR:=$PROJECTS/softgym}"
: "${HARENA_ENV:=harena-sim}"
# A non-interactive ssh shell may not have conda on PATH (MEASURED on thanos).
if ! command -v conda >/dev/null; then
    for _c in ~/anaconda3 ~/miniconda3 /opt/conda; do
        [ -f $_c/etc/profile.d/conda.sh ] && { . $_c/etc/profile.d/conda.sh; break; }
    done
fi
command -v conda >/dev/null && eval "$(conda shell.bash hook)"
conda activate "$HARENA_ENV"
_here=$PWD; cd "$SOFTGYM_DIR" && . ./setup.sh; cd "$_here"
export PYTHONPATH=$1:$PYTHONPATH MP_FOLD_PATH=$1 REAL_ROBOT_PATH=$1/real_robot
export WANDB_MODE=disabled PYTORCH_JIT=0 PYTHONUNBUFFERED=1
# ~/.local/lib/python3.10 is on every python3.10's path; keep it out of the lock's
# env (on thanos it held requests-oauthlib and rsa, which pip check then flagged).
export PYTHONNOUSERSITE=1
# Headless pyflex renders through EGL on the device EGL_GPU names, which the
# softgym setup.sh above sets (PyFlex/egl_device.py). These GLX variables cover
# a pyflex WINDOW, which goes through GLX instead.
export __GLX_VENDOR_LIBRARY_NAME=nvidia __NV_PRIME_RENDER_OFFLOAD=1 __VK_LAYER_NV_optimus=NVIDIA_only
export QT_QPA_PLATFORM=offscreen SDL_VIDEODRIVER=dummy
