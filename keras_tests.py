from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
import numpy as np
import csv

csvfile = open("10 GHz Reflection Re Im.csv", "r")
csvreader = csv.reader(csvfile)

inputs = []
outputs = []
for row in csvreader:
    if "Freq" in row[0]:
        continue
    inputs.append(float(row[0]))
    outputs.append([float(row[1]), float(row[2])])
inputs = np.array(inputs)
outputs = np.array(outputs)

# For a single-input model with 2 classes (binary classification):
model = Sequential()
model.add(Dense(10, activation='elu', input_dim=1))
model.add(Dense(2, activation='elu'))
model.compile(optimizer='rmsprop',
              loss='mse',
              metrics=['accuracy'])

# Generate dummy data
# data = np.random.random((1000, 100))
# labels = np.random.randint(2, size=(1000, 1))

# Train the model, iterating on the data in batches of 32 samples
model.fit(inputs, outputs, epochs=600, batch_size=256)