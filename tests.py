from functions import *

N = 10
T = 50
Y = create_DGP(N, T, 1, 1)

a = 1
i = 0
T1_size = int((T*a)/(1+a))

JH, pos, neg, self_gr, params, rank = define_parameters(Y, i)
beta = np.ones(rank)
print(beta.dot(JH).shape)
print(np.multiply(np.ones(1), self_gr).shape)
#beaten = run_simulation(Y,a)

#print(beaten)
