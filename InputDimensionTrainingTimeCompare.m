training_time = 0;
dimensions = 1;
inputs = rand(1, 5000);
outputs = rand(4, 5000);
time_history = [];

while training_time < 60
    net = feedforwardnet(10);
    [net tr] = train(net, inputs, outputs);
    training_time = tr.time(length(tr.time));
    fprintf("Dimensionality: %d\nTime to Train: %d\n\n", dimensions, training_time);
    inputs = [inputs;rand(1, length(inputs(1,:)))];
    dimensions = dimensions + 1;
    time_history = [time_history, training_time];
end

plot(1:dimensions, time_history)
title("Neural Net Inputs Vs. Time to Train (5000 Random Generated Data Points)")
xlabel('Number of Input Vectors')
ylabel('Time to Train')
