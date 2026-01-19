function res = singleRun(param);
    format longe

    alpha = param(1);
    delta = param(2);
    KK = param(3);
    ErrorUB = PoSRandomWalk(alpha, delta, KK);

    % write output to file
    fileName = sprintf("output_%.2f_%d_%d.txt", alpha, delta, KK);
    file = fopen(fileName, "w");
    fprintf(file, "alpha=%f delta=%d K=%d\nErrorUB\n", alpha, delta, KK);
    fdisp(file, ErrorUB);
    fclose(file);
    printf("saved %s\n", fileName);

    res = 0; % useless, but needed for parallel run
end