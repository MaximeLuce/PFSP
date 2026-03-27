from app.Problem.Problem import Problem
from app.OptimizationAlgorithm.EvolutionaryAlgorithm import EvolutionaryAlgorithm
from app.OptimizationAlgorithm.SimulatedAnnealing import SimulatedAnnealing
from app.OptimizationAlgorithm.RandomSearch import RandomSearch
from app.OptimizationAlgorithm.Greedy import Greedy
import statistics
import time
import os
import csv

class ExperimentRunner:
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
        
        csv_filepath = "app/Results/experiment_results.csv"
        
        print(f"Start running... Results will be saved to {csv_filepath}")
        
        # old default parameters
        '''
        pop_size = 100
        generations = 100
        total_evals = pop_size * generations  # 10 000 for default parameteres
        
        # for EA
        tour_size = 5
        px = 0.7
        pm = 0.1
        mutation = 'swap' # or 'inversion'
        crossover = 'ox' # or 'pmx'
        '''

        file_exists = os.path.isfile(csv_filepath)
        with open(csv_filepath, mode='a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            
            if not file_exists:
                header = [
                    "Case_ID", "Instance", "Population Size", "Generations number", "Px", "Pm", "Tour", "Mutation Type", "Crossover Type",
                    "RS_Best", "RS_Worst", "RS_Avg", "RS_Std", "RS_Time(s)", "RS_NFE",
                    "GR_Best", "GR_Time(s)", "GR_NFE",
                    "EA_Best", "EA_Worst", "EA_Avg", "EA_Std", "EA_Time(s)", "EA_NFE_Avg",
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
                    pop_size = case["pop_size"]
                    generations = case["generations"]
                    tour_size = case["tour"]
                    px = case["px"]
                    pm = case["pm"]
                    mutation = case["mutation"]
                    crossover = case["crossover"]
                    elitism = case["elitism"]
                    
                    total_evals = pop_size * generations

                    # Random Search [10x]
                    rs_results = []
                    rs_evals = []
                    t0_rs = time.perf_counter()
                    for _ in range(runs_per_algo):
                        problem.reset_counter() # set to 0 the NFE counter
                        rs = RandomSearch(problem, max_evaluations=total_evals)
                        best_ind = rs.run()
                        rs_results.append(float(best_ind.fitness))
                        rs_evals.append(problem.evaluations_count)
                    t_rs = time.perf_counter() - t0_rs
                    rs_b, rs_w, rs_a, rs_s = self._calc_stats(rs_results)
                    rs_b_evals, rs_w_evals, rs_a_evals, rs_s_evals = self._calc_stats(rs_evals)

                    print("End of computation for RandomSearch")

                    # Greedy [1x]
                    problem.reset_counter() # set to 0 the NFE counter
                    t0_gr = time.perf_counter()
                    greedy = Greedy(problem)
                    best_greedy = greedy.run()
                    t_gr = time.perf_counter() - t0_gr
                    gr_b = float(best_greedy.fitness)
                    gr_evals = problem.evaluations_count
                    
                    print("End of computation for Greedy")

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
                    print(f"{'Instance':<15} | {'Random Alg. [10k]':<26} | {'Greedy Alg.':<11} | {'Evol. Alg. [10x]':<26} | {'SA [10x]':<26} | {'Best known value'}")
                    print(f"{nom_inst:<15} | {'best*   worst  avg    std':<26} | {'best*':<11} | {'best*   worst  avg    std':<26} | {'best*   worst  avg    std':<26} |")
                    print("-" * 135)

                    
                    rs_str = f"{rs_b:>5.0f} {rs_w:>6.0f} {rs_a:>6.1f} {rs_s:>5.1f}"
                    gr_str = f"{gr_b:>5.0f}"
                    ea_str = f"{ea_b:>5.0f} {ea_w:>6.0f} {ea_a:>6.1f} {ea_s:>5.1f}"
                    sa_str = f"{sa_b:>5.0f} {sa_w:>6.0f} {sa_a:>6.1f} {sa_s:>5.1f}"

                    rs_evals_str = f"{rs_b_evals:>5.0f} {rs_w_evals:>6.0f} {rs_a_evals:>6.1f} {rs_s_evals:>5.1f}"
                    gr_evals_str = f"{gr_evals:>5.0f}"
                    ea_evals_str = f"{ea_b_evals:>5.0f} {ea_w_evals:>6.0f} {ea_a_evals:>6.1f} {ea_s_evals:>5.1f}"
                    sa_evals_str = f"{sa_b_evals:>5.0f} {sa_w_evals:>6.0f} {sa_a_evals:>6.1f} {sa_s_evals:>5.1f}"

                    print(f"{'Score':<15} | {rs_str:<26} | {gr_str:<11} | {ea_str:<26} | {sa_str:<26} | {best_known_value}")
                    print(f"{'Time':<15} | {t_rs:>7.2f}s {'':<17} | {t_gr:>6.4f}s {'':<3} | {t_ea:>7.2f}s {'':<17} | {t_sa:>5.1f}s |")
                    print(f"{'NFE':<15} | {rs_evals_str:<26} | {gr_evals_str:<11} | {ea_evals_str:<26} | {sa_evals_str:<26} |")
                    print("-" * 135)

                    row = [
                        case['id'], instance, pop_size, generations, px, pm, tour_size, mutation, crossover,
                        round(rs_b, 1), round(rs_w, 1), round(rs_a, 2), round(rs_s, 2), round(t_rs, 3), round(rs_a_evals, 1),
                        round(gr_b, 1), round(t_gr, 3), gr_evals,
                        round(ea_b, 1), round(ea_w, 1), round(ea_a, 2), round(ea_s, 2), round(t_ea, 3), round(ea_a_evals, 1),
                        round(sa_b, 1), round(sa_w, 1), round(sa_a, 2), round(sa_s, 2), round(t_sa, 3), round(sa_a_evals, 1),
                        best_known_value
                    ]
                    writer.writerow(row)
                    
                    # force saving
                    file.flush()
                    print(f"Case {case['id']} saved!")