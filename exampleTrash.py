from functions import *
import streamlit as st

st.title('Forecasting African GDP Growth')

T = st.sidebar.slider('Select Time Horizon (T): ', 10, 100,50)
N = st.sidebar.slider('Select #Countries (N): ', 10, 100,50)
runs = st.sidebar.slider('Select #runs (runs): ', 1, 100,1)
a = st.sidebar.selectbox('Select a',[1, 2, 5])
var_eps = st.sidebar.selectbox('Select variance of epsilon',[0.5, 1])
alpha = st.sidebar.selectbox('Select alpha',[1, 2, 5])

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
if st.checkbox('Show Example'):
    i = st.sidebar.slider('Select Country (i): ', 0, N,0)
    Y = create_DGP(N, T, alpha, var_eps)
    st.write('GDP Levels Country {}'.format(i))
    st.line_chart(Y[i])
    st.write('GDP Growth Country {}'.format(i))
    st.line_chart(growth_rate(Y[i]))

"""
    predictions, predictions_IMA, truth, RMSPE_i, RMSPE_IMA_i = run_single_estimation(Y, i, a)

    st.write('## Our Predictions')
    st.line_chart(predictions)
    st.write('## Benchmark Predictions')
    st.line_chart(predictions_IMA)
    st.write('## True Values')
    st.line_chart(truth)



    #st.line_chart(np.transpose(CRDW(Y, 0)))
    #pos, neg, self = max_min_correlations(Y, 0)
    #st.line_chart(pos)
    # plot cointegration
    st.write('## Cointegration Terms')
    #st.line_chart(cointegration)

    # plot correlation
    st.write('## Correlation Terms')
    #st.line_chart(correlation)
    # show estimated parameters

    # plot fit
    st.write('## Model Fit')
    # plot residuals
    st.write('## Residuals')
    # fit and plot IMA(1, 1)
    st.write('## IMA Model Fit')
    # table with RMSPE comparison
    st.write('## Model Comparison')

    # count across simulation runs
"""
