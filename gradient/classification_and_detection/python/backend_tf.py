"""
tensorflow backend (https://github.com/tensorflow/tensorflow)
"""

# pylint: disable=unused-argument,missing-docstring,useless-super-delegation

import tensorflow as tf
from tensorflow.core.framework import graph_pb2

import backend
import requests
import json
class BackendTensorflow(backend.Backend):
    def __init__(self):
        super(BackendTensorflow, self).__init__()

    def version(self):
        return tf.__version__ + "/" + tf.__git_version__

    def name(self):
        return "tensorflow"

    def image_format(self):
        # By default tensorflow uses NHWC (and the cpu implementation only does NHWC)
        return "NHWC"

    def load(self, model_path, inputs=None, outputs=None):
        # there is no input/output meta data i the graph so it need to come from config.
        if not inputs:
            raise ValueError("BackendTensorflow needs inputs")
        if not outputs:
            raise ValueError("BackendTensorflow needs outputs")
        self.outputs = outputs
        self.inputs = inputs

        self.url = "https://intel-devcloud.paperspacegradient.com/model-serving/desuevt9ekqcygd:predict"
        #self.url= "https://intel-devcloud.paperspacegradient.com/model-serving/desepohjtixshif:predict"
        
        # TODO: support checkpoint and saved_model formats?
        # graph_def = graph_pb2.GraphDef()
        # with open(model_path, "rb") as f:
        #     graph_def.ParseFromString(f.read())
        # g = tf.compat.v1.import_graph_def(graph_def, name='')
        # self.sess = tf.compat.v1.Session(graph=g)
        # return self

    def predict(self, feed):
        #r = requests.post(url=self.url, verify=False, data=json.dumps(feed))
        #print(r)
        #data = r.json()['outputs']
        #print(data)
        #return [data['num_detections'],data['detection_boxes'],data['detection_scores'],data['detection_classes']]
        #return self.sess.run(self.outputs, feed_dict=feed)
        #data_obj = feed["signature_name"]= "serving_default"
        
        #tf
        #print((feed))
        r = requests.post(url=self.url, verify=False, data=json.dumps(feed))
        #print(r.json())
        data = r.json()['outputs']
        return [data['num_detections'],data['detection_boxes'],data['detection_scores'],data['detection_classes']]

       
        # request_obj = {"signature_name": "serving_default",
        #         "inputs" :  {'image_tensor': feed['inputs']}}
        # r = requests.post(url=self.url, verify=False, data=json.dumps(request_obj))
        # print(r.json())
        # data = r.json()['outputs'][0][0]

        # num_detections = 0
        # detection_boxes = []
        # detection_scores = []
        # detection_classes = []
        # for number, proposal in enumerate(data):
        #     if proposal[2] > 0:
        #         num_detections+=1
        #         #num_detections
        #         detection_boxes += proposal[3:6]
        #         detection_scores += [proposal[2]]
        #         detection_classes += [proposal[1]]
            
        # return [[num_detections],[detection_boxes],[detection_scores],[detection_classes]]

    #detection_classes,detection_scores,detection_boxes,num_detections
    #image_id - ID of the image in the batch
    #label - predicted class ID
    #conf - confidence for the predicted class
    #(x_min, y_min) - coordinates of the top left bounding box corner (coordinates are in normalized format, in range [0, 1])
    #(x_max, y_max) - coordinates of the bottom right bounding box corner (coordinates are in normalized format, in range [0, 1])