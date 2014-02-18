clear all; close all;

load players_factors.mat
numPlayers = numel(players);
player_indices = [1:numPlayers];

for i = 1:numPlayers
    player = players{i};
    if player.numShots > 1000
        X = player.X;
        
        Y = player.Y;
        [b,dev,stats] = glmfit(X, Y, 'binomial', 'link', 'logit');
        display(sprintf('%s %i shots', player.name, player.numShots));
        for j = 1:8
            f = features{j};
            display(sprintf('\t%s b=%g (pval=%g)', f, b(j+1), stats.p(j+1)));
        end
    end
end

    