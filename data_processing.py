"""CSC110 Fall 2020 Final assignment data reading and processing

Description
===============================
This Python module contains functions that read data from the powerplant and carbon
emission file and preprocess the data for future computations.

Copyright and Usage Information
===============================
This file is provided solely for the final assignment of CSC110 at the University of Toronto
St. George campus. All forms of distribution of this code, whether as given or with any changes,
are expressly prohibited.

This file is Copyright (c) 2020 Raazia Hashim, Kenneth Miura, Shilin Zhang.
"""
import csv
from typing import List, Set, Dict


def read_powerplant_file(powerplant_filepath: str, carbon_emission_filepath: str,
                         population_filepath: str) -> List[List]:
    """Return the emission and non-emission powerplant per capita of a country.
        The returned value will be a list of two list. The first list represent
        the country name and the second list is a list of tuples that have the number of
        emission powerplant per capita and the number of non-emission powerplnat per capita.
        The first number in each tuple will be the number of emission powerplant per capita
        of a country and the second number in each tuple will be the number of non-emission
        powerplant per capita of a country.

    Preconditions:
        - powerplant_filepath refers to the powerplant csv file
        - carbon_emission_filepath refers to the carbon emission csv file
        - population_filepath refers to the countries of the world csv file

    >>> powerplant = read_powerplant_file('global_power_plant_database.csv', 'owid-co2-data.csv',\
     'countries of the world.csv')
    >>> len(powerplant[0]) == 147
    True
    >>> len(powerplant[1]) == 147
    True

    """
    emission = {'Oil', 'Gas', 'Petcoke', 'Coal', 'Storage', 'Cogeneration'}
    non_emission = {'Hydro', 'Wave and Tidal', 'Nuclear', 'Biomass',
                    'Solar', 'Geothermal', 'Wind', 'Waste'}
    powerplant = read_powerplant_data(powerplant_filepath)
    data_so_far = {'country': powerplant['country'], 'type': powerplant['type']}
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

    common = common_country(powerplant_filepath, carbon_emission_filepath, population_filepath)
    new_data = [[], [], []]
    for k in range(0, len(data[0])):
        if data[0][k] in common:
            list.append(new_data[0], data[0][k])
            list.append(new_data[1], data[1][k])
            list.append(new_data[2], data[2][k])

    population = read_pop_data(population_filepath)
    pop = [[], []]
    for x in range(0, len(population['country'])):
        if population['country'][x] in common:
            pop[0].append(population['country'][x])
            pop[1].append(population['population'][x])

    actual_data = [[], []]
    for x in range(0, len(pop[0])):
        list.append(actual_data[0], pop[0][x])
        list.append(actual_data[1], (new_data[1][x] / pop[1][x], new_data[2][x] / pop[1][x]))

    return actual_data


def read_carbon_emission_file(powerplant_filepath: str, carbon_emission_filepath: str,
                              population_filepath: str) -> List[List]:
    """Return the carbon emission per capita in 2017 among all the country
       in the powerplant dataset and
       population dataset. The returned value will be a list of two lists.
       The first list is the country name and
       the second list is the carbon emission per capita of the country in 2017

    Preconditions:
        - powerplant_filepath refers to the powerplant csv file
        - carbon_emission_filepath refers to the carbon emission csv file
        - population_filepath refers to the population csv file

    >>> carbon = read_carbon_emission_file('global_power_plant_database.csv', 'owid-co2-data.csv',\
     'countries of the world.csv')
    >>> len(carbon[0]) == 147
    True
    >>> len(carbon[1]) == 147
    True

    """
    country = common_country(powerplant_filepath, carbon_emission_filepath, population_filepath)
    population = read_pop_data(population_filepath)
    co2 = read_co2_data(carbon_emission_filepath)
    data_so_far = [[], []]
    for x in range(0, len(co2['country'])):
        if co2['country'][x] in country:
            data_so_far[0].append(co2['country'][x])
            index = population['country'].index(co2['country'][x])
            data_so_far[1].append(co2['co2'][x] / population['population'][index])

    return data_so_far


