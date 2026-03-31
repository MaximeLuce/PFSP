# Permutation Flowshop Scheduling Problem (PFSP)

## Context of this project

This project is a part of the course "Optimization Methods: Theory and Applications" at the Wroclaw Univeristy of Science and Technology (project).

It aims to study the Permutation Flowshop Scheduling Problem (PFSP) which is an NP-hard problem. The purpose of this project is to compare efficently different algorithms to solve it. We will compare:

- random search
- greedy
- Evolutionary Algorithm (EA) with different parameters
  - Population size
  - Crossover probability
  - Mutation probability
  - Tour size
  - Number of generation
  - Crossover methods : OX and PMX
  - Mutation methods : Swap or Inversion
- Simulated Annealing with two parameters
  - initial temperature
  - cooling rate

## Naviguation

- `app`: all the pythons file of the project
    - `Data`: instance of the problem (commin from [GitHub Pages]([https://pages.github.com/](https://github.com/chneau/go-taillard/tree/master/pfsp/instances))
    - `Utilities`: EALogger, ExperimentRunner
    - `Tests`: Unit tests on the class
    - `Problem`: DataLoader, Individual, Problem
    - `OptimizationAlgorithm`: EvolutionaryAlgorithm, OptimizationAlgorithm, RandomSearch
    - `Results`: folder where all csv were exported and contains file to export CSV to LaTeX tables
    - `Archive`: old files
- `Topic`: PDF files of the exercise goal and description
- `Report`: Report on the project
- `Figures`: Convergence graphs and figures
- `Notes`: some of my notes during the project

### Modules used for this project

#### Standard and external modules
* `abc` (and `ABC`, `abstractmethod`)
* `copy` (and `copy()`, `deepcopy()`)
* `csv` (and `writer()`, `writerow()`, `DictWriter()`, `writeheader()`, `writerows()`)
* `math` (and `exp()`)
* `matplotlib.pyplot` (and `figure()`, `plot()`, `title()`, `xlabel()`, `ylabel()`, `legend()`, `grid()`, `show()`, `savefig()`, `close()`)
* `numpy` (and `zeros()`)
* `os` (and `path.isfile()`, `environ`)
* `random` (and `random()`, `sample()`, `shuffle()`)
* `statistics` (and `mean()`, `stdev()`)
* `time` (and `perf_counter()`)
* `timeit` (and `default_timer()`)

#### Built-ins
* `enumerate()`
* `float()`
* `len()`
* `max()`
* `min()`
* `open()`
* `reversed()`
* `round()`
* `sorted()`

#### Methods for lists, strings and files
* `append()`
* `extend()`
* `flush()`
* `index()`
* `remove()`
* `replace()`
* `sort()`

### To Do
- buffer of last generation
- complete the check_sequence method of the class Individual

## License

MIT License

Copyright (c) 2026 Maxime LUCE

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
