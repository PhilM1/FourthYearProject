#!/usr/bin/python3
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow import saved_model, get_logger
import numpy as np
import pandas
import sys
import configparser
import os
from clint.textui import progress
from clint.textui import colored as coloured


def parse_config():
    config = configparser.ConfigParser()
    try:
        config.read("config.yaml")
    except:
        print(coloured.red("[!!] Config file not found. Edit config_sample.yaml in this directory, and rename it to config.yaml when done."))
    return config


def find_new_data(abs_data_path, rel_model_path):
    model_list = os.listdir(rel_model_path)
    data_list = []
    for root, dirs, files in os.walk(abs_data_path):
        for data_file in files:
            if data_file.endswith(".csv") and data_file.split(".")[0] not in model_list:
                print(coloured.green("[*] Found new data set: %s" % data_file))
                data_list.append(os.path.join(root, data_file))
    if len(data_list) == 0:
        print(coloured.yellow("[*] No new data was found"))
    return data_list


def tensorflow_train(np_inputs, np_outputs, model_path):
    # define model and metrics we are interested in, tanh or elu activations seem to give best results so far
    # going with rmsprop for now, subject to change
    # tracking mse and accuracy for comparisons to Matlab
    get_logger().setLevel('ERROR')

    if len(np_inputs.shape) > 1:
        input_dimensions = np_inputs.shape[1]
    else:
        input_dimensions = 1
    if len(np_outputs.shape) > 1:
        output_dimensions = np_outputs.shape[1]
    else:
        output_dimensions = 1
        
    model = Sequential()
    model.add(Dense(10, activation="elu", input_dim=input_dimensions))
    model.add(Dense(output_dimensions, activation="elu"))
    model.compile(optimizer="rmsprop", loss="mse", metrics=["accuracy"])
    
    # visualizes the built NN, commented out because it's annoying
    #model.summary()
    
    # Train the model over 100 epochs, iterating on the data in batches of 256 samples
    model.fit(np_inputs, np_outputs, epochs=100, batch_size=256, verbose=0)

    return model


def main():
    config = parse_config()
    abs_path = config["DEFAULT"]["data_path"]
    trained_models = config["DEFAULT"]["model_path"]
    csv_files = find_new_data(abs_path, trained_models)
    
    if len(csv_files) == 0:
        print(coloured.cyan("[*] No new models to train, exiting..."))
        sys.exit(0)

    # loop over every csv file in data directory and train a NN with it
    print(coloured.cyan("[*] Training neural networks for new data sets..."))
    print(coloured.cyan("[*] Throwing some extra junk in the terminal because of an open Tensorflow bug: https://github.com/tensorflow/tensorflow/issues/31870"))
    for data_set in progress.bar(csv_files, expected_size=len(csv_files)):
        data = pandas.read_csv(data_set)
        inputs = data.iloc[:,0].to_numpy()
        outputs = data.iloc[:, 1:].to_numpy()
        
        new_model = tensorflow_train(inputs, outputs, trained_models)

        filename = os.path.basename(data_set).split(".")[0]             # name trained models the same as the csv file, but without the extension
        try:
            saved_model.save(new_model, os.path.join(trained_models, filename))
        except:
            print(coloured.red("[!!] Problem writing trained model to disk. Does the path specified in the config exist and have write permissions for this user?"))
            pass
        

if __name__ == "__main__":
    main()
