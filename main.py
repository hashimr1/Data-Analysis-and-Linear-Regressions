"""CSC110 Fall 2020 Final Assignment Visualizations

Description
===============================
Copyright and Usage Information
===============================
This file is provided solely for the final assignment of CSC110 at the University of Toronto
St. George campus. All forms of distribution of this code, whether as given or with any changes,
are expressly prohibited.
This file is Copyright (c) 2020 Raazia Hashim, Kenneth Miura, Shilin Zhang

"""
import numpy as np
import regression
import data_processing
import visualizations


if __name__ == '__main__':
    # Data Processing:
    _, proportions = data_processing.read_powerplant_file('global_power_plant_database.csv',
                                                          'owid-co2-data.csv',
                                                          'countries of the world.csv')
    _, co2_emissions = data_processing.read_carbon_emission_file('global_power_plant_database.csv',
                                                                 'owid-co2-data.csv',
                                                                 'countries of the world.csv')

    _, nuclear_plants = data_processing.read_nuclear_powerplant('global_power_plant_database.csv',
                                                                'owid-co2-data.csv',
                                                                'countries of the world.csv')
    _, nuclear_co2 = data_processing.read_nuclear_powerplant_co2('global_power_plant_database.csv',
                                                                 'owid-co2-data.csv',
                                                                 'countries of the world.csv')

    proportions = np.array(proportions)
    co2 = np.array(co2_emissions).reshape((-1, 1))

    emissions_plants = proportions[:, 0].reshape((-1, 1))
    non_emission_plants = proportions[:, 1].reshape((-1, 1))

    nuclear_plants = np.array(nuclear_plants).reshape(-1, 1)
    nuclear_co2 = np.array(nuclear_co2).reshape(-1, 1)

    # Regression:
    emissions_coeff, non_emissions_coeff, offset = regression.ols_linear_regression(proportions,
                                                                                    co2)

    emissions_only_coeff, emissions_only_offset = regression.ols_linear_regression(emissions_plants,
                                                                                   co2)

    non_emissions_only_coeff, non_emissions_only_offset = regression.ols_linear_regression(non_emission_plants,
                                                                                           co2)

    nuclear_coeff, nuclear_offset = regression.ols_linear_regression(nuclear_plants, nuclear_co2)

    # Visualizations:
    visualizations.emissions_power_plants_plot(emissions_only_coeff.item(), emissions_only_offset.item())

    visualizations.non_emissions_power_plants_plot(non_emissions_only_coeff.item(), non_emissions_only_offset.item())

    visualizations.powerplants_and_emissions_plot(emissions_coeff.item(), non_emissions_coeff.item(), offset.item())

    # UNCOMMENT BELOW TO VIEW NUCLEAR EMISSIONS REGRESSION PLOT AND NUCLEAR PLANTS POSITION MAP

    # visualizations.nuclear_emissions_plot(nuclear_coeff.item(), nuclear_offset.item())

    # visualizations.nuclear_position_map()
