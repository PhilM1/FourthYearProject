#!/usr/bin/python3

# Workaround for google messing with pip packages after my project was mostly done...
import sys
sys.path.insert(0, "/opt/conda/lib/python3.7")
sys.path.insert(1, "/opt/conda/lib/python3.7/site-packages")

import requests
import json
import time
import configparser
#from clint.textui import colored as coloured
import tensorflow_metasurface
from google.cloud import storage
from google.auth import compute_engine


def parse_config():
    config = configparser.ConfigParser()
    try:
        config.read("config.yaml")
    except:
        #print(coloured.red("[!!] Config file not found. Edit config_sample.yaml in this directory, and rename it to config.yaml when done."))
        print("[!!] Config file not found. Edit config_sample.yaml in this directory, and rename it to config.yaml when done.")
    return config


def main():
    count = 0
    malformed = False
    training_jobs_old = set()
    while True:
        if config["DEFAULT"]["worker_id"] == "worker-0" and count == 6:
            requests.get("http://%s:5000/KillServer" % config["DEFAULT"]["cluster_master_ip"])      # workaround to trigger reset and get new jobs
            time.sleep(60)
        training_jobs = requests.get("http://%s:5000/%s" % (config["DEFAULT"]["cluster_master_ip"], config["DEFAULT"]["worker_id"]))
        try:
            training_jobs = set(json.loads(training_jobs.text))
            malformed = False
        except:
            print("[!!] Malformed data in training job request.")
            malformed = True
            continue

        training_jobs = training_jobs.difference(training_jobs_old)

        # if no data has been assigned to the worker, we want to keep track of how often this is happening to know if worker is needed
        if len(training_jobs) == 0 and not malformed:
            count += 1
            if count == 6 and config["DEFAULT"]["worker_id"] != "worker-0":      # just over a half hour of doing nothing, want at least one worker alive
                creds = compute_engine.Credentials()
                name = config["DEFAULT"]["worker_id"]
                compute.instances().delete(project=config["DEFAULT"]["project_id"], zone=config["DEFAULT"]["zone"], instance=name).execute()    # omae wa mou shindeiru
        elif not malformed:
            count = 0

            # training_jobs is a list of file paths in the bucket right now
            # we need to convert the paths to handles to file blobs to the storage api is happy
            training_blobs = []
            client = storage.Client()
            bucket = client.get_bucket(config["DEFAULT"]["bucket_id"])
            for file_path in training_jobs:
                training_blobs.append(bucket.get_blob(file_path))
            
            tensorflow_metasurface.train_new_data(training_blobs)
        training_jobs_old.update(training_jobs)
        #time.sleep(240)
    

config = parse_config()


if __name__ == "__main__":
    main()