#!/bin/bash
echo 10.43.252.183 intel-devcloud.paperspacegradient.com >> /etc/hosts

export MODEL_DIR=/storage/models/ssd/saved_model
export DATA_DIR=/storage/data/coco300


source ./run_common.sh


common_opt="--config ../mlperf.conf"
dataset="--dataset-path $DATA_DIR"
OUTPUT_DIR=`pwd`/output/$name
if [ ! -d $OUTPUT_DIR ]; then
    mkdir -p $OUTPUT_DIR
fi

python3 python/main.py --profile $profile $common_opt --model $model_path $dataset \
    --output $OUTPUT_DIR $EXTRA_OPS $@
