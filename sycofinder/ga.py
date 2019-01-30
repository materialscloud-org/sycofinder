#! /usr/bin/env python
from __future__ import division, print_function
from builtins import zip, range  # pylint: disable=redefined-builtins
from deap import base, creator
import numpy as np
import random
import scipy.stats as ss
## creating types ##
creator.create("FitnessMax", base.Fitness, weights=(1.0, ))
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()

## setting up the GA ##


# pylint: disable=unused-argument
def evaluate(individual):
    # since we rely on experiment, to run GA we just put an arbitrary value for fitness function
    return 1.0


## initializing the population with old population ##
def initIndividual(icls, content):
    a = icls(content[:-1])
    a.fitness.values = tuple([content[-1]])
    return a


def initPopulation(pcls, ind_init, input_data, var_names):
    if var_names[-1].lower() not in ['fitness','scores','rank']:
        raise ValueError("Last column needs to be 'fitness'")

    fitness = input_data[:, -1]

    return pcls(ind_init(c) for c in input_data), var_names[:-1]


toolbox.register("individual_guess", initIndividual, creator.Individual)
toolbox.register("population_guess", initPopulation, list,
                 toolbox.individual_guess)


def rankInds(pcls):
    # this function returns the ranking of fitness values #
    scores = []
    for icls in pcls:
        scores.append(-1 * icls.fitness.values[0])
    return ss.rankdata(scores, method="min")


def selectProportionate(chances):
    # this function selects an individual with a probability proportional to their fitness
    s = sum(chances)
    normalized_chances = [c / s for c in chances]
    # choosing ind1
    p = normalized_chances[0]
    x = random.random()
    ind1 = 0
    while x > p:
        ind1 = ind1 + 1
        p = p + normalized_chances[ind1]

    # choosing ind2 not the same as ind1
    ind2 = ind1
    while ind2 == ind1:
        p = normalized_chances[0]
        x = random.random()
        ind2 = 0
        while x > p:
            ind2 = ind2 + 1
            p = p + normalized_chances[ind2]

    return ind1, ind2

def selectTournament(chances,tournament_size):
    # this function selects individuals by running sets of tournaments between individuals.
    # The chance of winning a tournament is proportional to the the fitness of participants.
    participants1=random.sample(range(len(chances)),k=tournament_size)
    chances_tourn1 = [chances[i] for i in participants1]
    s = sum(chances_tourn1)
    normalized_chances = [c / s for c in chances_tourn1]
    # choosing ind1
    p = normalized_chances[0]
    x = random.random()
    ind1 = 0
    while x > p:
        ind1 = ind1 + 1
        p = p + normalized_chances[ind1]
    ind1 = participants1[ind1]
    # choosing ind2 not the same as ind1
    participants2=[ind1]
    while ind1 in participants2:
        participants2=random.sample(range(len(chances)),k=tournament_size)
    chances_tourn2 = [chances[i] for i in participants2]
    s = sum(chances_tourn2)
    normalized_chances = [c / s for c in chances_tourn2]
    # choosing ind2
    p = normalized_chances[0]
    x = random.random()
    ind2 = 0
    while x > p:
        ind2 = ind2 + 1
        p = p + normalized_chances[ind2]
    ind2 = participants2[ind2]


    return ind1, ind2



def mateIntermediate(par1, par2, nvar):
    # this function applies intermediate crossover operation on two parents to generate a child
    par1_genes = [par1.__getitem__(i) for i in range(nvar)]
    par2_genes = [par2.__getitem__(i) for i in range(nvar)]
    child_genes = [
        p1 + random.random() * (p2 - p1)
        for p1, p2 in zip(par1_genes, par2_genes)
    ]
    return child_genes


def mutGaussian(offspring, var_std):
    # this function applies a gaussian mutation. I need to add a user defined variable ranges to it later
    mutated_genes = [
        g + np.random.normal(loc=0.0, scale=std)
        for g, std in zip(offspring, var_std)
    ]
    mutated_genes = [g if g >= 0 else 0 for g in mutated_genes]
    return mutated_genes


def main(input_data, var_names,mutation_shrink_factor):
    pop, variables = toolbox.population_guess(input_data, var_names)
    # print("variables: ", variables)
    # print("Old population has %i individuals." % (len(pop)))
    # using rank instead of fitness #
    rank = rankInds(pop)
    selection_chance = [
        1 / np.sqrt(r) for r in rank
    ]  # the chance of being chose to reproduce offsprings is proportional to 1/sqrt(r)
    # mutation standard deviation based on variables ranges. Need to be corrected later! #
    UB = np.amax(input_data[:, :-1], axis=0)
    LB = np.amin(input_data[:, :-1], axis=0)
    varSTD = [mutation_shrink_factor*(m - n) / 5.0 for m, n in zip(UB, LB)]
    migration_rate, mutation_rate, number_generations = 0.1, 0.2, 1
    tournament_size=4
    new_pop = []
    for i in range(len(pop)):
        if random.random() < migration_rate:  # migration
            # indv1, indv2 = selectProportionate(selection_chance)
            indv1, indv2 = selectTournament(selection_chance,tournament_size)
            offspring = [
                pop[indv1].__getitem__(i) for i in range(len(variables))
            ]
            if random.random() < mutation_rate:
                offspring = mutGaussian(offspring, varSTD)

        else:
            ## selecting two parents with chances proportional to their rank
            # indv1, indv2 = selectProportionate(selection_chance)
            indv1, indv2 = selectTournament(selection_chance,tournament_size)
            parent1, parent2 = pop[indv1], pop[indv2]
            ## Apply crossover and mutation on the offspring
            offspring = mateIntermediate(parent1, parent2, len(variables))
            if random.random() < mutation_rate:
                offspring = mutGaussian(offspring, varSTD)

        new_pop.append(offspring)


    return np.array(new_pop), variables
