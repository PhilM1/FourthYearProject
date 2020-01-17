#!/usr/bin/python3
import sys
import json
import argparse
import configparser
from clint.textui import colored as coloured
import googleapiclient.discovery
from google.auth import compute_engine


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
        instance_names.append(result["items"][i]["name"])
    return instance_names


# https://cloud.google.com/compute/docs/tutorials/python-guide
def deploy_workers(amount, index):
    creds = compute_engine.Credentials()
    compute = googleapiclient.discovery.build(credentials=creds, serviceName = "compute", version = "v1")
    image = compute.images().getFromFamily(project="debian-cloud", family="debian-9").execute()                 # TODO: Using Debian-9 for now, change to deeplearning image when ready
    source_disk_image = image["selfLink"]
    machine_type = "zones/%s/machineTypes/n1-standard-1" % config["DEFAULT"]["zone"]
    #startup_script = open(os.path.join(os.path.dirname(__file__), "SCRIPT_GOES_HERE"), "r").read()             # TODO: set startup_script variable here to have instance run something on boot, will likely be training script with config for specific worker be spawned
    for i in range(amount):
        worker_index = index + amount + 1

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
                #{
                    # Startup script is automatically executed by the
                    # instance upon startup.
                    #'key': 'startup-script',       # TODO: UNCOMMENT THIS LATER WHEN WE HAVE A STARTUP SCRIPT TO RUN
                    #'value': startup_script
                #}, 
                # {
                #     'key': 'url',
                #     'value': image_url
                # }, {
                #     'key': 'text',
                #     'value': image_caption
                # }, {
                #     'key': 'bucket',
                #     'value': bucket
                # }
                ]
            }
        }
        compute.instances().insert(project=config["DEFAULT"]["project_id"], zone=config["DEFAULT"]["zone"], body=worker_config).execute()


def teardown_workers(amount, index):
    creds = compute_engine.Credentials()
    compute = googleapiclient.discovery.build(credentials=creds, serviceName = "compute", version = "v1")
    for i in range(index - amount, index):
        name = "worker-" + i
        compute.instances().delete(project=config["DEFAULT"]["project_id"], zone=config["DEFAULT"]["zone"], instance=name).execute()


def main():
    if args.list:
        available_workers = list_workers()
        print(available_workers)
        sys.exit(0)
    elif args.workers:
        num_workers = len(list_workers())
        if num_workers < int(args.workers):
            deploy_workers(int(args.workers) - num_workers, num_workers)
        elif num_workers > int(args.workers):
            teardown_workers(num_workers - int(args.workers), num_workers)
        
        #send_jobs()
        print("send_jobs() doesn't exist yet")


config = parse_config()
args = parse_args()
if __name__ == "__main__":
    main()

