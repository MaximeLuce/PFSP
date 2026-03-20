import random
import copy
from Individual import *
from EALogger import *

class EvolutionaryAlgorithm:
    def __init__(self, problem, pop_size=100, generations=100, tour_size=5, px=0.7, pm=0.1):
        self.problem = problem
        self.pop_size = pop_size  # size of the population
        self.generations = generations # number of generatio,
        self.tour_size = tour_size # size of the tournament
        self.px = px # crossover probability
        self.pm = pm # mutation probability
        self.population = []
        self.logger = EALogger() # for log the results of each generation

    def initialize_population(self):
        """Initialize the population randomly."""
        self.population = []
        for _ in range(self.pop_size):
            seq = list(range(self.problem.num_jobs))
            random.shuffle(seq)
            ind = Individual(seq)
            ind.evaluate(self.problem)
            self.population.append(ind)

    def tournament_selection(self):
        """Selection by tournament: chose the best among N individuals selected at random."""
        participants = random.sample(self.population, self.tour_size)
        best = min(participants, key=lambda x: x.fitness)
        return copy.deepcopy(best)

    def crossover_ox(self, parent1, parent2):
        """
        Ordered Crossover OX.
        Selects a subsequence from parent 1 and copies it into the child.
        Fills in the rest with genes from parent 2, preserving their order.
        Returns two children by swapping the roles of the parents.
        """
        size = len(parent1.sequence)
        
        def generate_child(p1, p2):
            # Select two random cut points
            start, end = sorted(random.sample(range(size), 2))
            
            # Copy the subsequence of the first parent
            child_seq = [None] * size
            child_seq[start:end+1] = p1.sequence[start:end+1]
            
            # Fill the remaining positions with elements from p2
            # We retrieve the elements from p2 that are not yet in the child
            p2_filtered = [gene for gene in p2.sequence if gene not in child_seq]
            
            # Enter these items from left to right in the “None” fields
            p2_idx = 0
            for i in range(size):
                if child_seq[i] is None:
                    child_seq[i] = p2_filtered[p2_idx]
                    p2_idx += 1
                    
            return Individual(child_seq)

        # We create two children by reversing the order of the parents
        child1 = generate_child(parent1, parent2)
        child2 = generate_child(parent2, parent1)
        
        return child1, child2

    def mutate_swap(self, individual):
        """Mutation Swap : swaps the positions of two random tasks."""
        if random.random() < self.pm:
            idx1, idx2 = random.sample(range(len(individual.sequence)), 2)
            individual.sequence[idx1], individual.sequence[idx2] = individual.sequence[idx2], individual.sequence[idx1]

    def mutate_inversion(self, individual):
        """Inversion: Reverses the order of a random subsequence."""
        if random.random() < self.pm:
            idx1, idx2 = sorted(random.sample(range(len(individual.sequence)), 2))
            individual.sequence[idx1:idx2+1] = reversed(individual.sequence[idx1:idx2+1])

    def run(self):
        """Exécute l'algorithme génétique sur le nombre de générations défini."""
        self.initialize_population()
        self.logger = EALogger() # initialize the logger at the beginning
        
        # Log generatio n0
        self.logger.log_generation(0, self.population)
        
        for gen in range(1, self.generations + 1):
            new_population = []
            
            while len(new_population) < self.pop_size:
                # selection
                p1 = self.tournament_selection()
                p2 = self.tournament_selection()
                
                # Crossover
                if random.random() < self.px:
                    c1, c2 = self.crossover_ox(p1, p2)
                else:
                    c1, c2 = copy.deepcopy(p1), copy.deepcopy(p2)
                
                # Mutation
                """Or inversion !"""
                self.mutate_swap(c1)
                self.mutate_swap(c2)
                
                # Evaluation
                c1.evaluate(self.problem)
                c2.evaluate(self.problem)
                
                new_population.extend([c1, c2])
                
            # Replacement
            self.population = new_population[:self.pop_size]
            
            # Saving the stats of the current generation
            self.logger.log_generation(gen, self.population)
            
        # display the best overall
        best_overall = min(self.population, key=lambda x: x.fitness)
        print(f"Fin de l'évolution. Meilleur fitness trouvé : {best_overall.fitness}")

        #print(min(self.population, key=lambda x: x.fitness).fitness)
        #return min(self.population, key=lambda x: x.fitness)
        
        return best_overall
        
        