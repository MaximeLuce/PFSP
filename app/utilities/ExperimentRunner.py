from app.Problem.Problem import Problem
from app.OptimizationAlgorithm.EvolutionaryAlgorithm import EvolutionaryAlgorithm
from app.OptimizationAlgorithm.SimulatedAnnealing import SimulatedAnnealing
from app.OptimizationAlgorithm.RandomSearch import RandomSearch
from app.OptimizationAlgorithm.Greedy import Greedy
import statistics
import time

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

    def _calc_stats(self, results):
        """Fonction utilitaire pour calculer best, worst, avg, std"""
        best = min(results)
        worst = max(results)
        avg = statistics.mean(results)
        std = statistics.stdev(results) if len(results) > 1 else 0.0
        return best, worst, avg, std

    def run_all(self):
        # main parameters
        runs_per_algo = 10 
        pop_size = 100
        generations = 100
        total_evals = pop_size * generations  # 10 000 for default parameteres
        
        # for EA
        tour_size = 5
        px = 0.7
        pm = 0.1

        # display head of table
        print("-" * 135)
        print(f"{'Instance':<15} | {'Random Alg. [10k]':<26} | {'Greedy Alg.':<11} | {'Evol. Alg. [10x]':<26} | {'SA [10x]':<26} | {'Best known value'}")
        print(f"{'':<15} | {'best*   worst  avg    std':<26} | {'best*':<11} | {'best*   worst  avg    std':<26} | {'best*   worst  avg    std':<26} |")
        print("-" * 135)

        for idx, instance in enumerate(self.instances):
            problem = Problem.from_file(f"app/data/{instance}")
            best_known_value = self.best_known_value[idx]
            
            # Random Search [10x]
            rs_results = []
            t0_rs = time.perf_counter()
            for _ in range(runs_per_algo):
                rs = RandomSearch(problem, max_evaluations=total_evals)
                best_ind = rs.run()
                rs_results.append(float(best_ind.fitness))
            t_rs = time.perf_counter() - t0_rs
            rs_b, rs_w, rs_a, rs_s = self._calc_stats(rs_results)

            print("End of computation for RandomSearch")

            # Greedy [1x]
            t0_gr = time.perf_counter()
            greedy = Greedy(problem)
            best_greedy = greedy.run()
            t_gr = time.perf_counter() - t0_gr
            gr_b = float(best_greedy.fitness)
            
            print("End of computation for Greedy")

            # Evolutionary Algorithm [10x]
            ea_results = []
            t0_ea = time.perf_counter()
            for _ in range(runs_per_algo):
                ea = EvolutionaryAlgorithm(problem, pop_size, generations, tour_size, px, pm)
                best_ind = ea.run()
                ea_results.append(float(best_ind.fitness))
            t_ea = time.perf_counter() - t0_ea
            ea_b, ea_w, ea_a, ea_s = self._calc_stats(ea_results)

            print("End of computation for EA")

            # Simulated Annealing [10x]
            sa_results = []
            t0_sa = time.perf_counter()
            for _ in range(runs_per_algo):
                sa = SimulatedAnnealing(problem, max_evaluations=total_evals)
                best_ind = sa.run()
                sa_results.append(float(best_ind.fitness))
            t_sa = time.perf_counter() - t0_sa
            sa_b, sa_w, sa_a, sa_s = self._calc_stats(sa_results)

            print("End of computation for SimulatedAnnealing")

            # diplay result for the instance
            nom_inst = instance.replace(".fsp", "")
            
            rs_str = f"{rs_b:>5.0f} {rs_w:>6.0f} {rs_a:>6.1f} {rs_s:>5.1f}"
            gr_str = f"{gr_b:>5.0f}"
            ea_str = f"{ea_b:>5.0f} {ea_w:>6.0f} {ea_a:>6.1f} {ea_s:>5.1f}"
            sa_str = f"{sa_b:>5.0f} {sa_w:>6.0f} {sa_a:>6.1f} {sa_s:>5.1f}"

            print(f"{nom_inst:<15} | {rs_str:<26} | {gr_str:<11} | {ea_str:<26} | {sa_str:<26} | {best_known_value}")
            print(f"{'-> Time (Total)':<15} | {t_rs:>7.2f}s {'':<17} | {t_gr:>6.4f}s {'':<3} | {t_ea:>7.2f}s {'':<17} | {t_sa:>7.2f}s |")

        print("-" * 135)