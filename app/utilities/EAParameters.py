from app.Problem.Problem import Problem
from app.OptimizationAlgorithm.EvolutionaryAlgorithm import EvolutionaryAlgorithm
import statistics
import time
import os
import csv

class ExperimentRunner:
    def __init__(self):
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
            # Best Ratio Population/Generations Size
            {"id": 1, "pop_size": 100, "generations": 100, "px": 0.7, "pm": 0.1, "tour": 5, "mutation": "swap", "crossover": "ox", "elitism": 0},
            {"id": 2, "pop_size": 20, "generations": 500, "px": 0.7, "pm": 0.1, "tour": 5, "mutation": "swap", "crossover": "ox", "elitism": 0},
            {"id": 3, "pop_size": 1000, "generations": 10, "px": 0.7, "pm": 0.1, "tour": 5, "mutation": "swap", "crossover": "ox", "elitism": 0},
            {"id": 4, "pop_size": 10000, "generations": 1, "px": 0.7, "pm": 0.1, "tour": 5, "mutation": "swap", "crossover": "ox", "elitism": 0}

            # Best Generations Size
            
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
        
        csv_filepath = "app/Results/EAParameters.csv"
        
        print(f"Start running... Results will be saved to {csv_filepath}")
        
        file_exists = os.path.isfile(csv_filepath)
        with open(csv_filepath, mode='a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            
            if not file_exists:
                header = [
                    "Case_ID", "Instance", "Population Size", "Generations number", "Px", "Pm", "Tour", "Mutation Type", "Crossover Type",
                    "EA_Best", "EA_Worst", "EA_Avg", "EA_Std", "EA_Time(s)", "EA_NFE_Avg",
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
                    pop_size = case["pop_size"]
                    generations = case["generations"]
                    tour_size = case["tour"]
                    px = case["px"]
                    pm = case["pm"]
                    mutation = case["mutation"]
                    crossover = case["crossover"]
                    elitism = case["elitism"]
                    
                    total_evals = pop_size * generations


                    # Evolutionary Algorithm [10x]
                    ea_results = []
                    ea_evals = []
                    t0_ea = time.perf_counter()
                    for _ in range(runs_per_algo):
                        problem.reset_counter() # set to 0 the NFE counter
                        ea = EvolutionaryAlgorithm(problem, pop_size, generations-1, tour_size, px, pm, mutation, crossover, elitism)
                        best_ind = ea.run()
                        ea_results.append(float(best_ind.fitness))
                        ea_evals.append(problem.evaluations_count)
                    t_ea = time.perf_counter() - t0_ea
                    ea_b, ea_w, ea_a, ea_s = self._calc_stats(ea_results)
                    ea_b_evals, ea_w_evals, ea_a_evals, ea_s_evals = self._calc_stats(ea_evals)

                    print("End of computation for EA")

                    # display head of table
                    
                    
                    print("-" * 135)
                    print(f"{'Instance':<15} | {'Evol. Alg. [10x]':<26} | {'Best known value'}")
                    print(f"{nom_inst:<15} |  {'best*   worst  avg    std':<26}  |")
                    print("-" * 135)

                    ea_str = f"{ea_b:>5.0f} {ea_w:>6.0f} {ea_a:>6.1f} {ea_s:>5.1f}"
                   
                    ea_evals_str = f"{ea_b_evals:>5.0f} {ea_w_evals:>6.0f} {ea_a_evals:>6.1f} {ea_s_evals:>5.1f}"
                    
                    print(f"{'Score':<15} | {ea_str:<26} | {best_known_value}")
                    print(f"{'Time':<15} | {t_ea:>7.2f}s {'':<17} |")
                    print(f"{'NFE':<15} | {ea_evals_str:<26} |")
                    print("-" * 135)

                    row = [
                        case['id'], instance, pop_size, generations, px, pm, tour_size, mutation, crossover,
                        round(ea_b, 1), round(ea_w, 1), round(ea_a, 2), round(ea_s, 2), round(t_ea, 3), round(ea_a_evals, 1),                        best_known_value
                    ]
                    writer.writerow(row)
                    
                    # force saving
                    file.flush()
                    print(f"Case {case['id']} saved!")