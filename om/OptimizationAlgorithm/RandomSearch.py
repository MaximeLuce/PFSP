import random
import copy
from om.problem.Individual import *
from om.OptimizationAlgorithm.OptimizationAlgorithm import *

class RandomSearch(OptimizationAlgorithm):
    def __init__(self, problem, pop_size=50000):
        super().__init__(problem)
        #self.problem = problem
        self.pop_size = pop_size
        self.population = []
        self.history = []

    def initialize_population(self):
        """Initialize the population randomly."""
        self.population = []
        self.history = []
        for _ in range(self.pop_size):
            seq = list(range(self.problem.num_jobs))
            random.shuffle(seq)
            ind = Individual(seq)
            ind.evaluate(self.problem)
            self.history.append(ind.fitness)
            self.population.append(ind)

    def run(self):
        """Runs the genetic algorithm for the specified number of generations."""
        self.initialize_population()
            
        best_gen = min(self.population, key=lambda x: x.fitness).fitness
        best_gen_seq = min(self.population, key=lambda x: x.fitness).sequence

        worst_gen = max(self.population, key=lambda x: x.fitness).fitness
        worst_gen_seq = max(self.population, key=lambda x: x.fitness).sequence

        average = sum(self.history)/self.pop_size
        
        return best_gen, best_gen_seq, worst_gen, worst_gen_seq, average