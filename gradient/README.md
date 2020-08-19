wget http://download.tensorflow.org/models/object_detection/faster_rcnn_resnet50_coco_2018_01_28.tar.gz
tar xvfz faster_rcnn_resnet50_coco_2018_01_28.tar.gz

python3 /opt/intel/openvino/deployment_tools/model_optimizer/mo.py --input_model faster_rcnn_resnet50_coco_2018_01_28/frozen_inference_graph.pb --transformations_config /opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/faster_rcnn_support.json --tensorflow_object_detection_api_pipeline_config faster_rcnn_resnet50_coco_2018_01_28/pipeline.config --reverse_input_channels
wget http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_2018_01_28.tar.gz

python3 /opt/intel/openvino/deployment_tools/model_optimizer/mo.py --input_model faster_rcnn_resnet50_coco_2018_01_28/frozen_inference_graph.pb --transformations_config /opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/faster_rcnn_support.json --tensorflow_object_detection_api_pipeline_config faster_rcnn_resnet50_coco_2018_01_28/pipeline.config --reverse_input_channels

mkdir -p object-detect/1
cp -r saved_model/* object-detect/1/

mkdir -p object-detect/2

cp frozen_inference_graph.* faster_rcnn_resnet50_coco_2018_01_28/object-detect/2/


machineType: metal-cpu
clusterId : cl1nurf0i
command: mv ./1 /artifacts/
container: paperspace/openvinopipeline:mo
modelPath: /artifacts
modelType: Custom
name: fastai-pipeline
projectId: pr20lgf8g
workspace: ./faster_rcnn_resnet50_coco_2018_01_28/object-detect