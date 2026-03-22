import random
import copy

class Individual:
    """Represents a potential solution (an individual)."""
    def __init__(self, sequence):
        self.sequence = sequence  # permutation of task
        self.fitness = float('inf') # f(x) total processing time

    def check_sequence(self, problem): # TO COMPLETE
        if len(self.sequence) != problem.num_jobs:
            return False

    def evaluate(self, problem):
        """Evaluate the quality of the solution using the problem evaluation feature."""
        self.fitness = problem.evaluate(self.sequence)