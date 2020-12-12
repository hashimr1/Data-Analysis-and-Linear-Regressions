"""CSC110 Fall 2020 Final Assignment Visualizations

Description
===============================
This Python module contains functions that visualize power plant and carbon emissions data.

Resources:
https://plotly.com/python/scattermapbox/
https://plotly.com/python/line-and-scatter/
https://plotly.com/python/3d-scatter-plots/
https://plotly.com/python/ml-regression/

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
import plotly.graph_objects as go

import data_processing
import regression


################################################################################
# Create Data Frames
################################################################################
def power_plant_df() -> pd.DataFrame:
    """Create and return a data frame containing information about power plants and carbon
    emissions for countries around the world.
    Columns:
        'Countries': names of all countries we have information for
        'Emission Power Plants per Capita': number of emission power plants in a country divided by population
        'Non-Emission Power Plants per Capita': number of emission power plants in a country divided by population
        'Carbon Emissions per Capita': total carbon emissions divided by the population
    """
    power_plant_data = data_processing.read_powerplant_file('global_power_plant_database.csv', 'owid-co2-data.csv',
                                                            'countries of the world.csv')
    emissions_data = data_processing.read_carbon_emission_file('global_power_plant_database.csv', 'owid-co2-data.csv',
                                                               'countries of the world.csv')

    return pd.DataFrame({
        'Countries': power_plant_data[0],
        'Emission Power Plants per Capita': [tup[0] for tup in power_plant_data[1]],
        'Non-Emission Power Plants per Capita': [tup[1] for tup in power_plant_data[1]],
        'Carbon Emissions per Capita': emissions_data[1]
    })


def nuclear_emissions_df() -> pd.DataFrame:
    """Create and return a data frame containing information about nuclear power plants per capita and carbon
    emissions for countries that have at least one nuclear power plant.
    Columns:
        'Countries': names of all countries that have at least one nuclear power plant
        'Nuclear Power Plants per Capita': number of nuclear power plants in a country divided by population
        'Carbon Emissions per Capita': total carbon emissions divided by the population
    """
    nuclear_data = data_processing.read_nuclear_powerplant('global_power_plant_database.csv', 'owid-co2-data.csv',
                                                           'countries of the world.csv')
    emission_data = data_processing.read_nuclear_powerplant_co2('global_power_plant_database.csv', 'owid-co2-data.csv',
                                                                'countries of the world.csv')

    return pd.DataFrame({
        'Countries': nuclear_data[0],
        'Nuclear Power Plants per Capita': nuclear_data[1],
        'Carbon Emissions per Capita': emission_data[1]
    })


def nuclear_locations_df() -> pd.DataFrame:
    """Create and return a data frame containing information about nuclear power plants, carbon
    emissions and their locations as an input to a map visualization.
    Columns:
        'Countries': names of countries corresponding to the plant
        'Power Plant': power plant name
        'Latitudes': latitudes for the power plant
        'Longitudes': longitudes for the power plant
        'Emissions': total carbon emissions per capita for that country
    """
    emissions_data = data_processing.read_nuclear_powerplant_co2('global_power_plant_database.csv',
                                                                 'owid-co2-data.csv', 'countries of the world.csv')
    position_data = data_processing.get_longtitude_latitude('global_power_plant_database.csv',
                                                            'owid-co2-data.csv', 'countries of the world.csv')

    return pd.DataFrame({
        'Countries': position_data[0],
        'Power Plant': position_data[1],
        'Latitudes': position_data[2],
        'Longitudes': position_data[3],
        'Emissions': duplicate_emissions(emissions_data, position_data[0])
    })


################################################################################
# Scatter Plot Map
################################################################################
def nuclear_position_map() -> None:
    """Plot positions of nuclear power plants on the world map,
    using mapbox and plotly.express.
    Each point that is plotted on the map represents a nuclear power plant. The size and color of the point
    depend on the country's carbon emissions per capita.

    Documentation available at https://plotly.com/python/scattermapbox/
    """
    px.set_mapbox_access_token(open(".mapbox_token").read())

    mapdf = nuclear_locations_df()

    fig = px.scatter_mapbox(mapdf, lat='Latitudes', lon='Longitudes',
                            template='seaborn',
                            zoom=1.5,
                            size='Emissions',
                            color='Emissions',
                            color_continuous_scale='jet',
                            # px.colors.sequential.Jet
                            hover_name='Countries',
                            hover_data=['Power Plant'],
                            title='Nuclear Power plants around the World')
    fig.show()


################################################################################
# Scatter Plots and Linear Regressions
################################################################################
def nuclear_emissions_plot(our_slope, our_intercept) -> None:
    """Plot nuclear emissions per capita and carbon emissions per capita on a scatter plot.
    Then add a linear regression, using regression fit in regression.py.
    Each point that is plotted represents a country. The size of the point
    depend on the country's carbon emissions per capita.

    Documentation available at https://plotly.com/python/line-and-scatter/
    """
    nuclearplantdf = nuclear_emissions_df()
    max_x_val = nuclearplantdf['Nuclear Power Plants per Capita'].max() * 1.2
    # min_x_val is close to 0, so its more intuitive to start the graph at 0
    min_x_val = 0

    print(f'min {min_x_val}')
    print(f'max: {max_x_val}')
    fig = px.scatter(nuclearplantdf, x='Nuclear Power Plants per Capita',
                     y='Carbon Emissions per Capita',
                     color='Countries',
                     size='Carbon Emissions per Capita',
                     title='Carbon Emissions and Nuclear Power Plants per Capita',
                     template='ggplot2')

    # line of best fit using our linear regression
    # ORIGINAL coeff & intercept
    # our_slope = 2.15e-10
    # our_intercept = 7.4e-6
    our_y1 = calculate_coeff(min_x_val, our_slope, our_intercept)
    our_y2 = calculate_coeff(max_x_val, our_slope, our_intercept)
    fig.add_trace(go.Scatter(x=[min_x_val, max_x_val], y=[our_y1, our_y2], mode="lines",
                             line=go.scatter.Line(color=px.colors.qualitative.Pastel[0]), name="our line"))

    # line of best fit using sklearn's multiple linear regression
    sk_slope = 0.809
    sk_intercept = 7.29e-6
    sk_y1 = calculate_coeff(min_x_val, sk_slope, sk_intercept)
    sk_y2 = calculate_coeff(max_x_val, sk_slope, sk_intercept)
    fig.add_trace(go.Scatter(x=[min_x_val, max_x_val], y=[sk_y1, sk_y2], mode="lines",
                             line=go.scatter.Line(color=px.colors.qualitative.Pastel[5]), name="sk line"))

    fig.show()


def emissions_power_plants_plot(our_slope, our_intercept) -> None:
    """Plot emissions power plants per capita and carbon emissions per capita on a scatter plot.
    Then add a linear regression, using regression fit in regression.py.
    Each point that is plotted represents a country.

    Documentation available at https://plotly.com/python/line-and-scatter/
    """
    powerplantdf = power_plant_df()

    fig = px.scatter(powerplantdf, x='Emission Power Plants per Capita',
                     y='Carbon Emissions per Capita',
                     title='Carbon Emissions and Emission Power Plants per Capita',
                     template='ggplot2')
    max_x_val = powerplantdf['Emission Power Plants per Capita'].max() * 1.2
    # min_x_val is close to 0, so its more intuitive to start the graph at 0
    min_x_val = 0
    # line of best fit using our linear regression
    # ORIGINAL VALS:
    # our_slope = 3.65e-6
    # our_intercept = 6.55e-6
    our_y1 = calculate_coeff(min_x_val, our_slope, our_intercept)
    our_y2 = calculate_coeff(max_x_val, our_slope, our_intercept)
    fig.add_trace(go.Scatter(x=[min_x_val, max_x_val], y=[our_y1, our_y2], mode="lines",
                             line=go.scatter.Line(color=px.colors.qualitative.Pastel[0]), name="our line"))

    # line of best fit using sklearn's multiple linear regression
    sk_slope = 4.03
    sk_intercept = -3.59e-7
    sk_y1 = calculate_coeff(min_x_val, sk_slope, sk_intercept)
    sk_y2 = calculate_coeff(max_x_val, sk_slope, sk_intercept)
    fig.add_trace(go.Scatter(x=[min_x_val, max_x_val], y=[sk_y1, sk_y2], mode="lines",
                             line=go.scatter.Line(color=px.colors.qualitative.Pastel[5]), name="sk line"))

    fig.show()


def non_emissions_power_plants_plot(our_slope, our_intercept) -> None:
    """Plot non-emissions power plants per capita and carbon emissions per capita on a scatter plot.
    Then add a linear regression, using regression fit in regression.py.
    Each point that is plotted represents a country.

    Documentation available at https://plotly.com/python/line-and-scatter/
    """
    powerplantdf = power_plant_df()

    fig = px.scatter(powerplantdf, x='Non-Emission Power Plants per Capita',
                     y='Carbon Emissions per Capita',
                     title='Carbon Emissions and Non-Emission Power Plants per Capita',
                     template='ggplot2')
    max_x_val = powerplantdf['Non-Emission Power Plants per Capita'].max() * 1.2
    # min_x_val is close to 0, so its more intuitive to start the graph at 0
    min_x_val = 0
    # line of best fit using our linear regression
    # ORIGINAL VALS:

    # our_slope = 1.73e-6
    # our_intercept = 6.4e-6
    our_y1 = calculate_coeff(min_x_val, our_slope, our_intercept)
    our_y2 = calculate_coeff(max_x_val, our_slope, our_intercept)
    fig.add_trace(go.Scatter(x=[min_x_val, max_x_val], y=[our_y1, our_y2], mode="lines",
                             line=go.scatter.Line(color=px.colors.qualitative.Pastel[0]), name="our line"))

    # line of best fit using sklearn's multiple linear regression
    sk_slope = 0.08
    sk_intercept = 6.05e-6
    sk_y1 = calculate_coeff(min_x_val, sk_slope, sk_intercept)
    sk_y2 = calculate_coeff(max_x_val, sk_slope, sk_intercept)
    fig.add_trace(go.Scatter(x=[min_x_val, max_x_val], y=[sk_y1, sk_y2], mode="lines",
                             line=go.scatter.Line(color=px.colors.qualitative.Pastel[5]), name="sk line"))

    fig.show()


################################################################################
# 3D Scatter Plots and Regression Surface
################################################################################
def powerplants_and_emissions_plot() -> None:
    """Plot emission and non-emissions power plants per capita to prediict carbon emissions per capita
    on a 3D scatter plot.
    Then add a regression regression surface.
    Each point that is plotted represents a country.

    Documentation for 3D plot available at https://plotly.com/python/3d-scatter-plots/
    Documentation for regression surface available at https://plotly.com/python/ml-regression/
    """
    powerplantdf = power_plant_df()

    fig = px.scatter_3d(powerplantdf, x='Emission Power Plants per Capita',
                        y='Non-Emission Power Plants per Capita',
                        z='Carbon Emissions per Capita',
                        title='Carbon Emissions and Type of Power Plants per Capita',
                        template='ggplot2')
    fig.show()


################################################################################
# Helper Functions
################################################################################
def duplicate_emissions(emission: List[List], countries: List) -> List:
    """Return a list with duplicated carbon emissions corresponding with the countries that go
    with all nuclear power plants.
    """
    emissions_so_far = []
    for country in countries:
        i = emission[0].index(country)
        emissions_so_far.append(emission[1][i])

    return emissions_so_far


def calculate_coeff(x_value: float, m_value: float, b_value: float) -> float:
    """Calculate the y-value in the linear regression equation, y = mx + b
    using the given coefficients.
    """
    return (m_value * x_value) + b_value


if __name__ == '__main__':
    import python_ta

    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'extra-imports': ['python_ta.contracts', 'pandas', 'plotly.express', 'data_processing'],
    #     'disable': ['R1705', 'C0200'],
    # })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()
