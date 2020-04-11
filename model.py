from functions import create_DGP, run_single_estimation

N =10
T=50
alpha=1
var_eps=1
a=1
i=0


Y = create_DGP(N, T, alpha, var_eps)

predictions, predictions_IMA, truth, RMSPE_i, RMSPE_IMA_i, params = run_single_estimation(Y, i, a)
print(RMSPE_i)
print(truth)
