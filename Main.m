format longe

KK = 3

for alpha = [0.99, 0.95, 0.9, 0.85, 0.8, 0.75] % honest stake ratio
    for delta = [2, 3, 4, 5] % network delay in slots

        ErrorUB = PoSRandomWalk(alpha, delta, KK)

        % write output to file
        fileName = sprintf("output_%.2f_%d_%d.txt", alpha, delta, KK)
        file = fopen(fileName, "w")
        fprintf(file, "alpha=%f delta=%d K=%d\nErrorUB\n", alpha, delta, KK)
        fdisp(file, ErrorUB)
        fclose(file)
    end
end