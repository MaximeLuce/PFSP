import numpy as np
from app.Problem.DataLoader import * # use in the alternative constructor

class Problem:
    """
    Represents an instance of the problem and contains evaluation function.
    """
    
    def __init__(self, num_jobs, num_machines, processing_times):
        self.num_jobs = num_jobs # number of jobs
        self.num_machines = num_machines # numbers of machines
        self.processing_times = processing_times # matrix M x J of the processing_times

    def __str__(self):
        return f'Problem with {self.num_jobs} tasks and {self.num_machines} machines. Matrix = {self.processing_times}'
        
    @classmethod
    def from_file(cls, filepath):
        """Alternatif constructor to instance a problem directly with a file."""
        num_jobs, num_machines, processing_times = DataLoader.load_from_file(filepath)
        return cls(num_jobs, num_machines, processing_times)

    def evaluate(self, sequence):
        """
        Compute objective function f(x) for x a given sequence, x is a list of indices of tasks (0 to J-1).
        """
        M = self.num_machines # number of machines
        J = self.num_jobs # number of jobs
        p = self.processing_times # matrix of the problem
        
        # we define the matrix of completion C : C[m][j] represents the time completion of the jth task of the sequence on machine m
        C = np.zeros((M, J), dtype=int) # we set it first to zeros_(m x J)
        
        # First step : first task on the first machine (j=1, m=1 so index 0, 0)
        C[0][0] = p[0][sequence[0]]
        
        # Step two : other tasks on the first machine (m=1, j>1)
        for j in range(1, J):
            C[0][j] = C[0][j-1] + p[0][sequence[j]]
            
        # Step three : first task on others machines (j=1, m>1)
        for m in range(1, M):
            C[m][0] = C[m-1][0] + p[m][sequence[0]]
            
        # Last step : other tasks on others machines (j>1, m>1)
        for m in range(1, M):
            for j in range(1, J):
                C[m][j] = max(C[m][j-1], C[m-1][j]) + p[m][sequence[j]]
                
        # f(x) = sum on all the tasks on the last machine
        total_flow_time = np.sum(C[M-1, :])
        
        return total_flow_time


