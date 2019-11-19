#!/usr/bin/python3
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow import saved_model
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


def find_new_data(abs_data_path, rel_model_path):
    model_list = os.listdir(rel_model_path)
    data_list = []
    for root, dirs, files in os.walk(abs_data_path):
        for data_file in files:
            if data_file.endswith(".csv") and data_file.split(".")[0] not in model_list:
                print("[*] Found new data set: %s" % data_file)
                data_list.append(os.path.join(root, data_file))
    if len(data_list) == 0:
        print("[*] No new data was found")
    return data_list


def tensorflow_train(np_inputs, np_outputs, model_path):
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
    
    # loop over every csv file in data directory and train a NN with it
    i = 1
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
        
        print("[*] Training model %d of %d" % (i, len(csv_files)))
        new_model = tensorflow_train(inputs, outputs, trained_models)
        filename = os.path.basename(data_set).split(".")[0]       # name trained models the same as the csv file, but without the extension

        try:
            saved_model.save(new_model, os.path.join(trained_models, filename))
        except:
            print("[!!] Problem writing trained model to disk. Does the path specified in the config exist and have write permissions for this user?")
            pass
        
        i += 1
        

if __name__ == "__main__":
    main()
