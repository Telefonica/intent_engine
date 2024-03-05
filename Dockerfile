# Use an official Python runtime as the base image
FROM python:3.10-alpine

# Set the working directory in the container
WORKDIR /intent_engine

# Copy the current directory contents into the container at /intent_engine
COPY . /intent_engine
COPY executioner_catalogue.in executioner_catalogue.in

# Install any needed dependencies specified in requirements.in
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.in

# Make port 80 available to the world outside this container
EXPOSE 8080
EXPOSE 3000

# Define environment variable
ENV NAME World

WORKDIR /
# Run app.py when the container launches
CMD ["python", "-m" ,"intent_engine"]
