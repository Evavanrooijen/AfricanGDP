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

if st.checkbox('Show Example', value=True):
    i = st.slider('Select Country (i): ', 0, N,0)
    #Y = create_DGP(N, T, alpha, var_eps)
    st.write('GDP Levels Country {}'.format(i))
    st.line_chart(Y[i])
    st.write('GDP Growth Country {}'.format(i))
    st.line_chart(growth_rate(Y[i]))

    st.write('Step 1: CRDW')
    tao = st.selectbox('Select tao',[0.4, 0.7], index=1)
    JH, pos, neg, self_gr, params, rank = define_parameters(Y, i)

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

    a = st.selectbox('Select a',[1, 2, 5])
    predictions, predictions_IMA, truth, RMSPE_i, RMSPE_IMA_i, params = run_single_estimation(Y, i, a, 2)
    if st.checkbox('Show Fitted Parameter Values'):
        for name, value in params.valuesdict().items():
            st.write(name, value)

    st.write('RMSPE for country {} is {} for our model against a benchmark of {}'.format(i, RMSPE_i, RMSPE_IMA_i))


    # plot fit
    st.write('## Model Fit')
    st.line_chart(predictions, truth)
    # plot residuals
    st.write('## Residuals')
    st.line_chart(predictions-truth)
    # fit and plot IMA(1, 1)
    st.write('## IMA Model Fit')
    st.line_chart(predictions_IMA)
    # table with RMSPE comparison
    st.write('## Model Comparison')
    st.line_chart([predictions, predictions_IMA, truth])

    runs = st.slider('Select #runs (runs): ', 1, 100,1)
    st.write('## Simulation runs')
    scoresBeaten = np.zeros(runs)
    for run in range(runs):
        scoresBeaten[run] = run_simulation(Y,a, tao)
    beatenScore = np.mean(scoresBeaten)
    st.write('Over {} runs, we beat on average {} out of {} countries'.format(runs, beatenScore, N))
