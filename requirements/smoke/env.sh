# source env.sh <repo-dir>   -- harena-sim + softgym + the repo on PYTHONPATH,
# i.e. what each repo's setup.sh does, minus activating that repo's own env.
: "${PROJECTS:=$HOME/Projects}"
: "${SOFTGYM_DIR:=$PROJECTS/softgym}"
: "${HARENA_ENV:=harena-sim}"
command -v conda >/dev/null && eval "$(conda shell.bash hook)"
conda activate "$HARENA_ENV"
_here=$PWD; cd "$SOFTGYM_DIR" && . ./setup.sh; cd "$_here"
export PYTHONPATH=$1:$PYTHONPATH MP_FOLD_PATH=$1 REAL_ROBOT_PATH=$1/real_robot
export WANDB_MODE=disabled PYTORCH_JIT=0 PYTHONUNBUFFERED=1
# pyflex renders through GLX: on a hybrid-GPU laptop or a cluster node it must be
# pointed at the NVIDIA driver, or it falls back to Mesa and segfaults at init.
export __GLX_VENDOR_LIBRARY_NAME=nvidia __NV_PRIME_RENDER_OFFLOAD=1 __VK_LAYER_NV_optimus=NVIDIA_only
export QT_QPA_PLATFORM=offscreen SDL_VIDEODRIVER=dummy
