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
- Simulated Annealing

## Naviguation

- `app`: all the pythons file of the project
    - `Data`: instance of the problem (commin from [GitHub Pages]([https://pages.github.com/](https://github.com/chneau/go-taillard/tree/master/pfsp/instances))
    - `Utilities`: EALogger, ExperimentRunner
    - `Tests`: Unit tests on the class
    - `Problem`: DataLoader, Individual, Problem
    - `OptimizationAlgorithm`: EvolutionaryAlgorithm, OptimizationAlgorithm, RandomSearch
    - `Archive`: old files
- `Topic`: PDF files of the exercise goal and description
- `Report`: Report on the project

## Notepad

### Todo
- buffer of last generation
- stop condition
- export table latex for report
- PMX crossover
- complete the check_sequence method of the class Individual

### Questions to ask
- order of protocol for analysis of parameteres
- time computation VS number of evaluation ? adding number of evaluation

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
