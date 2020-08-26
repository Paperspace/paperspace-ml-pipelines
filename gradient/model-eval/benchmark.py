import requests

URL = "https://intel-devcloud.paperspacegradient.com/model-serving/desq9bue0d4t11c/v1/models/frozen_inference_graph/metadata"
r = requests.get(url=URL, verify=False)
print(r.json()) 
