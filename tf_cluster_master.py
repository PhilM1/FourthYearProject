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
    parser.add_argument("project_id")
    parser.add_argument("zone")


config = parse_config()
creds = compute_engine.Credentials()
compute = googleapiclient.discovery.build(credentials=creds, serviceName = "compute", version = "v1")
result = compute.instances().list(project=config["DEFAULT"]["project_id"], zone=config["DEFAULT"]["zone"]).execute()
print(result)
