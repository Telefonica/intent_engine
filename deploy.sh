kubectl delete namespace ie
kubectl create namespace ie
docker build intent_engine/ -t intent-engine:latest
docker tag intent-engine:latest localhost:32000/intent-engine
docker push localhost:32000/intent-engine
kubectl apply -f intent_engine/deploy.yaml 