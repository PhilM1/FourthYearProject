#!/bin/bash

# install git and clone repo
apt install -y git
git clone https://github.com/PhilM1/FourthYearProject.git

# install pip requirements
#apt install -y python3-pip
#pip3 install --user clint

# set up config
cd FourthYearProject
PROJECT_ID=$(curl http://metadata.google.internal/computeMetadata/v1/instance/attributes/project_id -H "Metadata-Flavor: Google")
ZONE=$(curl http://metadata.google.internal/computeMetadata/v1/instance/attributes/zone -H "Metadata-Flavor: Google")
CLUSTER_MASTER_IP=$(curl http://metadata.google.internal/computeMetadata/v1/instance/attributes/cluster_master_ip -H "Metadata-Flavor: Google")
WORKER_ID=$(curl http://metadata.google.internal/computeMetadata/v1/instance/attributes/worker_id -H "Metadata-Flavor: Google")
BUCKET_ID=$(curl http://metadata.google.internal/computeMetadata/v1/instance/attributes/bucket_id -H "Metadata-Flavor: Google")
printf "[DEFAULT]\nproject_id = $PROJECT_ID\nzone = $ZONE\ncluster_master_ip = $CLUSTER_MASTER_IP\nworker_id = $WORKER_ID\nbucket_id = $BUCKET_ID\n" > config.yaml

# let er rip and pray she don't crash and burn
python3 tf_worker.py
