fullSet = readtable('S Parameter 60GHz Huygen FullSet.xlsx'); %Load Data
fullSet = table2array(fullSet);

net = feedforwardnet([10,10]); %create simple net
inputs = fullSet(:,1); %get inputs
inputs = transpose(inputs); %transpose for net training
targets = fullSet(:, 2:3); %get outputs
targets = transpose(targets); %transpose for net training
[net tr] = train(net, inputs, targets); %train the net

save net %save our neural net