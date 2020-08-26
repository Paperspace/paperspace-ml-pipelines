wget http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz
mkdir -p /storage/models/ssd
sudo tar xvfz ssd_mobilenet_v2_coco_2018_03_29.tar.gz
#cp -r ssd_mobilenet_v1_coco_2018_01_28/saved_model/ /storage/models/ssd/
touch ssd_mobilenet_v2_coco_2018_03_29/saved_model/variables/empty.txt

python3 /opt/intel/openvino/deployment_tools/model_optimizer/mo.py --input_model ssd_mobilenet_v2_coco_2018_03_29/frozen_inference_graph.pb --transformations_config /opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/ssd_v2_support.json --tensorflow_object_detection_api_pipeline_config ssd_mobilenet_v2_coco_2018_03_29/pipeline.config --input_shape [1,300,300,3] --disable_nhwc_to_nchw --reverse_input_channels --output_dir /artifacts
cp -r ssd_mobilenet_v2_coco_2018_03_29/saved_model/ /artifacts/1/

#--tensorflow_object_detection_api_pipeline_config ssd_mobilenet_v1_coco_2018_01_28/pipeline.config
