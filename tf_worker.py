#!/usr/bin/python3
import requests
import json
import configparser
from clint.textui import colored as coloured
import tensorflow_metasurface
from google.cloud import storage


def parse_config():
    config = configparser.ConfigParser()
    try:
        config.read("config.yaml")
    except:
        print(coloured.red("[!!] Config file not found. Edit config_sample.yaml in this directory, and rename it to config.yaml when done."))
    return config


def main():
    training_jobs = requests.get("http://%s:5000/%s" % (config["DEFAULT"]["cluster_master_ip"], config["DEFAULT"]["worker_id"]))
    try:
        training_jobs = json.loads(training_jobs.text)
    except:
        print("[!!] Malformed data in training job request.")

    # training_jobs is a list of file paths in the bucket right now
    # we need to convert the paths to handles to file blobs to the storage api is happy
    training_blobs = []
    client = storage.Client()
    bucket = client.get_bucket(config["DEFAULT"]["bucket_id"])
    for file_path in training_jobs:
        training_blobs.append(bucket.get_blob(file_path))
    
    tensorflow_metasurface.train_new_data(training_blobs)
    

config = parse_config()


if __name__ == "__main__":
    main()