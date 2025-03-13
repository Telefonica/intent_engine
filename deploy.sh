#!/bin/bash

# © 2024 Telefónica Innovación Digital

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# namespace creation
kubectl delete namespace nemo-net
kubectl create namespace nemo-net

# l2sm test grpc server
docker build intent_engine/executioners/grpc_libs -t localhost:$1/nemometaos/mncc-ibs-grpc-l2sm:v0.0.2
docker push localhost:$1/nemometaos/mncc-ibs-grpc-l2sm:v0.0.2
kubectl apply -f intent_engine/l2sm_grpc_test.yaml 

# sleep 20
# intent engine deployment
docker build intent_engine/ -t localhost:$1/nemometaos/mncc-ibs:v0.0.2
docker push localhost:$1/nemometaos/mncc-ibs:v0.0.2
kubectl apply -f intent_engine/manifest.yaml 