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
This file is Copyright (c) 2020 Raazia Hashim.
"""

import pandas as pd
import plotly.express as px

import data_processing


power_plant_data = data_processing.read_powerplant_file('global_power_plant_database.csv',
                                                        'owid-co2-data.csv')
emissions_data = data_processing.read_carbon_emission_file('global_power_plant_database.csv',
                                                           'owid-co2-data.csv')

prop_emissions = [tup[0] for tup in power_plant_data[1]]
prop_non_emissions = [tup[1] for tup in power_plant_data[1]]
total_carbon_emissions = emissions_data[1]


df = pd.DataFrame({
    'Proportion of Emission Power Plants': prop_emissions,
    'Proportion of non-Emission Power Plants': prop_non_emissions,
    'Carbon Emissions': total_carbon_emissions
})

# Version 1:
fig = px.scatter_3d(df, x='Proportion of Emission Power Plants',
                    y='Proportion of non-Emission Power Plants',
                    z='Carbon Emissions',
                    title='Carbon Emissions and Type of Power Plants in a Country',
                    template='ggplot2',
                    height=700,)
fig.show()


# if __name__ == '__main__':
#     import python_ta
#
#     python_ta.check_all(config={
#         'max-line-length': 100,
#         'extra-imports': ['python_ta.contracts', 'csv', 'List', 'Set'],
#         'disable': ['R1705', 'C0200'],
#         'allowed-io': ['common_country', 'read_carbon_emission_file', 'read_powerplant_file']
#     })
#
#     import python_ta.contracts
#
#     python_ta.contracts.DEBUG_CONTRACTS = False
#     python_ta.contracts.check_all_contracts()
#
#     import doctest