def read_nuclear_powerplant(powerplant_filepath: str, carbon_emission_filepath: str,
                            population_filepath: str) -> List[List]:
    """Return the country name and the number of nuclear powerplant per capita in a country.
    If the country has no nuclear powerplant, it is not included in the output

    Precondition:
        - the powerplant_filepath refers to the powerplant csv file
        - the carbon_emission_filepath refers to the carbon emission csv file
        - the population_filepath refers to the populatioin csv file

    >>> nuclear = read_nuclear_powerplant('global_power_plant_database.csv', 'owid-co2-data.csv', \
    'countries of the world.csv')
    >>> len(nuclear[0]) == 30
    True

    """
    country = common_country(powerplant_filepath, carbon_emission_filepath, population_filepath)
    nuclear = [[], []]
    powerplant = read_powerplant_data(powerplant_filepath)
    data_so_far = {'country': powerplant['country'], 'type': powerplant['type']}
    for x in range(0, len(data_so_far['country'])):
        if data_so_far['type'][x] == 'Nuclear':
            if data_so_far['country'][x] in nuclear[0]:
                nuclear[1][-1] = nuclear[1][-1] + 1
            else:
                list.append(nuclear[0], data_so_far['country'][x])
                list.append(nuclear[1], 1)

    nuclear_power = [[], []]
    for x in range(0, len(nuclear[0])):
        if nuclear[0][x] in country:
            nuclear_power[0].append(nuclear[0][x])
            nuclear_power[1].append(nuclear[1][x])

    population = read_pop_data(population_filepath)
    pop = [[], []]
    for x in range(0, len(population['country'])):
        if population['country'][x] in nuclear[0]:
            pop[0].append(population['country'][x])
            pop[1].append(population['population'][x])

    actual_data = [[], []]
    for x in range(0, len(nuclear_power[0])):
        list.append(actual_data[0], pop[0][x])
        list.append(actual_data[1], nuclear_power[1][x] / pop[1][x])

    return actual_data


def read_nuclear_powerplant_co2(powerplant_filepath: str, carbon_emission_filepath: str,
                                population_filepath: str) -> List[List]:
    """Return the carbon emission per capita for countries that have at
     least one nuclear powerplant and that
     is in both the carbon emission dataset and the population dataset
     The returned value will be a list of two lists. The first list is the country name
     and the second list is the carbon emission per capita in 2017 that correspond to the country

     Precondition:
        - powerplant_filepath refers to the powerplant csv file
        - carbon_emission_filepaht refers to the carbon emission csv file
        - population_filepath refers to the population csv file

    >>> nuclear_co2 = read_nuclear_powerplant_co2('global_power_plant_database.csv', 'owid-co2-data.csv',\
     'countries of the world.csv')
    >>> len(nuclear_co2[0]) == 30
    True
    """
    nuclear = read_nuclear_powerplant(powerplant_filepath, carbon_emission_filepath,
                                      population_filepath)
    co2 = read_co2_data(carbon_emission_filepath)
    population = read_pop_data(population_filepath)
    nuclear_co2 = [[], []]
    for x in range(0, len(nuclear[0])):
        nuclear_co2[0].append(nuclear[0][x])
        nuclear_co2[1].append(co2['co2'][co2['country'].index(nuclear[0][x])]
                              / population['population']
                              [population['country'].index(nuclear[0][x])])

    return nuclear_co2


def get_longtitude_latitude(powerplant_filepath: str, carbon_emission_filepath: str,
                            population_filepath: str) -> List[List]:
    """Return the country, name of the powerplant, longtitude and latitude of
    each nuclear powerplant in the 30 countries that are in all three data sets.
    The return value will be a list of four lists. The first list is the country name.
    The second list is the name of the powerplant.
    The third list is the latitude of the nuclear powerplants.
    The fourth list is the longitude of the nuclear powerplants.

    Precondition:
        - powerplant_filepath refers to the powerplant csv file
        - carbon_emission_filepaht refers to the carbon emission csv file
        - population_filepath refers to the population csv file

    >>> nuclear_longtitude_latitude = get_longtitude_latitude('global_power_plant_database.csv', 'owid-co2-data.csv'\
    , 'countries of the world.csv')
    >>> len(nuclear_longtitude_latitude[0]) == 192
    True
    """
    powerplant = read_powerplant_data('global_power_plant_database.csv')
    country = read_nuclear_powerplant(powerplant_filepath, carbon_emission_filepath,
                                      population_filepath)[0]
    nuclear = [[], [], [], []]
    for x in range(0, len(powerplant['country'])):
        if powerplant['country'][x] in country and powerplant['type'][x] == 'Nuclear':
            nuclear[0].append(powerplant['country'][x])
            nuclear[1].append(powerplant['name'][x])
            nuclear[2].append(powerplant['longtitude'][x])
            nuclear[3].append(powerplant['latitude'][x])

    return nuclear


