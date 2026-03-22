import math
import random
import copy
from app.OptimizationAlgorithm.OptimizationAlgorithm import OptimizationAlgorithm
from app.Problem.Individual import Individual

class SimulatedAnnealing(OptimizationAlgorithm):
    def __init__(self, problem, max_evaluations, initial_temp=1000.0, cooling_rate=0.99):
        super().__init__(problem) # constructor of OptimizationAlgorithm
        self.max_evaluations = max_evaluations
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate

    def generate_neighbor(self, current_individual):
        """
        Generates a neighboring solution by applying a slight modification.
        Here, with the "swap" method.
        """
        # create a copy of the sequence to not erase the original one
        neighbor_seq = current_individual.sequence.copy()
        
        # pic 2 random index to swap
        idx1, idx2 = random.sample(range(len(neighbor_seq)), 2)
        neighbor_seq[idx1], neighbor_seq[idx2] = neighbor_seq[idx2], neighbor_seq[idx1]
        
        return Individual(neighbor_seq)

    def run(self):
        """Executes the simulated annealing algorithm."""
        
        # create a random first solution
        initial_seq = list(range(self.problem.num_jobs))
        random.shuffle(initial_seq)
        current_sol = Individual(initial_seq)
        current_sol.evaluate(self.problem)
        
        # we keep track of the best solution found
        best_sol = copy.deepcopy(current_sol)
        
        # set up temperature
        T = self.initial_temp
        
        # main loop
        for i in range(1, self.max_evaluations):
            # create and evaluate a neighbor
            neighbor = self.generate_neighbor(current_sol)
            neighbor.evaluate(self.problem)
            
            # compute the difference
            delta_f = neighbor.fitness - current_sol.fitness
            
            if delta_f < 0: # the neighbor is better
                current_sol = neighbor

                if neighbor.fitness < best_sol.fitness: # if better, we update
                    best_sol = copy.deepcopy(neighbor)
            
            # if the neighbor is worst, we accept it with a probability
            else:
                probability = math.exp(-delta_f / T)
                if random.random() < probability:
                    current_sol = neighbor
                    
            # cooling down
            T = T * self.cooling_rate
            
            # warning on the zero machine
            if T < 1e-10:
                T = 1e-10
                
        return best_sol