pkg load parallel

alphas = [0.99, 0.95, 0.9, 0.85, 0.8, 0.75]; % honest stake ratio
deltas = [2, 3, 4, 5]; % network delay in slots
KK = 25;

params = zeros([(length(alphas) * length(deltas))  3]);
index = 1;

for alpha = alphas
    for delta = deltas
        params(index++, :) = [alpha, delta, KK];
    end
end

pararrayfun(nproc-1, @(rowIdx) singleRun(params(rowIdx, :)), 1:rows(params));
