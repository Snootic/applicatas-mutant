from pandas import *
import numpy as np
from scipy.stats import binom


def distBinomial( n, p, testes=10, x_min=0, x_max=0):
    k = range(testes)
    dist = binom.pmf(k,n,p)
    
    print(dist)
    
    if x_max == 0 and x_max < x_min:
        dist_filtrada = dist[x_min-1:] if x_min > 0 else dist[x_min:]
    else:
        dist_filtrada = dist[x_min-1:x_max+1] if x_min > 0 else dist[x_min:x_max+1]

    print(dist_filtrada)
    
    soma = sum(dist_filtrada)
    
    print(soma)
    
    esperanca = n * p
    
    print(esperanca)
    
    q = 1 - p
    variancia = n * p * q
    desvio_padrao = np.sqrt(variancia)
    
    print(variancia)
    print(desvio_padrao)
    
    return dist, dist_filtrada, soma, esperanca, desvio_padrao
    
        
if __name__ == '__main__':
    a = distBinomial(10, 0.2, x_max = 1)
        