from pandas import *
import numpy as np
from scipy.stats import binom


def distBinomial(n, p, testes=10, x_min=0, x_max=0):
    k = range(testes+1)
    dist = binom.pmf(k,n,p)

    if x_max == 0 and x_max <= x_min:
        dist_filtrada = dist[x_min:] if x_min > 0 else dist[:]
    else:
        dist_filtrada = dist[x_min:x_max+1] if x_min > 0 else dist[x_min:x_max+1]
    
    soma = sum(dist_filtrada)

    esperanca = n * p
    
    q = 1 - p
    variancia = n * p * q
    desvio_padrao = np.sqrt(variancia)
    
    return dist, dist_filtrada, soma, esperanca, desvio_padrao
    
        
if __name__ == '__main__':
    a = distBinomial(10, 0.2, x_max = 1)
        