#!/usr/bin/env bash
# Every method repository's documented entry points, on tiny configs, against
# one environment built from actoris_harena/requirements/. Each step logs to
# logs/<step>.log; the last lines are one PASS/FAIL per step.
#   bash smoke_all.sh <root>    (root holds the six repos side by side, datasets/;
#                                logs/ and out/ are written there)
H=${1:?root}; S=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd); L=$H/logs; O=$H/out; mkdir -p $L $O
export PROJECTS=$H SOFTGYM_DIR=${SOFTGYM_DIR:-$HOME/Projects/softgym} HARENA_ENV=${HARENA_ENV:-harena-sim}
# bimanual and PlaNet pick a save root per HOSTNAME (on Viking, the real
# experiment tree in /mnt/scratch) unless SAVE_ROOT is set; never write there.
export SAVE_ROOT=$O/save_root
declare -A RESULT; ORDER=()
step() {  # step <name> <repo> <cwd> <cmd...>
  local name=$1 repo=$H/$2 dir=$3; shift 3
  # ONLY="a b c" runs just those steps (a rerun after a fix).
  if [ -n "$ONLY" ] && [[ " $ONLY " != *" $name "* ]]; then return; fi
  ORDER+=($name)
  echo "=== $name $(date +%T)"
  ( source $S/env.sh $repo >/dev/null 2>&1; cd $dir && timeout ${STEP_TIMEOUT:-3600} "$@" ) > $L/$name.log 2>&1
  local rc=$?; RESULT[$name]=$rc; echo "    exit $rc"
}
SMOKE="python $S/smoke_run.py"
A_JATN1='softgym|domain:rainbow-rectangular-fabrics,initial:crumpled,action:pixel-pick-and-place(1),task:flattening'
A_JATN2='softgym|domain:realadapt-towels,initial:crumpled,action:pixel-pick-and-place(1),task:flattening'
PLANET=sim_exp/lagarnet/planet_clothpick_single_picker_single_primitive_multi_longsleeve_flattening_longsleeve_all_garment
MAGPIE=sim_exp/magpie/magpie_ctr_align_all_sim_garments_p4_v151_hindsight

step imports_ja-tn JA-TN $H/JA-TN python $S/import_check.py ja_tn.adapter ja_tn.transporter actoris_harena.api
step imports_lagarnet LaGarNet $H/LaGarNet python $S/import_check.py lagarnet.controllers.gc_rssm lagarnet.controllers.planet.rssm lagarnet.utils
step imports_draper DRAPER $H/DRAPER python $S/draper_check.py $H/DRAPER/interface
step compose_planet PlaNet-ClothPick $H python $S/compose_all.py $H/PlaNet-ClothPick
step compose_magpie bimanual_garment_folding $H python $S/compose_all.py $H/bimanual_garment_folding sim_exp/magpie


PO="agent.total_update_steps=4 agent.validation_interval=2 agent.test_interval=2 agent.batch_size=2 agent.datasets.0.params.data_dir=$H/datasets agent.datasets.1.params.data_dir=$H/datasets save_root=$O/planet"
step planet_train PlaNet-ClothPick $H/PlaNet-ClothPick $SMOKE tool/hydra_train.py --config-name $PLANET $PO
step planet_eval PlaNet-ClothPick $H/PlaNet-ClothPick $SMOKE tool/hydra_eval.py --config-name $PLANET $PO

R=$H/lagarnet_run; mkdir -p $R/data; cp -r $S/lagarnet_run/configuration $R/
step lagarnet_collect LaGarNet $R/data $SMOKE $H/LaGarNet/data/collect_data.py --trials 4 --parallel_processes 1 --data_path smoke --agent_save_dir $O/lagarnet
step lagarnet_compress LaGarNet $R/data python $H/LaGarNet/data/compress_data.py --data_path smoke
step lagarnet_train_gc_rssm LaGarNet $R $SMOKE $H/LaGarNet/train_policy.py --agent gc_rssm --config smoke --log_dir $O/lagarnet/models
step lagarnet_train_rssm LaGarNet $R $SMOKE $H/LaGarNet/train_policy.py --agent rssm --config smoke --log_dir $O/lagarnet/models
step lagarnet_eval LaGarNet $R $SMOKE $H/LaGarNet/eval_policy_in_all_sim_envs.py --agent gc_rssm --config smoke --model_dir $O/lagarnet/models --save_dir $O/lagarnet/evals

MO="save_root=$O/magpie"
step magpie_heuristic_eval bimanual_garment_folding $H/bimanual_garment_folding $SMOKE tool/hydra_eval.py --config-name sim_exp/magpie/heuristic_centre_sleeve_folding $MO
step magpie_train bimanual_garment_folding $H/bimanual_garment_folding $SMOKE tool/hydra_train.py --config-name $MAGPIE $MO agent.total_update_steps=4 agent.validation_interval=2 agent.val_interval=2 agent.batch_size=8 agent.num_warmup_steps=1 agent.dataset_config.data_dir=$H/datasets

export SMOKE_SET="register:CONFIG_DIR=$S/jatn_conf"
step jatn_transporter_train JA-TN $H/JA-TN/tool $SMOKE train_and_evaluate.py --agent transporter --arena "$A_JATN1" --config smoke --log_dir $O/jatn
step jatn_transporter_eval JA-TN $H/JA-TN/tool $SMOKE evaluate.py --agent transporter --arena "$A_JATN1" --config smoke --log_dir $O/jatn --eval_checkpoint -1
step jatn_ja-tn_train JA-TN $H/JA-TN/tool $SMOKE train_and_evaluate.py --agent ja-tn --arena "$A_JATN2" --config smoke --log_dir $O/jatn
unset SMOKE_SET

echo "=== summary"
for n in "${ORDER[@]}"; do [ "${RESULT[$n]}" = 0 ] && echo "PASS $n" || echo "FAIL $n (exit ${RESULT[$n]})"; done
