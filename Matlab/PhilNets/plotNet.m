xDat = fullSet(:,1);
yDatReal = fullSet(:,2);
yDatIm = fullSet(:,3);

ySim = sim(net, inputs);
ySimReal = ySim(1,:);
ySimReal = transpose(ySimReal);
ySimIm = ySim(2,:);
ySimIm = transpose(ySimIm);

yDeltaReal = yDatReal - ySimReal;
yDeltaIm = yDatIm - ySimIm;

figure(1);
scatter(xDat,yDatReal,1);
title('HFSS Real re(S(1:2,1:2))');
xlabel('Frequency [GHz]');
ylabel('re(S(1:2,1:2))');

figure(2);
scatter(xDat,ySimReal,1);
title('Neural Net Real re(S(1:2,1:2))');
xlabel('Frequency [GHz]');
ylabel('re(S(1:2,1:2))');

figure(3);
scatter(xDat,yDatIm,1);
title('HFSS Imaginary im(S(1:2,1:2))');
xlabel('Frequency [GHz]');
ylabel('im(S(1:2,1:2))');

figure(4);
scatter(xDat,ySimIm,1);
title('Neural Net Imaginary im(S(1:2,1:2))');
xlabel('Frequency [GHz]');
ylabel('im(S(1:2,1:2))');

figure(5);
scatter(xDat,yDeltaReal,1);
title('Difference between HFSS and Neural Net re(S(1:2,1:2))');
xlabel('Frequency [GHz]');
ylabel('HFSS - NeuralNet [re(S(1:2,1:2))]');

figure(6);
scatter(xDat,yDeltaIm,1);
title('Difference between HFSS and Neural Net im(S(1:2,1:2))');
xlabel('Frequency [GHz]');
ylabel('HFSS - NeuralNet [im(S(1:2,1:2))]');

figure(6);
scatter(xDat,yDeltaReal,1);
hold on;
scatter(xDat,yDeltaIm,1);
hold off
ylim([-0.001, 0.001]);
legend('Real Diff', 'Imaginary Diff');
title('Difference between HFSS and Neural Net real and imaginary');
xlabel('Frequency [GHz]');
ylabel('HFSS - NeuralNet');

