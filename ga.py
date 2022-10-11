from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PolynomialMutation
import pymoo.problems.single as single_obj
from pymoo.core.termination import Termination
from pymoo.optimize import minimize
import numpy as np

def ga(fobj, max_eval, pop_size, p_cross, eta_cross, p_mut, eta_mut, eliminate_duplicates):
    if fobj == 1:
        problem = single_obj.Ackley(n_var=10)
    elif fobj == 2:
        problem = single_obj.Griewank(n_var=10)
    elif fobj == 3:
        problem = single_obj.Rastrigin(n_var=10)
    # elif fobj == 4:
    #     problem = single_obj.Rosenbrock(n_var=10)
    # elif fobj == 5:
    #     problem = single_obj.Sphere(n_var=10)

    algorithm = GA(
        pop_size=pop_size,
        crossover=SBX(eta=eta_cross, prob_per_variable=p_cross),
        mutation=PolynomialMutation(eta=eta_mut, prob=p_mut),
        eliminate_duplicates=eliminate_duplicates)
    
    algorithm.setup(problem=problem, termination=('n_eval', max_eval))

    res = minimize(problem,
                algorithm,
                # seed=1,
                verbose=True)
    
    return float(res.F)

# print(ga(1, max_eval=1000, pop_size=100, p_cross=1.0, eta_cross=2.0, p_mut=0.1, eta_mut=10, eliminate_duplicates=True))