def common_country(powerplant_filepath: str, carbon_emission_filepath: str,
                   population_filepath: str) -> Set:
    """Return the name of all countries in both the powerplant dataset, population dataset
       and the carbon emission dataset with a carbon emission avaliable in 2017.

    Preconditions:
        - powerplant_filepath refers to the powerplant csv file
        - carbon_emission_filepath refers to the carbon emission csv file
        - population_filepath refers to the population csv file

    >>> common = common_country('global_power_plant_database.csv', 'owid-co2-data.csv', 'countries of the world.csv')
    >>> len(common) == 147
    True

    """
    powerplant = read_powerplant_data(powerplant_filepath)
    co2 = read_co2_data(carbon_emission_filepath)
    population = read_pop_data(population_filepath)
    powerplant_country = set(powerplant['country'])
    co2_country = set(co2['country'])
    population_country = set(population['country'])
    common = powerplant_country.intersection(co2_country, population_country)
    return common


def read_powerplant_data(powerplant_filepath: str) -> Dict:
    """Return the data from the powerplant data set we need for the project as a
     dictionary of the name of the variable and the value for each powerplant
     as a list

    Precondition:
        - powerplant_filepath refers to the powerplant csv file

    >>> powerplant = read_powerplant_data('global_power_plant_database.csv')
    >>> len(powerplant['country']) == 29910
    True
    """
    with open(powerplant_filepath, encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        data_so_far = {'country': [], 'name': [], 'type': [], 'longtitude': [], 'latitude': []}
        for row in reader:
            if row[1] == 'United States of America':
                list.append(data_so_far['country'], 'United States')
                list.append(data_so_far['name'], row[2])
                list.append(data_so_far['type'], row[7])
                list.append(data_so_far['longtitude'], float(row[5]))
                list.append(data_so_far['latitude'], float(row[6]))
            else:
                list.append(data_so_far['country'], row[1])
                list.append(data_so_far['name'], row[2])
                list.append(data_so_far['type'], row[7])
                list.append(data_so_far['longtitude'], float(row[5]))
                list.append(data_so_far['latitude'], float(row[6]))

        return data_so_far


def read_co2_data(carbon_emission_filepath: str) -> Dict:
    """Return the country name and carbon emission for all countries
    that have a carbon emission value in 2017.

    Precondition:
        - carbon_emission_filepath refers to the carbon emission csv file

    >>> co2 = read_co2_data('owid-co2-data.csv')
    >>> len(co2['country']) == 233
    True
    """
    with open(carbon_emission_filepath, encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        data_so_far = {'country': [], 'co2': []}
        for row in reader:
            if row[2] == "2017":
                data_so_far['country'].append(row[1])
                data_so_far['co2'].append(float(row[3]))

        return data_so_far


def read_pop_data(population_filepath: str) -> Dict:
    """Return the country name and the population for all countries in the population dataset

    Precondition:
        - population_filepath refers to the population data set

    >>> population = read_pop_data('countries of the world.csv')
    >>> len(population['country']) == 227
    True
    """
    with open(population_filepath, encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        data_so_far = {'country': [], 'population': []}
        for row in reader:
            data_so_far['country'].append(row[0][:-1])
            data_so_far['population'].append(int(row[2]))

        return data_so_far


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['python_ta.contracts', 'csv', 'List', 'Set', 'Dict'],
        'disable': ['R1705', 'C0200'],
        'allowed-io': ['common_country', 'read_carbon_emission_file', 'read_powerplant_file',
                       'read_pop_data', 'read_co2_data', 'read_powerplant_data',
                       'get_longtitude_latitude', 'read_nuclear_powerplant_co2',
                       'read_nuclear_powerplant']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()
