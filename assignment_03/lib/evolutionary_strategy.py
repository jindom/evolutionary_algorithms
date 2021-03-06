from __future__ import division
import numpy as np
import random
from itertools import chain
from logger import LOG
from common_algo import fitness_func
GENERATION = 0


def random_vector(pop_range):
    return [round(a, 2) for a in np.random.random_sample(pop_range) * pop_range*2 - pop_range]


def random_steps(pop_range):
    return [round(a, 2) for a in np.random.random_sample(pop_range)]


def random_gaussian(mu, sigma):
    return np.random.normal(mu, sigma)


def mutate_problem(vector, stdv):
    # x'i = xi + sigma'i*Ni(0,1)
    i = 0
    child = []
    new_child = 0
    mutate_id = random.randint(0, len(vector))
    for v in vector:
        if mutate_id == i:
            new_child = v + (stdv[i]*random_gaussian(0, 1))
        else:
            new_child = v
        i = i + 1
        child.append(new_child)
    return child


def mutate_strategy(stdv, p):
    # sigma'i = sigmai * e(tao_p*N(0,1) + tao * Ni(0,1))
    sigma_p = []
    tau = 1.0/(np.sqrt(2.0*len(stdv)))
    tau_p = 1.0/np.sqrt(2*np.sqrt(len(stdv)))
    for i in stdv:
        sigma = i * np.exp(tau_p * random_gaussian(0, 1) + tau * random_gaussian(0, 1))
        new_sigma = sigma * p
        if new_sigma > 2:
            new_sigma = new_sigma % 2
        new_sigma = 1 - new_sigma
        sigma_p.append(new_sigma)
    return sigma_p


def mutate(vector, stdv, p):
    new_stdv = mutate_strategy(stdv, p)
    new_vector = mutate_problem(vector, new_stdv)
    return new_vector, new_stdv


def init_population(pop_range):
    pop = random_vector(pop_range)
    stdv = random_steps(pop_range)
    return pop, stdv


def search_es(max_gens, pop_range, ad_mut_stp, mu_lambda):
    pop = init_population(pop_range)
    best = fitness_func(pop[0])
    p = 1.5
    for gen in range(0, max_gens-1):
        children = mutate(pop[0], pop[1], p)
        LOG.debug("children>{0}".format(children))
        fitness = fitness_func(children[0])
        if fitness <= best:
            best = fitness
            pop = children
            p = 1.5
        else:
            p = 1.5 ** (-1/4)
        if mu_lambda:
            pop = init_population(pop_range)
            best = fitness_func(pop[0])
        LOG.rbf("Generation>{0}:new best>{1}".format(gen, best))
    return best
