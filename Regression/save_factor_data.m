clear all; close all;

home = pwd;
data_path = '/Users/Matthew/Documents/MIT/UAP - Basketball/Factors/';
x = dir([data_path '*.csv']);
numPlayers = numel(x);
players = cell(numPlayers, 1);
readme = 'X(i,:) = [location situation fgPercentage takenInterval madeInterval numShots nomMade distance]; Y(i) = made;';


for i = 1:numPlayers
    
    FILE = [data_path x(i).name];
    disp(FILE);
    factors = csvread(FILE, 1, 1);
    numShots = size(factors, 1);
    
    y = regexp(x(i).name, '.csv', 'split');
    player.name = y{1};
    player.numShots = numShots;
    
    X = factors(:, 2:end);
    Y = factors(:, 1);
    
    player.X = X;
    player.Y = Y;
    players{i} = player;
    
    save('players_factors.mat', 'players', 'readme');
end

features = {'location', 'situation', 'fgPercentage', 'takenInterval', 'madeInterval', 'numShots', 'numMade', 'distance'};
save('players_factors.mat', 'players', 'readme', 'features');


