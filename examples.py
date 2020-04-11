from functions import *
import streamlit as st

st.title('Forecasting African GDP Growth')
T = st.sidebar.slider('Select Time Horizon (T): ', 10, 100,50)
N = st.sidebar.slider('Select #Countries (N): ', 10, 100,50)
var_eps = st.sidebar.selectbox('Select variance of epsilon',[0.5, 1])
alpha = st.sidebar.selectbox('Select alpha',[1, 2, 5])
if st.sidebar.button('Generate Data'):
     Y = create_DGP(N, T, alpha, var_eps)

st.write('Generate Data by specifying parameters in the sidebar.')
runs = st.slider('Select #runs (runs): ', 1, 100,1)
a = st.selectbox('Select a',[1, 2, 5])

st.write('## Model Comparison')
st.write('For {} countries and a time horizon of {} '.format(N, T))
"""
scores = np.random.rand(runs)
for run in range(runs):
    Y = create_DGP(N, T, alpha, var_eps)
    scores[run] = run_simulation(Y,a) # score out of N
scoreSpec = np.mean(scores)
st.write('The average number of times we beat the benchmark out of {} simulation runs is {}'.format(runs, scoreSpec))
"""
#Y_test = create_DGP(N, T, alpha, var_eps)
if st.checkbox('Show Example'):
    i = st.slider('Select Country (i): ', 0, N,0)
    #Y_test = create_DGP(N, T, alpha, var_eps)
    st.write('GDP Levels Country {}'.format(i))
    st.line_chart(Y[i])
    st.write('GDP Growth Country {}'.format(i))
    st.line_chart(growth_rate(Y[i]))

    st.write('Step 1: CRDW')
    tao = st.selectbox('Select tao',[0.4, 0.7])
    JH, pos, neg, self_gr, params, rank = define_parameters(Y, i)
    #assert JH.shape == (rank, T-2)
    #assert pos.shape == (4, T-2)
    #assert neg.shape == (4, T-2)
    st.write('We find {} cointegration series'.format(rank-1))
    if st.checkbox('Show Time Series'):
        st.dataframe(JH)

    st.write('Step 2: Correlations')
    format = st.selectbox('Select a visualization', ['Table', 'Plot'])
    if st.checkbox('Show Highest Correlation Series'):
        # show country with correlation value instead of messy plot
        if format == 'Table':
            st.dataframe(pos)
        if format == 'Plot':
            st.line_chart(np.transpose(pos))
    if st.checkbox('Show Lowest Correlation Series'):
        if format == 'Table':
            st.dataframe(neg)
        if format == 'Plot':
            st.line_chart(np.transpose(neg))

    st.write('Step 3: Define Parameters')
    st.write('optional to add initialization values here')
    if st.checkbox('Show Initial Parameter Values'):
        for name, value in params.valuesdict().items():
            st.write(name, value)

    st.write('Step 4: Model Fitting')
    T1_size = int((T*a)/(1+a))
    t = st.slider('Select Time (t): ', T1_size, T,T1_size)
    t = t-T1_size
    JH_T1, pos_T1, neg_T1, self_T1 = rolling_training(T1_size, t, rank, JH, pos, neg, self_gr)
    out = minimize(residual, params, args=(pos_T1, neg_T1, self_T1, JH_T1, rank), method='leastsq', maxfev=1000000)
    JH_T2, pos_T2, neg_T2, self_T2 = rolling_test(T1_size, t, rank, JH, pos, neg, self_gr)
    if st.checkbox('Show Fitted Parameter Values'):
        for name, value in params.valuesdict().items():
            st.write(name, value)
    prediction_t = step_forecast(pos_T2, neg_T2, JH_T2, self_T2, rank, params)
    st.write('Predition for time {}: growth level of {}'.format(t, prediction_t))

    st.write('Step 5: Calculate RMSPE over T2')
    predictions = np.zeros(T-T1_size-1)
    for t in range(T-T1_size-1):
        JH_T1, pos_T1, neg_T1, self_T1 = rolling_training(T1_size, t, rank, JH, pos, neg, self_gr)
        out = minimize(residual, params, args=(pos_T1, neg_T1, self_T1, JH_T1, rank), method='leastsq', maxfev=1000000)
        JH_T2, pos_T2, neg_T2, self_T2 = rolling_test(T1_size, t, rank, JH, pos, neg, self_gr)

        predictions[t] = step_forecast(pos_T2, neg_T2, JH_T2, self_T2, rank, params)
        truth = growth_rate(Y[i])[T1_size:]
        RMSPE_i = calculate_RMSPE(predictions, truth)
    st.write('Step 6: Calculate RMSPE Benchmark')
    predictions_IMA = np.zeros(T-T1_size-1)
    for t in range(T-T1_size-1):
        model = ARIMA(growth_rate(Y[i])[t:T1_size+t], order=(0,1,1))
        model_fit = model.fit(disp=0)
        predictions_IMA[t] = model_fit.forecast(steps=1)[0]
        RMSPE_IMA_i = calculate_RMSPE(predictions_IMA, truth)

    st.write('RMSPE for country {} is {} for our model against a benchmark of {}'.format(i, RMSPE_i, RMSPE_IMA_i))
    st.write('## Simulation runs')
    scoresBeaten = np.zeros(runs)
    for run in range(runs):
        scoresBeaten[run] = run_simulation(Y,a, tao)
    beatenScore = np.mean(scoresBeaten)
    beatenVar = np.var(scoresBeaten)
    st.write('Over {} runs, we beat on average {} out of {} countries (variance: {})'.format(runs, beatenScore, N, beatenVar))

    # plot fit
    st.write('## Model Fit')
    # plot residuals
    st.write('## Residuals')
    # fit and plot IMA(1, 1)
    st.write('## IMA Model Fit')
    # table with RMSPE comparison
    st.write('## Model Comparison')

    # count across simulation runs