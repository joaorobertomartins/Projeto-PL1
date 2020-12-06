"""
Real Python Linear Programming example

https://realpython.com/linear-programming-python/
"""

import numpy as np
from scipy.optimize import linprog
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable
from pulp import GLPK


def main_scipy():
    """
    linprog() solves only minimization (not maximization)

    obj holds the coefficients from the objective function.
    lhs_ineq holds the left-side coefficients from the inequality (red, blue, and yellow) constraints.
    rhs_ineq holds the right-side coefficients from the inequality (red, blue, and yellow) constraints.
    lhs_eq holds the left-side coefficients from the equality (green) constraint.
    rhs_eq holds the right-side coefficients from the equality (green) constraint.

    linprog() returns a data structure with these attributes:
    .con is the equality constraints residuals.
    .fun is the objective function value at the optimum (if found).
    .message is the status of the solution.
    .nit is the number of iterations needed to finish the calculation.
    .slack is the values of the slack variables, or the differences between the values of the left and right sides of
    the constraints.
    .status is an integer between 0 and 4 that shows the status of the solution, such as 0 for when the optimal solution
    has been found.
    .success is a Boolean that shows whether the optimal solution has been found.
    .x is a NumPy array holding the optimal values of the decision variables.


    SciPy can’t run various external solvers.
    SciPy can’t work with integer decision variables.
    SciPy doesn’t provide classes or functions that facilitate model building. You have to define arrays and matrices,
    which might be a tedious and error-prone task for large problems.
    SciPy doesn’t allow you to define maximization problems directly. You must convert them to minimization problems.
    SciPy doesn’t allow you to define constraints using the greater-than-or-equal-to sign directly. You must use the
    less-than-or-equal-to instead.

    :return: None
    """
    obj = [-1, -2]
    lhs_ineq = [[2, 1], [-4, 5], [1, -2]]
    rhs_ineq = [20, 10, 2]
    lhs_eq = [[-1, 5]]
    rhs_eq = [15]
    bnd = [(0, np.inf), (0, np.inf)]

    # opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq, A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd)
    opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq, bounds=bnd)

    print(opt)


def main_pulp():
    # Create the model
    model = LpProblem(name="real_python_example", sense=LpMaximize)

    # Initialize the decision variables
    x = LpVariable(name="x", lowBound=0, cat="Integer")
    y = LpVariable(name="y", lowBound=0)

    # Add the constraints to the model
    model += (2 * x + y <= 20, "red_constraint")
    model += (-4 * x + 5 * y <= 10, "blue_constraint")
    model += (-x + 2 * y >= -2, "yellow_constraint")
    model += (-x + 5 * y == 15, "green_constraint")

    # Add the objective function to the model
    model += lpSum([x, 2 * y])
    # model += x + 2 * y

    status = model.solve()
    # status = model.solve(solver=GLPK(msg=False))

    print(model.status)

    print(LpStatus[model.status])
    print(model.objective.value())
    for var in model.variables():
        print('{}: {}'.format(var.name, var.value()))


if __name__ == '__main__':
    main_pulp()
