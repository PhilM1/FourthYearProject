fullSet = readtable('PillData.xlsx'); %Load Data
fullSet = table2array(fullSet);

net = feedforwardnet([10,10]); %create simple net
inputs = fullSet(:,1:2); %get inputs
inputs = transpose(inputs); %transpose for net training
targets = fullSet(:, 3:6); %get outputs
targets = transpose(targets); %transpose for net training
[net tr] = train(net, inputs, targets); %train the net

save net %save our neural net