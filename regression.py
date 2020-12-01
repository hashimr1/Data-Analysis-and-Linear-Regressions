''' Multiple Variable Linear Regression

Provides an implementation of Multiple Variable Linear Regression, as well as a test case


Copyright and Usage Information
===============================
TODO: Figure out how we're supposed to claim copyright.
TODO: If it's just what I did, make sure to add everyones names to it.

This file is Copyright (c) 2020 Kenneth Miura
'''
from typing import List


def linear_regression(data: List[List[float]], learning_rate: float) -> List[float]:
    '''Return a list of coefficients for a fitted function to data.

    The last element of the nested list is assumed to be the dependent variable.
    All earlier elements are assumed to be the corresponding independent variables.

    Let n be the number of independent variables in data.
    The returned list of coefficients will be in the form (x_1,x_2, ... , x_n , b),
    where x_1 is the weight for the 1st independent variable. b is an offset.

    Preconditions:
        - data != []
        - all the nested lists are the same size

    '''

    # TODO:
    # Use numpy for matrix multiplications
    # Use MSE to calculate error
    # Use simplest gradient descent alg to minimize cost
    # If there's issues with performance, do batches
    # If there's issues with optimizing badly, look up a better grad desc alg
    pass


def test_linear_regression() -> None:
    '''


    Based off https://scikit-learn.org/stable/auto_examples/linear_model/plot_ols_3d.html#sphx-glr-auto-examples-linear-model-plot-ols-3d-py (CITE THIS LATER!)
    '''


if __name__ == '__main__':
    # TODO: Customize PyTA args for this file
    # import python_ta
    #
    # python_ta.check_all(config={
    #     'max-line-length': 100,
    #     'extra-imports': ['math', 'python_ta.contracts', 'hypothesis.strategies'],
    #     'disable': ['R1705', 'W1114']
    # })
    #
    # import python_ta.contracts
    #
    # python_ta.contracts.DEBUG_CONTRACTS = False
    # python_ta.contracts.check_all_contracts()
    import pytest

    pytest.main(['regression.py'])
