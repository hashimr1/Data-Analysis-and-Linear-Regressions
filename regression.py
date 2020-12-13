"""CSC110 Fall 2020 Final assignment Multiple Variable Linear Regression

Provides an implementation of Multiple Variable Linear Regression, as well as a test case


Copyright and Usage Information
===============================
This file is provided solely for the final assignment of CSC110 at the University of Toronto
St. George campus. All forms of distribution of this code, whether as given or with any changes,
are expressly prohibited.

This file is Copyright (c) 2020 Kenneth Miura.
"""
import math
import numpy as np
from sklearn.linear_model import LinearRegression
import data_processing

def ols_linear_regression(x: np.array, y: np.array) -> np.array:
    """Return a numpy array of coefficients and intercept that best predict y.

    n is the number of independent variables (x.shape[1]). b is the intercept.
    The returned numpy array is in the form [x_1, x_2, ..., x_n, b]
    Preconditions:
        - x.size != 0
        - y.size != 0
        - len(x.shape) == 2
        - len(y.shape) == 2
        - x.shape[0] > 1
        - y.shape[0] > 1
    """
    num_of_data_points = x.shape[0]
    # Adding a coefficient of 1 to allow for the offset
    x = np.append(x, np.ones((num_of_data_points, 1)), axis=1)
    y = np.array(y).astype(np.float64).reshape((-1, 1))
    # equation based off:
    # http://mezeylab.cb.bscb.cornell.edu/labmembers/documents/supplement%205%20-ob%20multiple%20regression.pdf
    # also got idea of adding a column of 1s for offset, although put it on other side
    # to match order of sklearn output for easier testing
    # Using http: pillowlab.princeton.edu/teaching/statneuro2018/slides/notes03b_LeastSquaresRegression.pdf
    # to show derivatives of x
    params = np.dot(np.linalg.inv(np.dot(x.T, x)), np.dot(x.T, y))
    return params


def test_emissions_and_nonemissions_regression() -> None:
    """Test that ols_linear_regression method's regression is similarly or more accurate to the
    sklearn LinearRegression class's regression on data with IV: emission and non-emission
    powerplants per capita and DV: Carbon Emissions per capita
    """
    _, proportions = data_processing.read_powerplant_file('global_power_plant_database.csv', 'owid-co2-data.csv',
                                                          'countries of the world.csv')
    _, emissions = data_processing.read_carbon_emission_file('global_power_plant_database.csv', 'owid-co2-data.csv',
                                                             'countries of the world.csv')
    np_proportions = np.array(proportions)
    np_emissions = np.array(emissions).reshape((-1, 1))
    assert similar_to_sklearn(np_proportions, np_emissions)


def test_nuclear_regression() -> None:
    """Test that ols_linear_regression's regression is similarly or moreaccurate to the sklearn LinearRegression
    class's regression on data with IV: Nuclear powerplants per Capita and DV: Carbon Emissions per capita
    """
    _, nuclear_powerplants = data_processing.read_nuclear_powerplant('global_power_plant_database.csv',
                                                                     'owid-co2-data.csv',
                                                                     'countries of the world.csv')
    _, nuclear_emissions = data_processing.read_nuclear_powerplant_co2('global_power_plant_database.csv',
                                                                       'owid-co2-data.csv',
                                                                       'countries of the world.csv')
    np_nuclear = np.array(nuclear_powerplants).reshape(-1, 1)
    np_nuclear_emissions = np.array(nuclear_emissions).reshape(-1, 1)

    assert similar_to_sklearn(np_nuclear, np_nuclear_emissions)


def test_emissions_only_data() -> None:
    """Test that ols_linear_regression's regression is similarly or more accurate to the sklearn LinearRegression
    class's regression on data with IV: Emissions powerplants per Capita and DV: Carbon Emissions per Capita
    """
    # NOTE: the sklearn methods want np array in form (index of the datapoint, variable), which they are in right now
    _, proportions = data_processing.read_powerplant_file('global_power_plant_database.csv',
                                                          'owid-co2-data.csv',
                                                          'countries of the world.csv')
    _, emissions = data_processing.read_carbon_emission_file('global_power_plant_database.csv',
                                                             'owid-co2-data.csv',
                                                             'countries of the world.csv')
    np_proportions = np.array(proportions)[:, 0].reshape((-1, 1))
    np_emissions = np.array(emissions).reshape((-1, 1))

    assert similar_to_sklearn(np_proportions, np_emissions)


def test_non_emission_only_data() -> None:
    """Test that ols_linear_regression's regression is similarly or more accurate to the sklearn LinearRegression
    class's regression on data with IV: Non-Emission powerplants per Capita and DV: Carbon Emissions per Capita
    """
    _, proportions = data_processing.read_powerplant_file('global_power_plant_database.csv',
                                                          'owid-co2-data.csv',
                                                          'countries of the world.csv')
    _, emissions = data_processing.read_carbon_emission_file('global_power_plant_database.csv',
                                                             'owid-co2-data.csv',
                                                             'countries of the world.csv')
    np_proportions = np.array(proportions)[:, 1].reshape((-1, 1))
    np_emissions = np.array(emissions).reshape((-1, 1))

    assert similar_to_sklearn(np_proportions, np_emissions)


def similar_to_sklearn(x: np.array, y: np.array) -> bool:
    """Return whether ols_linear_regression's regression is similarly or more accurate than the sklearn LinearRegression
    class's regression on data with IV: x, and DV: y

    Based off
    https://scikit-learn.org/stable/auto_examples/linear_model/plot_ols_3d.html#sphx-glr-auto-examples-linear-model-plot-ols-3d-py (CITE THIS LATER!)
    https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html#sklearn.linear_model.LinearRegression
    Preconditions:
        - x.size != 0
        - y.size != 0
        - len(x.shape) == 2
        - len(y.shape) == 2
        - x.shape[0] > 1
        - y.shape[0] > 1
    """
    train_index = math.floor(len(x) * 0.8)

    x_train = x[:train_index, :]
    x_test = x[train_index:, :]
    y_train = y[:train_index, :]
    y_test = y[train_index:, :]

    # SK LEARN
    sklearn_reg = LinearRegression().fit(x_train, y_train)
    sklearn_test_error_average = np.average(sklearn_reg.predict(x_test) - y_test)

    # ols
    ols_reg = ols_linear_regression(x_train, y_train)
    np_coeffs = np.array(ols_reg)[:-1]
    offset = ols_reg[-1]
    print(f'coeffs: {np_coeffs}, offset: {offset}')
    prediction = np.dot(x_test, np_coeffs) + offset
    ols_test_error_average = np.average(prediction - y_test)

    tolerance = 0.5
    # Less than because it's fine/good for the ols implementation to have less error than the sklearn version
    return abs(ols_test_error_average) - abs(sklearn_test_error_average) < tolerance


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['python_ta.contracts', 'numpy', 'data_processing', 'math', 'sklearn.linear_model'],
        'disable': ['R1705', 'W1114']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
    import pytest

    pytest.main(['regression.py'])
