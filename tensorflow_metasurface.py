#!/usr/bin/python3
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
import numpy as np
import csv
import configparser
import os

def parse_config():
    config = configparser.ConfigParser()
    try:
        config.read("config.yaml")
    except:
        print("[!!] Config file not found. Edit config_sample.yaml in this directory, and rename it to config.yaml when done.")
    return config
    
def find_csv_paths(root_path):
    data_csv = []
    #path = os.path.path(root_path)
    for root, dirs, files in os.walk(root_path):
        for data_file in files:
            if data_file.endswith(".csv"):
                data_csv.append(os.path.join(root, data_file))
    return data_csv

def tensorflow_train(np_inputs, np_outputs):
    # define model and metrics we are interested in, tanh or elu activations seem to give best results so far
    # going with rmsprop for now, subject to change
    # tracking mse and accuracy for comparisons to Matlab
    if len(np_inputs.shape) > 1:
        dimensions = np_inputs.shape[1]
    else:
        dimensions = 1
    model = Sequential()
    model.add(Dense(10, activation="elu", input_dim=dimensions))
    model.add(Dense(2, activation="elu"))
    model.compile(optimizer="rmsprop", loss="mse", metrics=["accuracy"])
    
    # visualizes the built NN
    model.summary()
    
    # Train the model over 100 epochs, iterating on the data in batches of 256 samples
    model.fit(np_inputs, np_outputs, epochs=100, batch_size=256)

def main():
    config = parse_config()
    abs_path = config["DEFAULT"]["data_path"]
    csv_files = find_csv_paths(abs_path)
    
    # loop over every csv file in data directory and train a NN with it
    for data_set in csv_files:
        csvfile = open(data_set, "r")
        csvreader = csv.reader(csvfile)

        # load inputs/outputs into numpy arrays with a small portion set aside for validation
        inputs = []
        outputs = []
        for row in csvreader:
            if "Freq" in row[0]:    # probably a better way to do this, but it works for our data
                continue
            inputs.append(float(row[0]))
            outputs.append([float(row[1]), float(row[2])])
        inputs = np.array(inputs)
        outputs = np.array(outputs)
        
        tensorflow_train(inputs, outputs)


if __name__ == "__main__":
    main()
