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
# Use an official Python runtime as the base image
FROM python:3.10-alpine

# Set the working directory in the container
WORKDIR /grpc_libs

# Copy the current directory contents into the container at /intent_engine
COPY . /grpc_libs

# Install any needed dependencies specified in requirements.in
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /grpc_libs/grpc_requirements.in

# Make port 80 available to the world outside this container
EXPOSE 50051

# Run app.py when the container launches
# ENTRYPOINT [ "ls","-la","-R" ]
# WORKDIR /grpc_libs
CMD ["python3","test_server_l2sm.py"]
