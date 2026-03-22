from app.Problem.Problem import Problem
from app.OptimizationAlgorithm.EvolutionaryAlgorithm import EvolutionaryAlgorithm
from app.OptimizationAlgorithm.SimulatedAnnealing import SimulatedAnnealing
from app.OptimizationAlgorithm.RandomSearch import RandomSearch
import statistics
import os 

class ExperimentRunner:
    def __init__(self):
        # list of instances
        #self.instances = [
        #    "tai20_5_0.fsp", "tai20_10_0.fsp", "tai20_20_0.fsp", 
        #    "tai100_10_0.fsp", "tai100_20_0.fsp", "tai500_20_0.fsp"
        #]
        self.instances = [
            "tai20_5_0.fsp"
        ]

    def run_all(self):
        for instance in self.instances:
            print(f"--- Solving file problem {instance} ---")
            # print(os.getcwd())
            problem = Problem.from_file(f"app/data/{instance}")
            
            # parameters
            pop_size = 100
            generations = 100
            tour_size = 5
            px = 0.7
            pm = 0.1

            # just EA now
            ea_results = []
            for i in range(5):
                ea = EvolutionaryAlgorithm(problem, pop_size, generations, tour_size, px, pm)
                best_ind = ea.run()
                ea_results.append(float(best_ind.fitness))

            # simulated 
            # Hypothèse : ton EA utilise pop_size=100 et generations=100
            total_evals = 100 * 100

            # Tu lances le Recuit Simulé
            sa = SimulatedAnnealing(problem, max_evaluations=total_evals)
            best_sa_solution = sa.run()

            print(f"Meilleur temps trouvé par le Recuit Simulé : {best_sa_solution.fitness}")
                
            print(f"AE - Best: {min(ea_results)}, Avg: {statistics.mean(ea_results):.2f}, Std: {statistics.stdev(ea_results):.2f}")