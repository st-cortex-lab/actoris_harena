#!/usr/bin/env bash
#SBATCH --job-name=harena-smoke
#SBATCH --account=cs-garm-2025
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=48G
#SBATCH --time=0-06:00:00
#SBATCH --output=%x-%j.log
module purge; module load Miniconda3/23.5.2-0
source /opt/apps/eb/software/Miniconda3/23.5.2-0/etc/profile.d/conda.sh
echo "Job $SLURM_JOB_ID on $(hostname)"; nvidia-smi -L
H=$HOME/project/harena-smoke
SOFTGYM_DIR=$HOME/project/softgym ONLY="${ONLY:-}" STEP_TIMEOUT="${STEP_TIMEOUT:-3600}" bash $H/actoris_harena/requirements/smoke/smoke_all.sh $H
