#!/usr/bin/python3

# general imports
import sys
import os
import math
import time
import argparse
import configparser
from clint.textui import colored as coloured
from multiprocessing import Process

# json api imports
from flask import Flask, request
import json

# gcp utility imports 
import googleapiclient.discovery
from google.auth import compute_engine

# custom script imports
import tensorflow_metasurface


def parse_config():
    config = configparser.ConfigParser()
    try:
        config.read("config.yaml")
    except:
        print(coloured.red("[!!] Config file not found. Edit config_sample.yaml in this directory, and rename it to config.yaml when done."))
    return config


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", help="Utilize a specified number of workers for training. Will deploy or tear down worker instances as needed.")
    parser.add_argument("--list", action="store_true", help="List available workers in GCP project and exit.")
    return parser.parse_args()


def list_workers():
    creds = compute_engine.Credentials()
    compute = googleapiclient.discovery.build(credentials=creds, serviceName = "compute", version = "v1")
    result = compute.instances().list(project=config["DEFAULT"]["project_id"], zone=config["DEFAULT"]["zone"]).execute()
    instance_names = []
    for i in range(len(result["items"])):
        if result["items"][i]["name"].startswith("worker"):
            instance_names.append(result["items"][i]["name"])
    return instance_names


# https://cloud.google.com/compute/docs/tutorials/python-guide
def deploy_workers(amount, index):
    creds = compute_engine.Credentials()
    compute = googleapiclient.discovery.build(credentials=creds, serviceName = "compute", version = "v1")
    image = compute.images().getFromFamily(project="deeplearning-platform-release", family="tf2-latest-cpu").execute()
    source_disk_image = image["selfLink"]
    machine_type = "zones/%s/machineTypes/n1-standard-1" % config["DEFAULT"]["zone"]

    # note to future me, this is a greate guide on startup scripts and passing custom values: https://cloud.google.com/compute/docs/startupscript
    startup_script = open(os.path.join(os.path.dirname(__file__), "worker_setup.sh"), "r").read()

    for i in range(amount):
        worker_index = i + index

        # most of config taken from referenced URL
        worker_config = {
            'name': "worker-" + str(worker_index),
            'machineType': machine_type,

            # Specify the boot disk and the image to use as a source.
            'disks': [
                {
                    'boot': True,
                    'autoDelete': True,
                    'initializeParams': {
                        'sourceImage': source_disk_image,
                    }
                }
            ],

            # Specify a network interface with NAT to access the public
            # internet.
            'networkInterfaces': [{
                'network': 'global/networks/default',
                'accessConfigs': [
                    {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
                ]
            }],

            # Allow the instance to access cloud storage and logging.
            'serviceAccounts': [{
                'email': 'default',
                'scopes': [
                    'https://www.googleapis.com/auth/devstorage.read_write',
                    'https://www.googleapis.com/auth/logging.write'
                ]
            }],

            # Metadata is readable from the instance and allows you to
            # pass configuration from deployment scripts to instances.
            'metadata': {
                'items': [
                {
                    # Startup script is automatically executed by the
                    # instance upon startup.
                    'key': 'startup-script',
                    'value': startup_script
                }, {
                    'key': 'project_id',
                    'value': config["DEFAULT"]["project_id"]
                }, {
                    'key': 'zone',
                    'value': config["DEFAULT"]["zone"]
                }, {
                    'key': 'cluster_master_ip',
                    'value': config["DEFAULT"]["cluster_master_ip"]
                }, {
                    'key': 'worker_id',
                    'value': "worker-" + str(worker_index)
                }, {
                    'key': 'bucket_id',
                    'value': config["DEFAULT"]["bucket_id"]
                }
                ]
            }
        }
        compute.instances().insert(project=config["DEFAULT"]["project_id"], zone=config["DEFAULT"]["zone"], body=worker_config).execute()


def teardown_workers(amount, index):
    creds = compute_engine.Credentials()
    compute = googleapiclient.discovery.build(credentials=creds, serviceName = "compute", version = "v1")
    for i in range(index - amount, index):
        name = "worker-" + str(i)
        compute.instances().delete(project=config["DEFAULT"]["project_id"], zone=config["DEFAULT"]["zone"], instance=name).execute()


def split_new_data_dynamic():
    csv_files = tensorflow_metasurface.find_new_data()
    if len(csv_files) == 0:
        print(coloured.cyan("[*] No new models to train, exiting..."))
        #sys.exit(0)
        return []
    else:
        new_data = len(csv_files)
        queue_size = int(config["DEFAULT"]["queue_size"])
        csv_table = []
        for i in range(0, new_data, queue_size):
            # python doesn't care if we go past the end of the list, it just gives what's left
            # this will result in a varying amount of queues "queue_size" long, except for the last queue which gets the leftovers
            csv_table.append(csv_files[i:i+queue_size])
        return csv_table
        
        
def split_new_data_static(num_workers):
    csv_files = tensorflow_metasurface.find_new_data()
    if len(csv_files) == 0:
        print(coloured.cyan("[*] No new models to train, exiting..."))
        #sys.exit(0)
        return []
    else:
        new_data = len(csv_files)
        queue_size = math.ceil(new_data / num_workers)
        csv_table = []
        for i in range(0, new_data, queue_size):
            # python doesn't care if we go past the end of the list, it just gives what's left
            # this will result in a varying amount of queues "queue_size" long, except for the last queue which gets the leftovers
            csv_table.append(csv_files[i:i+queue_size])
        return csv_table


def main():
    while True:
        global batch_csv
        if args.list:
            available_workers = list_workers()
            if len(available_workers) != 0:
                print("[*] %d workers available" % len(available_workers))
                print(available_workers)
            else:
                print("[*] No workers currently deployed. Spawn some instances with the --workers [number] script argument.")
            sys.exit(0)
        elif args.workers:
            num_workers = len(list_workers())
            if num_workers < int(args.workers):
                to_spawn = int(args.workers) - num_workers
                print("[*] Deploying %d worker(s)." % to_spawn)
                deploy_workers(to_spawn, num_workers)
            elif num_workers > int(args.workers):
                to_teardown = num_workers - int(args.workers)
                print("[*] Tearing down %d worker(s)." % to_teardown)
                teardown_workers(to_teardown, num_workers)
            batch_csv = split_new_data_static(int(args.workers))
        else:
            batch_csv = split_new_data_dynamic()
            needed_workers = len(batch_csv)          # should be the number of queues in the list
            num_workers = len(list_workers())
            if num_workers < needed_workers:
                to_spawn = needed_workers - num_workers
                print("[*] Deploying %d worker(s)." % to_spawn)
                deploy_workers(to_spawn, num_workers)
            elif num_workers > needed_workers:
                to_teardown = num_workers - needed_workers
                print("[*] Tearing down %d worker(s)." % to_teardown)
                teardown_workers(to_teardown, num_workers)  
        
        # serve datasets to workers
        app.run(host="0.0.0.0")


config = parse_config()
args = parse_args()
batch_csv = []
app = Flask(__name__)


@app.route("/<worker>")
def serve_dataset(worker):
    worker_list = list_workers()
    worker_index = worker_list.index(worker)
    to_serve = []
    for data_set in batch_csv[worker_index]:
        to_serve.append(data_set.name) 
    return json.dumps(to_serve)

@app.route("/KillServer")   # this is jank and I know it
def kill_server():
    shutdown = request.environ.get('werkzeug.server.shutdown')
    shutdown()


if __name__ == "__main__":
    main()
