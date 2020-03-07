#!/usr/bin/python3

# general imports
import numpy as np
import pandas
import sys
import configparser
import os
import glob
import shutil
from io import StringIO
#from clint.textui import progress
#from clint.textui import colored as coloured

# tensorflow imports
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow import saved_model, get_logger

# gcp utility imports
from google.cloud import storage


def parse_config():
    config = configparser.ConfigParser()
    try:
        config.read("config.yaml")
    except:
        #print(coloured.red("[!!] Config file not found. Edit config_sample.yaml in this directory, and rename it to config.yaml when done."))
        print("[!!] Config file not found. Edit config_sample.yaml in this directory, and rename it to config.yaml when done.")
    return config


def find_new_data():
    client = storage.Client()
    bucket = client.get_bucket(config["DEFAULT"]["bucket_id"])
    blob_list = bucket.list_blobs()
    model_list = []
    data_list = []
    for blob in blob_list:
        if blob.name.split("/")[0] == "models":
            model_list.append(blob.name.split("/")[1])
    blob_list = bucket.list_blobs()                 # spooky bug where the blob_list is "aware" it's being looped over, 
    for blob in blob_list:                          # needs to be reset with another call to list_blobs()
        if blob.name.split(".")[-1] == "csv" and blob.name.split("/")[-1].split(".")[-2] not in model_list:
            #print(coloured.green("[*] Found new data set: %s" % blob.name.split("/")[-1]))
            print("[*] Found new data set: %s" % blob.name.split("/")[-1])
            data_list.append(blob)
    if len(data_list) == 0:
        #print(coloured.yellow("[*] No new data was found"))
        print("[*] No new data was found")
    return data_list


def tensorflow_train(np_inputs, np_outputs):
    # define model and metrics we are interested in, tanh or elu activations seem to give best results so far
    # going with rmsprop for now, subject to change
    # tracking mse and accuracy for comparisons to Matlab
    #get_logger().setLevel('ERROR')

    if len(np_inputs.shape) > 1:
        input_dimensions = np_inputs.shape[1]
    else:
        input_dimensions = 1
    if len(np_outputs.shape) > 1:
        output_dimensions = np_outputs.shape[1]
    else:
        output_dimensions = 1
        
    # define the model of the neural network
    model = Sequential()
    model.add(Dense(10, activation="relu", input_dim=input_dimensions))
    model.add(Dense(8, activation="relu", input_dim=input_dimensions))
    model.add(Dense(6, activation="relu", input_dim=input_dimensions))
    model.add(Dense(4, activation="relu"))
    model.add(Dense(output_dimensions, activation="elu"))
    model.compile(optimizer="Adam", loss="mse", metrics=["acc"])
    
    # Train the model over 100 epochs, iterating on the data in batches of 256 samples
    model.fit(np_inputs, np_outputs, epochs=10, batch_size=256)

    return model


def train_new_data(csv_files):
    # loop over every csv file in data directory and train a NN with it
    #for data_set in progress.bar(csv_files, expected_size=len(csv_files)):
    for data_set in csv_files:
        download_data = data_set.download_as_string()
        data = pandas.read_csv(StringIO(download_data.decode()))
        
        inputs = pandas.DataFrame()
        outputs = pandas.DataFrame()
        for i in range(len(data.columns)):
            if data.columns[i].startswith("im") or data.columns[i].startswith("re") or data.columns[i].startswith("mag") or data.columns[i].startswith("ang"):        # s-parameters are outputs
                outputs[data.columns[i]] = data[data.columns[i]]
            else:
                inputs[data.columns[i]] = data[data.columns[i]]         # anything else that is appearing in the csv must be an input
        inputs = inputs.to_numpy()
        outputs = outputs.to_numpy()
        #print(coloured.cyan("[*] Now training model for: %s" % (data_set.name)))
        print("[*] Now training model for: %s" % (data_set.name))
        new_model = tensorflow_train(inputs, outputs)
        filename = data_set.name.split("/")[-1].split(".")[-2]             # name trained models the same as the csv file, but without the extension
        try:
            saved_model.save(new_model, "/tmp/" + filename)
            # you could probably pop a shell here with a malicious filename, but what's life without some excitement?
            os.system("gsutil cp -R '/tmp/" + filename + "' gs://" + config["DEFAULT"]["bucket_id"] + "/models")
            shutil.rmtree("/tmp/" + filename)
        except:
            #print(coloured.red("[!!] Problem writing trained model to disk. Does the path specified in the config exist and have write permissions for this user?"))
            print("[!!] Problem writing trained model to disk. Does the path specified in the config exist and have write permissions for this user?")
            pass


def main():
    csv_files = find_new_data()
    if len(csv_files) == 0:
        #print(coloured.cyan("[*] No new models to train, exiting..."))
        print("[*] No new models to train, exiting...")
        return
    train_new_data(csv_files)
        

config = parse_config()


if __name__ == "__main__":
    main()
