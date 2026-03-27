from app.Problem.Problem import Problem
from app.OptimizationAlgorithm.EvolutionaryAlgorithm import EvolutionaryAlgorithm
from app.OptimizationAlgorithm.SimulatedAnnealing import SimulatedAnnealing
from app.OptimizationAlgorithm.RandomSearch import RandomSearch
from app.OptimizationAlgorithm.Greedy import Greedy
import statistics
import time
import os
import csv

class SAParameters:
    def __init__(self):
        # Pour tester rapidement, on garde une seule instance. 
        # Tu pourras décommenter les autres plus tard.
        self.instances = [
            "tai20_5_0.fsp", 
            # "tai20_10_0.fsp", "tai20_20_0.fsp", 
            # "tai100_10_0.fsp", "tai100_20_0.fsp",
            #"tai500_20_0.fsp"
        ]
        self.best_known_value = [
             "14033",
            # "20911", "33623",
            # "300566", "367267",
            #"6697476"
        ]

        self.cases = [
            # Best initial_temp
            {"id": "25", "initial_temp": 100, "cooling_rate": 0.99},
            {"id": "26", "initial_temp": 1000, "cooling_rate": 0.99},
            {"id": "27", "initial_temp": 10000, "cooling_rate": 0.99},

            # Best cooling_rate
            
        ]

    def _calc_stats(self, results):
        """Auxiliary function to computer best, worst, avg, std"""
        best = min(results)
        worst = max(results)
        avg = statistics.mean(results)
        std = statistics.stdev(results) if len(results) > 1 else 0.0
        return best, worst, avg, std

    def run_all(self):
        # main parameters
        runs_per_algo = 10 
        
        csv_filepath = "app/Results/SAParameters.csv"
        
        print(f"Start running... Results will be saved to {csv_filepath}")
    

        file_exists = os.path.isfile(csv_filepath)
        with open(csv_filepath, mode='a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            
            if not file_exists:
                header = [
                    "Case_ID", "Instance",
                    "SA_Best", "SA_Worst", "SA_Avg", "SA_Std", "SA_Time(s)", "SA_NFE_Avg",
                    "Best_Known_Value"
                ]
                writer.writerow(header)

            for idx, instance in enumerate(self.instances):
                problem = Problem.from_file(f"app/Data/{instance}")
                best_known_value = self.best_known_value[idx]

                
                # diplay result for the instance
                nom_inst = instance.replace(".fsp", "")

                print(f"\n{'='*50}")
                print(f"=== ANALYZING INSTANCE: {nom_inst} ===")
                print(f"{'='*50}")
                
                for case in self.cases:
                    print(f"\n--- RUNNING CASE {case['id']} ---")
                    print(f"Params: Pop={case['pop_size']}, Gen={case['generations']}, Total Evals={case['pop_size'] * case['generations']}")
                    
                    # Récupération des paramètres du cas courant
                    initial_temp = case["initial_temp"]
                    cooling_rate = case["cooling_rate"]
                    
                    total_evals = 10000

                    # Simulated Annealing [10x]
                    sa_results = []
                    sa_evals = []
                    t0_sa = time.perf_counter()
                    for _ in range(runs_per_algo):
                        problem.reset_counter() # set to 0 the NFE counter
                        sa = SimulatedAnnealing(problem, max_evaluations=total_evals)
                        best_ind = sa.run()
                        sa_evals.append(problem.evaluations_count)
                        sa_results.append(float(best_ind.fitness))
                    t_sa = time.perf_counter() - t0_sa
                    sa_b, sa_w, sa_a, sa_s = self._calc_stats(sa_results)
                    sa_b_evals, sa_w_evals, sa_a_evals, sa_s_evals = self._calc_stats(sa_evals)

                    print("End of computation for SimulatedAnnealing")


                    # display head of table
                    
                    
                    print("-" * 135)
                    print(f"{'Instance':<15} | {'SA [10x]':<26} | {'Best known value'}")
                    print(f"{nom_inst:<15} |  {'best*   worst  avg    std':<26} |")
                    print("-" * 135)

                    sa_str = f"{sa_b:>5.0f} {sa_w:>6.0f} {sa_a:>6.1f} {sa_s:>5.1f}"
                    sa_evals_str = f"{sa_b_evals:>5.0f} {sa_w_evals:>6.0f} {sa_a_evals:>6.1f} {sa_s_evals:>5.1f}"

                    print(f"{'Score':<15} | {sa_str:<26} | {best_known_value}")
                    print(f"{'Time':<15} |  {t_sa:>5.1f}s |")
                    print(f"{'NFE':<15} | {sa_evals_str:<26} |")
                    print("-" * 135)

                    row = [
                        case['id'], instance,
                        round(sa_b, 1), round(sa_w, 1), round(sa_a, 2), round(sa_s, 2), round(t_sa, 3), round(sa_a_evals, 1),
                        best_known_value
                    ]
                    writer.writerow(row)
                    
                    # force saving
                    file.flush()
                    print(f"Case {case['id']} saved!")