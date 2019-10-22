[filename,pathname] = uigetfile('.csv','MultiSelect','on');
S11 = readtable(filename{1});
S11 = table2array(S11);
S12 = readtable(filename{2});
S12 = table2array(S12);

frequency = transpose(S11(:,1));
ReS11 = transpose(S11(:,2));
ImS11 = transpose(S11(:,3));
ReS12 = transpose(S12(:,2));
ImS12 = transpose(S12(:,3));
targets = [ReS11;ImS11;ReS12;ImS12];

neuronsPerLayer = 2;
fatNeurons = 2;
startingPointNeurons = neuronsPerLayer;
numLayers = 2;
startingLayers = numLayers;
netStructure = zeros(1,numLayers);
netStructure(1:numLayers) = neuronsPerLayer;

neuronSatisfaction = 0;
fatSatisfaction = 0;

terminator = feedforwardnet(netStructure);
[terminator,tr] = train(terminator,frequency,targets);
originalY = terminator(frequency);
originalPerformance = perform(terminator,targets,originalY);

layers(1,1) = numLayers;
layers(1,2) = originalPerformance;

neurons(1,1) = neuronsPerLayer;
neurons(1,2) = originalPerformance;

layerIteration = 2;
neuronIteration = 2;

fatLayers = numLayers + 1;
fatStructure = zeros(1,fatLayers);
fatStructure(1:fatLayers) = fatNeurons;
fatTerminator = feedforwardnet(fatStructure);
[fatTerminator,fatTr] = train(fatTerminator,frequency,targets);
fatY = fatTerminator(frequency);
fatPerformance = perform(fatTerminator,targets,fatY);

layers(layerIteration,1) = fatLayers;
layers(layerIteration,2) = fatPerformance;
layerIteration = layerIteration + 1;

if fatPerformance < originalPerformance
    previousTerminator = fatTerminator;
    previousPerformance = fatPerformance;
    while fatSatisfaction == 0
        clear fatTerminator;
        clear fatStructure;
        fatLayers = fatLayers + 1;
        fatStructure = zeros(1,fatLayers);
        fatStructure(1:fatLayers) = fatNeurons; 
        fatTerminator = feedforwardnet(fatStructure);
        tic
        [fatTerminator,fatTr] = train(fatTerminator,frequency,targets);
        runtime = toc;
        fatY = fatTerminator(frequency);
        fatPerformance = perform(fatTerminator,targets,fatY);
        layers(layerIteration,1) = fatLayers;
        layers(layerIteration,2) = fatPerformance;
        layerIteration = layerIteration + 1;
        if fatPerformance > previousPerformance || runtime > 300
            fatSatisfaction = 1;
        else
            previousTerminator = fatTerminator;
            previousPerformance = fatPerformance;
        end
    end
else
    previousTerminator = fatTerminator;
    previousPerformance = fatPerformance;
    fatLayers = startingLayers;
    while fatSatisfaction == 0 && fatLayers >= 1
        clear fatTerminator
        clear fatStructure
        fatLayers = fatLayers - 1;
        fatStructure = zeros(1,fatLayers);
        fatStructure(1:fatLayers) = fatNeurons;
        fatTerminator = feedforwardnet(fatStructure);
        tic
        [fatTerminator,fatTr] = train(fatTerminator,frequency,targets);
        runtime = toc;
        fatY = fatTerminator(frequency);
        fatPerformance = perform(fatTerminator,targets,fatY);
        layers(layerIteration,1) = fatLayers;
        layers(layerIteration,2) = fatPerformance;
        layerIteration = layerIteration + 1;
        if fatPerformance > previousPerformance || runtime > 300
            fatSatisfaction = 1;
        else
            previousTerminator = fatTerminator;
            previousPerformance = fatPerformance;
        end
    end
end

neuronsPerLayer = neuronsPerLayer + 1;
netStructure(1:numLayers) = neuronsPerLayer;
newTerminator = feedforwardnet(netStructure);
[newTerminator,newTr] = train(newTerminator,frequency,targets);
newY = newTerminator(frequency);
newPerformance = perform(newTerminator,targets,newY);

neurons(neuronIteration,1) = neuronsPerLayer;
neurons(neuronIteration,2) = newPerformance;
neuronIteration = neuronIteration + 1;

if newPerformance < originalPerformance
    lastTerminator = newTerminator;
    lastPerformance = newPerformance;
    while neuronSatisfaction == 0
        clear newTerminator;
        neuronsPerLayer = neuronsPerLayer + 1;
        netStructure(1:numLayers) = neuronsPerLayer;
        newTerminator = feedforwardnet(netStructure);
        tic
        [newTerminator,newTr] = train(newTerminator,frequency,targets);
        runtime = toc;
        newY = newTerminator(frequency);
        newPerformance = perform(newTerminator,targets,newY);
        neurons(neuronIteration,1) = neuronsPerLayer;
        neurons(neuronIteration,2) = newPerformance;
        neuronIteration = neuronIteration + 1;
        if newPerformance > lastPerformance || runtime > 300
            neuronSatisfaction = 1;
        else
            lastTerminator = newTerminator;
            lastPerformance = newPerformance;
        end
    end
else
    lastTerminator = newTerminator;
    lastPerformance = newPerformance;
    neuronsPerLayer = startingPointNeurons;
    while neuronSatisfaction == 0 && neuronsPerLayer >= 1
        clear newTerminator;
        neuronsPerLayer = neuronsPerLayer - 1;
        netStructure(1:numLayers) = neuronsPerLayer;
        newTerminator = feedforwardnet(netStructure);
        tic
        [newTerminator,newTr] = train(newTerminator,frequency,targets);
        runtime = toc;
        newY = newTerminator(frequency);
        newPerformance = perform(newTerminator,targets,newY);
        neurons(neuronIteration,1) = neuronsPerLayer;
        neurons(neuronIteration,2) = newPerformance;
        neuronIteration = neuronIteration + 1;
        if newPerformance > lastPerformance || runtime > 300
            neuronSatisfaction = 1;
        else
            lastTerminator = newTerminator;
            lastPerformance = newPerformance;
        end
    end
end