"""CSC110 Fall 2020 Final assignment data reading and processing

Description
===============================

This Python module contains functions that read data from the powerplant and carbon
emission file and preprocess the data for our future computations which is creating a
multiple variable linear regression to predict carbon emission with proportion of
emission and non-emission powerplant.

Copyright and Usage Information
===============================

This file is provided solely for the final assignment of CSC110 at the University of Toronto
St. George campus. All forms of distribution of this code, whether as given or with any changes,
are expressly prohibited.

This file is Copyright (c) 2020 Shilin Zhang.
"""
import csv
from typing import List, Set


def read_powerplant_file(powerplant_filepath: str, carbon_emission_filepath: str) -> List[List]:
    """ return the proportion of emission and non-emission powerplants in a country.
        The returned value will be a list of two list. The first list represent
        the country name and the second list is a list of tuples that have the
        proportion of emission and non-emission powerplant. The first number in
        each tuple will be the proportion of emission powerplant in a country
        and the second number in each tuple will be the proportion of non-emission
        powerplant in a country.

    Preconditions:
        - powerplant_filepath refers to the powerplant csv file
        - carbon_emission_filepath refers to the carbon emission csv file

    >>> powerplant = read_powerplant_file('global_power_plant_database.csv', 'owid-co2-data.csv')
    >>> len(powerplant[0]) == 156
    True
    >>> len(powerplant[1]) == 156
    True

    """
    emission = {'Oil', 'Gas', 'Petcoke', 'Coal', 'Storage', 'Cogeneration'}
    non_emission = {'Hydro', 'Wave and Tidal', 'Nuclear', 'Biomass',
                    'Solar', 'Geothermal', 'Wind', 'Waste'}
    with open(powerplant_filepath) as file:
        reader = csv.reader(file)
        next(reader)
        data_so_far = {'country': [], 'type': []}
        for row in reader:
            list.append(data_so_far['country'], row[1])
            list.append(data_so_far['type'], row[7])

    data = [[], [], []]
    for x in range(0, len(data_so_far['country'])):
        if data_so_far['country'][x] in data[0]:
            if data_so_far['type'][x] in emission:
                data[1][-1] = data[1][-1] + 1
            elif data_so_far['type'][x] in non_emission:
                data[2][-1] = data[2][-1] + 1

        else:
            list.append(data[0], data_so_far['country'][x])
            if data_so_far['type'][x] in emission:
                list.append(data[1], 1)
                list.append(data[2], 0)
            else:
                list.append(data[1], 0)
                list.append(data[2], 1)

    country = common_country(powerplant_filepath, carbon_emission_filepath)
    prop_data = [[], [], []]
    for k in range(0, len(data[0])):
        if data[0][k] in country:
            list.append(prop_data[0], data[0][k])
            list.append(prop_data[1], data[1][k] / (data[1][k] + data[2][k]))
            list.append(prop_data[2], data[2][k] / (data[1][k] + data[2][k]))

    actual_data = [[], []]
    for k in range(0, len(prop_data[0])):
        list.append(actual_data[0], prop_data[0][k])
        list.append(actual_data[1], (prop_data[1][k], prop_data[2][k]))

    return actual_data


def read_carbon_emission_file(powerplant_filepath: str, carbon_emission_filepath: str)\
        -> List[List]:
    """Return the carbon emission in 2018 among all the country in the powerplant dataset
       The returned value will be a list of two lists. The first list is the country name and
       the second list is the carbon emission of the country in 2018

    Preconditions:
        - powerplant_filepath refers to the powerplant csv file
        - carbon_emission_filepath refers to the carbon emission csv file

    >>> carbon = read_carbon_emission_file('global_power_plant_database.csv', 'owid-co2-data.csv')
    >>> len(carbon[0]) == 156
    True
    >>> len(carbon[1]) == 156
    True

    """
    country = common_country(powerplant_filepath, carbon_emission_filepath)
    with open(carbon_emission_filepath) as file:
        reader = csv.reader(file)
        next(reader)
        data_so_far = [[], []]
        for row in reader:
            if row[1] in country:
                if row[2] == "2018":
                    list.append(data_so_far[0], row[1])
                    list.append(data_so_far[1], row[3])

        return data_so_far


def common_country(powerplant_filepath: str, carbon_emission_filepath: str) -> Set:
    """Return the name of all countries in both the powerplant dataset and the carbon
       emission dataset with a carbon emission avaliable in 2018.

    Preconditions:
        - powerplant_filepath refers to the powerplant csv file
        - carbon_emission_filepath refers to the carbon emission csv file

    >>> common = common_country('global_power_plant_database.csv', 'owid-co2-data.csv')
    >>> len(common) == 156
    True

    """
    powerplant_country = set()
    co_country = set()
    with open(powerplant_filepath) as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            powerplant_country.add(row[1])

    with open(carbon_emission_filepath) as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[2] == "2018":
                co_country.add(row[1])

    all_country = powerplant_country.union(co_country)
    return {k for k in all_country if k in powerplant_country and k in co_country}


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['python_ta.contracts', 'csv', 'List', 'Set'],
        'disable': ['R1705', 'C0200'],
        'allowed-io': ['common_country', 'read_carbon_emission_file', 'read_powerplant_file']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()
