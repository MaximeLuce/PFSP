from om.problem.Problem import Problem
from om.OptimizationAlgorithm.EvolutionaryAlgorithm import EvolutionaryAlgorithm
from om.OptimizationAlgorithm.RandomSearch import RandomSearch
import statistics
import os 

class ExperimentRunner:
    def __init__(self):
        # list of instances
        self.instances = [
            "tai20_5_0.fsp", "tai20_10_0.fsp", "tai20_20_0.fsp", 
            "tai100_10_0.fsp", "tai100_20_0.fsp", "tai500_20_0.fsp"
        ]

    def run_all(self):
        for instance in self.instances:
            print(f"--- Solving file problem {instance} ---")
            # print(os.getcwd())
            problem = Problem.from_file(f"om/data/{instance}")
            
            # just EA now
            ea_results = []
            for i in range(5):
                ea = EvolutionaryAlgorithm(problem)
                best_ind = ea.run()
                ea_results.append(float(best_ind.fitness))
                
            print(f"AE - Best: {min(ea_results)}, Avg: {statistics.mean(ea_results):.2f}, Std: {statistics.stdev(ea_results):.2f}")