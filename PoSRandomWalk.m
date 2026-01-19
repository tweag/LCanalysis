function ErrorUB = PoSRandomWalk(alpha, delta, KK)

% alpha is honest stake ratio
% delta is network delay, in slots
% KK is the max number of confirmation to evaluate

D = delta * 1/20; % network delay (measured in block interval)
                  % Cardano 20s per block

Alphabet = 10;
States = 19;
% Alphabet is max possible epoch length
%   need to be large enough to ensure numeric precision of P(j, 2)
%   as well as negligible probability of larger j
% States is the number of states in the Markov chain tracked

[Pa, PH, PD, PA, PAD] = PoSSlotPdf(alpha, D, Alphabet);

% PoS warmup and final stages are the same as PoW
St0 = PoWMCWarmupUB(PAD, Alphabet, States);
Error = zeros(KK, 1);
tic
for K = 1:KK
    St2 = PoSMCConfirmUB(K, Pa, PH, PD, PA, St0, Alphabet, States);
    Error(K) = PoWMCFinalUB(PAD, St2, Alphabet, States);
end
toc
ErrorUB = Error;

% % Lower bound may no longer be relevant for Peras
% St0 = PoWMCWarmupLB(PAD, Alphabet, States);
% Error = zeros(KK, 1);
% tic
% for K = 1:KK
%     % private mining as lower bound
%     St2 = PoSMCConfirmPM(K, Pa, PH, PD, PA, PAD, St0, Alphabet, States);
%     Error(K) = PoWMCFinalLB(PAD, St2, Alphabet, States);
% end
% toc
% ErrorLB = Error;

end
