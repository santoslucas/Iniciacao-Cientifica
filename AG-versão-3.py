#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import math
import random


# Função-objetivo $f(x) = \sum_{i=1}^{n} x_i^2$

# In[ ]:


def fquadratica(x):
    return np.sum( x*x )


# função quadrática $f(x) = \sum_{i=1}^{n} x_i^2-3 x_i+5$
#     min: [1,5 ; 2,8]

# In[ ]:


def fparabola(x):
    return np.sum(pow(x, 2) - 3*x + 5)


# função multiplicação $f(x) = x*y*z$

# In[ ]:


def fmultiplicacao(x):
    return np.multiply(x)


# Geração da população inicial:
# 
# Parâmetros:
# - ps: tamanho da população
# - n: número de variáveis
# - lb, ub: limites inferior e superior para cada variável
# 
# Saída:
# - parent_pop: população de pais (ps $\times$ n)

# In[ ]:


def pop_inicial(ps, n, lb, ub):
    parent_pop = np.random.uniform(lb, ub, (ps, n))
    return parent_pop


# Avalia função-objetivo (fitness)
# 
# Parâmetros:
# - fobj: função-objetivo
# - pop: população
# - ps: tamanho da população
# 
# Saída:
# - pop_f: avaliação da população

# In[ ]:


def avalia_pop(fobj, pop, ps, num_avalia):
    num_avalia += 1
    pop_f = np.zeros(ps)
    for i in range(ps):
        pop_f[i] = fobj(pop[i])
    return pop_f, num_avalia


# Seleção por torneio binário
# 
# Parâmetros:
# - ps: tamanho da população
# - pop_f: avaliação da população
# 
# Saída:
# - sel: pares de índices de soluções selecionadas (ps $\times$ 2)

# In[ ]:


def torneio_binario(ps, pop_f):
    ip1 = np.zeros(ps)
    ip2 = np.zeros(ps)
    
    i11 = np.arange(0, ps)
    np.random.shuffle(i11)
    i12 = np.arange(0, ps)
    np.random.shuffle(i12)
    
    i21 = np.arange(0, ps)
    np.random.shuffle(i21)
    i22 = np.arange(0, ps)
    np.random.shuffle(i22)
    
    for i in range(ps):
        if pop_f[ i11[i] ] < pop_f[ i12[i] ]:
            ip1[i] = i11[i]
        else:
            ip1[i] = i12[i]
        
        if pop_f[ i21[i] ] < pop_f[ i22[i] ] and i21[i] != ip1[i]:
            ip2[i] = i21[i]
        elif ip2[i] != i22[i]:
            ip2[i] = i22[i]
        elif (i+1) < ps:
            ip2[i] = i22[i+1]
    
    return np.stack((ip1, ip2)).astype(int)


# Seleção por Classificação
# 
# Parâmetros:
# - ps: tamanho da população
# - pop_f: avaliação da população
# 
# Saída:
# - sel: índices de soluções selecionadas (ps $\times$ 2)

# In[ ]:


def classificacao(ps, pop_f):
    si = np.argsort(pop_f)
    sel = np.zeros(ps)

    i=0
    j=0

    while i<ps:
        rand = random.randint(0, 9)
        if (j >= rand and si[j] != -1):
            sel[i] = si[j]
            si[j] = -1
            i += 1
        
        j += 1

        if j == ps:
            j = 0

    return sel


# Cruzamento via combinação linear
# 
# Entrada:
# - pais: população de pais
# - ps: tamanho da população
# - n: número de variáveis
# - sel: índices de seleção
# 
# Saída:
# - filhos: população de filhos (ps $\times$ n)

# In[ ]:


def cruzamento_linear(pais, ps, n, sel):
    alpha = np.random.uniform(0, 1, ps)
    filhos = np.zeros((ps, n))
    for i in range(ps):
        filhos[i] = alpha[i] * pais[ sel[0][i] ] + (1 - alpha[i]) * pais[ sel[1][i] ]
    return filhos


