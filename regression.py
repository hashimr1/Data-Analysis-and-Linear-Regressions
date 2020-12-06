''' Multiple Variable Linear Regression

Provides an implementation of Multiple Variable Linear Regression, as well as a test case


Copyright and Usage Information
===============================
TODO: Figure out how we're supposed to claim copyright.
TODO: If it's just what I did, make sure to add everyones names to it.

This file is Copyright (c) 2020 Kenneth Miura
'''
from typing import List, Tuple
import numpy as np
from matplotlib import pyplot as plt
import data_processing
from sklearn.linear_model import LinearRegression

''' The returned value will be a list of two list. The first list represent
        the country name and the second list is a list of tuples that have the
        proportion of emission and non-emission powerplant. The first number in
        each tuple will be the proportion of emission powerplant in a country
        and the second number in each tuple will be the proportion of non-emission
        powerplant in a country.
'''


def show_error():
    # THIS IS GROSS
    plt.show()


def linear_regression(independent_vars: List[Tuple], dependent_var: List, num_of_iterations: int,
                      learning_rate: float) -> List[float]:
    '''Return a list of coefficients for independent_vars that best predict dependent_var.


    Let n be the length of the tuples inside independent_vars.
    The returned list of coefficients will be in the form (x_1,x_2, ... , x_n , b),
    where x_1 is the weight for the 1st independent variable. b is an offset.

    Preconditions:
        - data != []
        - all the nested lists are the same size

    '''
    # NOTE: This is debugging stuff
    error_over_time = []
    # TODO:
    X = np.array(independent_vars)
    num_of_data_points = X.shape[0]
    # Adding a coefficient of 1 to allow for the offset
    X = np.append(X, np.ones((num_of_data_points, 1)), axis=1)
    Y = np.array(dependent_var).astype(np.float64).reshape((num_of_data_points, 1))
    params = np.ones((X.shape[1], 1))

    for i in range(num_of_iterations):
        #
        prediction = np.dot(X, params)
        error = (Y - prediction)
        mean_squared_error = (np.dot(error.T, error)) / num_of_data_points

        error_over_time.append(np.asscalar(mean_squared_error))
        # This gradient calculation is incorrect, the gradient for the first variable is positive
        # Try this one: https://mccormickml.com/2014/03/04/gradient-descent-derivation/
        gradient = (np.dot(X.T, prediction) - np.dot(X.T, Y)) * 2 / num_of_data_points
        params = params - learning_rate * gradient
    # NOTE:This is kinda gross code
    # plt.plot(error_over_time)
    print(f'Final error: {error_over_time[-2]}')

    return params


def test_linear_regression() -> None:
    '''


    Based off https://scikit-learn.org/stable/auto_examples/linear_model/plot_ols_3d.html#sphx-glr-auto-examples-linear-model-plot-ols-3d-py (CITE THIS LATER!)
    and
    https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html#sklearn.linear_model.LinearRegression
    '''

    # NOTE: the sklearn methods want np array in form (index of the datapoint, variable), which they are rn
    names, proportions = data_processing.read_powerplant_file('global_power_plant_database.csv', 'owid-co2-data.csv')
    _, emissions = data_processing.read_carbon_emission_file('global_power_plant_database.csv', 'owid-co2-data.csv')
    reg = LinearRegression().fit(proportions, emissions)
    print(f'coeff: {reg.coef_}, intercept: {reg.intercept_}')
    # If you train on the whole set,
    # [-37.0178922  37.0178922], intercept: 189.93495820316974
    # This makes sense, since the first variable is the emissions, and the second is non-emission
    pass


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
