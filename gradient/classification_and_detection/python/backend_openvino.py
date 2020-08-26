"""
tensorflow backend (https://github.com/tensorflow/tensorflow)
"""

# pylint: disable=unused-argument,missing-docstring,useless-super-delegation

import tensorflow as tf
from tensorflow.core.framework import graph_pb2

import backend
import requests
import json
class BackendOpenvino(backend.Backend):
    def __init__(self):
        super(BackendOpenvino, self).__init__()

    def version(self):
        return tf.__version__ + "/" + tf.__git_version__

    def name(self):
        return "openvino"

    def image_format(self):
        # By default tensorflow uses NHWC (and the cpu implementation only does NHWC)
        return "NCHW"

    def load(self, model_path, inputs=None, outputs=None):
        # there is no input/output meta data i the graph so it need to come from config.
        if not inputs:
            raise ValueError("BackendOpenvino needs inputs")
        if not outputs:
            raise ValueError("BackendOpenvino needs outputs")
        self.outputs = outputs
        self.inputs = inputs

        #self.url = "https://intel-devcloud.paperspacegradient.com/model-serving/desuevt9ekqcygd:predict"
        self.url= "https://intel-devcloud.paperspacegradient.com/model-serving/desepohjtixshif:predict"

    def predict(self, feed):
        request_obj = {"signature_name": "serving_default",
                "inputs" :  {'image_tensor': feed['inputs']}}
        r = requests.post(url=self.url, verify=False, data=json.dumps(request_obj))
        #print(r.json())
        data = r.json()['outputs'][0][0]

        num_detections = 0
        detection_boxes = []
        detection_scores = []
        detection_classes = []
        for number, proposal in enumerate(data):
            if proposal[2] > 0:
                num_detections+=1
                #num_detections
                detection_boxes += [proposal[3:7]]
                detection_scores += [proposal[2]]
                detection_classes += [proposal[1]]
            
        return [[num_detections],[detection_boxes],[detection_scores],[detection_classes]]

    #detection_classes,detection_scores,detection_boxes,num_detections
    #image_id - ID of the image in the batch
    #label - predicted class ID
    #conf - confidence for the predicted class
    #(x_min, y_min) - coordinates of the top left bounding box corner (coordinates are in normalized format, in range [0, 1])
    #(x_max, y_max) - coordinates of the bottom right bounding box corner (coordinates are in normalized format, in range [0, 1])