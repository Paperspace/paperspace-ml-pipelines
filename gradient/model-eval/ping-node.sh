echo 10.43.252.183 intel-devcloud.paperspacegradient.com >> /etc/hosts
curl -k "https://intel-devcloud.paperspacegradient.com/model-serving/desq9bue0d4t11c/v1/models/frozen_inference_graph/metadata"

export MODEL_NAME=ssd-resnet34
export DATA_DIR=/storage/data/coco300
python3 benchmark.py 
