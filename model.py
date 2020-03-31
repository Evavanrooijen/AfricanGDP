"""Define model input, params
estimate, fit"""


def CRDW(i, tao=0.4):
  """This function tests for cointegration
      Args:
        i (int): index of the country we are modeling
        tao (float): critical value (default = 0.4)

      Returns:
        JH (array): An array with the regressors (incl. self)

  """

  JH=Y[i]
  for j in range(N):
      if j!=i:
        y = Y[i]
        x = Y[j]
        x = sm.add_constant(x)

        model = sm.OLS(y, x)
        results = model.fit()
        CRDW_j = stats.stattools.durbin_watson(results.resid)
        if CRDW_j > tao:
          JH = np.vstack((JH, Y[j]))
  assert JH.shape[0]>0 # test if JH contains atleast self
  return JH

def correlation(i, kn=4, kp=4):
    """Feature selection based on pairwise correlation
    Args:
        i (int): index of the country we are modeling
        tao (float): critical value (default = 0.4)

    Returns:
        JH (array): An array with the regressors (incl. self)

    """
    corr_i = np.zeros(N)
    for j in range(N):
      corr_i[j] = pearsonr(Y_growth[i], Y_growth[j])[0]

    pos = Y_growth[np.argpartition(corr_i, -(kp+1))[-(kp+1):-1]]
    #pos = Y_growth[corr_i.argsort()[(kp+1):-1]]
    assert pos.shape == (kp, T-1)
    neg = Y_growth[corr_i.argsort()[:kn]]
    assert neg.shape == (kn, T-1)
    #neg = Y_growth[np.argpartition(correlation(7), -5)[-5:-1]]
    return pos, neg
