# gradient-benchmarks
 Gradient end to end pipeline benchmarks

## launch commands from repo with after pip install gradient & setting apiKey
- To pull and process coco: gradient experiments run singlenode --optionsFile process_coco.yaml
- To pull and convert model: gradient experiments run singlenode --optionsFile download_model.yaml
- Export model as endpoints, then start in paperspace: (openvino) - gradient deployments create --optionsFile deploy.yaml, (tf) gradient deployments create --optionsFile deploy_tf.yaml 
- **Run benchmark: gradient experiments run singlenode --optionsFile model-eval/exec-bench.yaml** 
