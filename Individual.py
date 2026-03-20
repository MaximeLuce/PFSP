import random
import copy

class Individual:
    """Represents a potential solution (an individual)."""
    def __init__(self, sequence):
        self.sequence = sequence  # La permutation des tâches (ex: [3, 1, 0, 2])
        self.fitness = float('inf') # f(x) : le temps de flux total (à minimiser)

    def check_sequence(self, problem):
        if len(self.sequence) != problem.num_jobs:
            return False

    def evaluate(self, problem):
        """Evaluate the quality of the solution using the problem evaluation feature."""
        self.fitness = problem.evaluate(self.sequence)