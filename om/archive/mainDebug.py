import numpy as np

from om.problem.DataLoader import * # class to load the .fsp file
from om.problem.Problem import * # class that contain a problem

if __name__ == "__main__":

    filepath = "data/tai20_5_0.fsp"
    
    try:
        # initialization of the problem
        problem = Problem.from_file(filepath)
        print(f"Data well loaded: {problem.num_jobs} tasks, {problem.num_machines} and matrice M = \n{problem.processing_times}.")
        
        # example of sequence
        example_sequence = list(range(problem.num_jobs))
        
        # evaluation of the sequence
        score = problem.evaluate(example_sequence)
        print(f"Séquence évaluée: {example_sequence}")
        print(f"Temps total (Total flow time) f(x) = {score}")
        
    except FileNotFoundError:
        print(f"Problem with the file {filepath} (not existing).")