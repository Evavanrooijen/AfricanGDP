from functions import *
N = 10
T = 50
Y = create_DGP(N, T, 1, 1)

a = 1
i = 0
T1_size = int((T*a)/(1+a))
JH, pos, neg, self_gr, params, rank = define_parameters(Y, i)
if rank > 1:
    print(rank)
    t = 1
    JH_T1, pos_T1, neg_T1, self_T1 = rolling_training(T1_size, t, rank, JH, pos, neg, self_gr)

    JH_T2, pos_T2, neg_T2, self_T2 = rolling_test(T1_size, t, rank, JH, pos, neg, self_gr)
    print(neg[0])
    print(neg[:, 1:][0])
    print(neg[:, 1:].shape)

    def run_simulationTest(Y,a, tao=0.4):
      N = Y.shape[0]
      T = Y.shape[1]
      T1_size = int((T*a)/(1+a))

      RMSPE = np.zeros(N)
      RMSPE_IMA = np.zeros(N)
      beaten = 0

      for i in range(N):
        predictions = np.zeros(T-T1_size-2)
        predictions_IMA = np.zeros(T-T1_size-2) # make copy of pred for simplicity
        truth = growth_rate(Y[i])[T1_size+1:] # to check

        assert truth.size == predictions.size

        JH, pos, neg, self_gr, params, rank = define_parameters(Y, i, tao)

        for t in range(T-T1_size-1):
          JH_T1, pos_T1, neg_T1, self_T1 = rolling_training(T1_size, t, rank, JH, pos, neg, self_gr)
          out = minimize(residual, params, args=(pos_T1, neg_T1, self_T1, JH_T1, rank), method='leastsq', maxfev=1000000)
          JH_T2, pos_T2, neg_T2, self_T2 = rolling_test(T1_size, t, rank, JH, pos, neg, self_gr)

          predictions[t] = step_forecast(pos_T2, neg_T2, JH_T2, self_T2, rank, params)

          model = ARIMA(growth_rate(Y[i])[t:T1_size+t], order=(0,1,1))
          model_fit = model.fit(disp=0)
          predictions_IMA[t] = model_fit.forecast(steps=1)[0] # Check the other scalar and 1x2 returned arrays

        RMSPE_i = calculate_RMSPE(predictions, truth)
        RMSPE_IMA_i = calculate_RMSPE(predictions_IMA, truth)
        print('Hello!')
        if RMSPE_i>RMSPE_IMA_i:
            print('Hello! We lost....')
            beaten += 1

      return beaten


    print(run_simulation(Y, a))
