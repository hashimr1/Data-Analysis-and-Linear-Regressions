"""CSC110 Fall 2020 Final assignment visualizations
Description
===============================
This Python module contains functions that ....................
Copyright and Usage Information
===============================
This file is provided solely for the final assignment of CSC110 at the University of Toronto
St. George campus. All forms of distribution of this code, whether as given or with any changes,
are expressly prohibited.
This file is Copyright (c) 2020 Raazia Hashim.
"""
from typing import List

import pandas as pd
import plotly.express as px

import data_processing

power_plant_data = data_processing.read_powerplant_file('global_power_plant_database.csv', 'owid-co2-data.csv',
                                                        'countries of the world.csv')
emissions_data = data_processing.read_carbon_emission_file('global_power_plant_database.csv', 'owid-co2-data.csv',
                                                           'countries of the world.csv')
nuclear_data = data_processing.read_nuclear_powerplant('global_power_plant_database.csv', 'owid-co2-data.csv',
                                                       'countries of the world.csv')
nuclear_emissions = data_processing.read_nuclear_powerplant_co2('global_power_plant_database.csv', 'owid-co2-data.csv',
                                                                'countries of the world.csv')
nuclear_position = data_processing.get_longtitude_latitude('global_power_plant_database.csv', 'owid-co2-data.csv',
                                                           'countries of the world.csv')

emissions_capita = [tup[0] for tup in power_plant_data[1]]
non_emissions_capita = [tup[1] for tup in power_plant_data[1]]
total_carbon_emissions = emissions_data[1]

powerplantdf = pd.DataFrame({
    'Emission Power Plants per Capita': emissions_capita,
    'Non-Emission Power Plants per Capita': non_emissions_capita,
    'Carbon Emissions per Capita': total_carbon_emissions,
})

nuclearplantdf = pd.DataFrame({
    'Nuclear Power Plants per Capita': nuclear_data[1],
    'Carbon Emissions per Capita': nuclear_emissions[1]
})


def duplicate_emissions(emission: List[List], countries: List) -> List:
    """Return a list with duplicated carbon emissions corresponding with the countries that go
    with all nuclear power plants.

    >>> new_emissions = duplicate_emissions(nuclear_emissions, nuclear_position[0])
    >>> len(new_emissions) == len(nuclear_position[0])
    True
    """
    emissions_so_far = []
    for country in countries:
        i = emission[0].index(country)
        emissions_so_far.append(emission[1][i])

    return emissions_so_far


mapdf = pd.DataFrame({
    'Countries': nuclear_position[0],
    'Power Plant': nuclear_position[1],
    'Latitudes': nuclear_position[2],
    'Longitudes': nuclear_position[3],
    'Emissions': duplicate_emissions(nuclear_emissions, nuclear_position[0])
})

# Figure 1:
fig = px.scatter_3d(powerplantdf, x='Emission Power Plants per Capita',
                    y='Non-Emission Power Plants per Capita',
                    z='Carbon Emissions per Capita',
                    title='Carbon Emissions and Type of Power Plants per Capita',
                    template='seaborn')
fig.show()
#
# # Figure 2:
fig = px.scatter(powerplantdf, x='Emission Power Plants per Capita',
                 y='Carbon Emissions per Capita',
                 title='Carbon Emissions and Emission Power Plants per Capita',
                 template='seaborn')
fig.show()

# # Figure 3:
fig = px.scatter(powerplantdf, x='Non-Emission Power Plants per Capita',
                 y='Carbon Emissions per Capita',
                 title='Carbon Emissions and Non-Emission Power Plants per Capita',
                 template='seaborn')
fig.show()

# # Figure 4:
fig = px.scatter(nuclearplantdf, x='Nuclear Power Plants per Capita',
                 y='Carbon Emissions per Capita',
                 title='Carbon Emissions and Nuclear Power Plants per Capita',
                 template='seaborn')
fig.show()

# Figure 5: Map
px.set_mapbox_access_token(open(".mapbox_token").read())

fig = px.scatter_mapbox(mapdf, lat='Latitudes', lon='Longitudes',
                        template='seaborn',
                        zoom=1.5,
                        size='Emissions',
                        color='Emissions',
                        color_continuous_scale=px.colors.sequential.Jet,
                        hover_name='Countries',
                        hover_data=['Power Plant'],
                        title='Nuclear Power plants around the World')
fig.show()

# if __name__ == '__main__':
#     import python_ta
#
#     python_ta.check_all(config={
#         'max-line-length': 120,
#         'extra-imports': ['python_ta.contracts', 'pandas', 'plotly.express', 'data_processing'],
#         'disable': ['R1705', 'C0200'],
#     })
#
#     import python_ta.contracts
#     python_ta.contracts.DEBUG_CONTRACTS = False
#     python_ta.contracts.check_all_contracts()
#
#     import doctest
#     doctest.testmod()