# Mutação Gaussiana
# - pop: população
# - ps: tamanho da população
# - n: número de variáveis
# - pm: probabilidade de mutação
# - std: desvio padrão da mutação
# 
# Saída:
# - pop: população mutada

# In[ ]:


def mutacao_gaussiana(pop, ps, n, pm, std):
    for i in range(ps):
        if np.random.uniform() < pm:
            pop[i] += np.random.normal(0, std, n)
    return pop


# Mutação de inversão simples
# - pop: população
# - ps: tamanho da população
# - n: número de variáveis
# - pm: probabilidade de mutação
# 
# Saída:
# - pop: população mutada

# In[ ]:


def mutacao_inversao(pop, ps, n, pm):
    for i in range(ps):
        if np.random.uniform() < pm:
            ponto1 = random.randint(1, n-1)
            ponto2 = random.randint(1, n-1)

            if ponto1 == ponto2:
                break

            if ponto2<ponto1:
                aux = ponto1
                ponto1 = ponto2
                ponto2 = aux

            j=ponto1
            while j < (math.floor(ponto2/2)):
                aux = pop[i][j]
                pop[i][j] = pop[i][ponto2-j]
                pop[i][ponto2-j] = aux
                j+=1

    return pop


# Cruzamento por single-point
# 
# - pais: população de pais
# - ps: tamanho da população
# - n: número de variáveis
# 
# Saída:
# - filhos: população de filhos (ps $\times$ n)

# In[ ]:


def cruzamento_1point(pais, ps, n, sel):
    filhos = np.zeros((ps, n))
    
    i=0
    while i < ps:
        j = random.randint(0, n-1)
        
        aux = pais[int(sel[i])][j]
        pais[int(sel[i])][j] = pais[int(sel[i+1])][j]
        pais[int(sel[i+1])][j] = aux

        filhos[i] = pais[int(sel[i])]
        filhos[i+1] = pais[int(sel[i+1])]
        i = i+2
    
    return filhos
    


# Próxima população de pais
# 
# Entrada:
# - pais: população de pais
# - pais_f: avaliação dos pais
# - filhos: população de filhos
# - filhos_f: avaliação dos filhos
# - ps: tamanho da população
# 
# Saída:
# - pais: nova população de pais

# In[ ]:


def proximos_pais(pais, pais_f, filhos, filhos_f, ps):
    pop = np.concatenate((pais, filhos))
    pop_f = np.concatenate((pais_f, filhos_f))
    
    si = np.argsort(pop_f)
    
    best = pop[ si[0] ]
    best_f = pop_f[ si[0] ]
    
    si = si[1:]
    np.random.shuffle(si)
    
    pais[0], pais_f[0] = best, best_f
    pais[1:], pais_f[1:] = pop[ si[0:ps-1] ], pop_f[ si[0:ps-1] ]
    
    return pais, pais_f


# 
# FUNÇÃO MAIN

# In[ ]:


# MAIN
ps, n, lb, ub = 10, 3, -5, 5
pm, std = 0.10, 0.01
max_avalia = 500
num_avalia = 0

pais = pop_inicial(ps, n, lb, ub)
print(pais)


# In[ ]:


pais_f, num_avalia = avalia_pop(fquadratica, pais, ps, num_avalia)
print(pais_f)


# In[ ]:


while(num_avalia != max_avalia):   
    # seleção por meio de classificação
    sel = classificacao(ps, pais_f)

    # cruzamento
    filhos = cruzamento_1point(pais, ps, n, sel)
    filhos = mutacao_inversao(filhos, ps, n, pm)
    filhos_f, num_avalia = avalia_pop(fquadratica, filhos, ps, num_avalia)
    
    # novos pais
    pais, pais_f = proximos_pais(pais, pais_f, filhos, filhos_f, ps)


# In[ ]:


pais


# In[ ]:


pais_f


# In[ ]:


print("Melhor solução encontrada: ", pais[0])
print("Melhor avaliação: ", pais_f[0])
print("Número de avaliações: ", num_avalia)

