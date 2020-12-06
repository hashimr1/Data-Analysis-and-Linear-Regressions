import regression
import data_processing

if __name__ == '__main__':
    # Call all the functions from our individual pieces of code
    names, proportions = data_processing.read_powerplant_file('global_power_plant_database.csv', 'owid-co2-data.csv')
    _, emissions = data_processing.read_carbon_emission_file('global_power_plant_database.csv', 'owid-co2-data.csv')
    params = regression.linear_regression(proportions, emissions, 10000, 0.5)
    print(params)
    # regression.show_error()
    pass
