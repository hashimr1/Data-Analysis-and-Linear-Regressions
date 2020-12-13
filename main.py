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
import regression
import data_processing
import visualizations

if __name__ == '__main__':
    # Call all the functions from our individual pieces of code
    names, proportions = data_processing.read_powerplant_file('global_power_plant_database.csv', 'owid-co2-data.csv')
    _, emissions = data_processing.read_carbon_emission_file('global_power_plant_database.csv', 'owid-co2-data.csv')
    params = regression.linear_regression(proportions, emissions, 10000, 0.5)
    print(params)
    # regression.show_error()
    pass
