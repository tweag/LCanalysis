function res = singleRun(param);
    format longe

    alpha = param(1);
    delta = param(2);
    KK = param(3);
    ErrorUB = PoSRandomWalk(alpha, delta, KK);

    % write output to file
    fileName = sprintf("results/output_%.2f_%d_%d.csv", alpha, delta, KK);
    file = fopen(fileName, "w");
    fprintf(file, "alpha,delta,K,errorUB\n");
    for K = 1:KK
        fprintf(file, "%.2f,%d,%d,%.10e\n", alpha, delta, K, ErrorUB(K))
    end
    fclose(file);
    printf("saved %s\n", fileName);

    res = 0; % useless, but needed for parallel run
end