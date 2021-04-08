# CSC110 Final Project
# Relationship between Emission and Non-Emission Power Plants on Carbon Emissions
The United Nations has recognized climate change to be an imminent threat to humankind.  In response, the Paris Agreement, signed in 2015 by a total of 197 countries around the world aims to limit the global temperature rise below 2 degree celsius,  while aiming to limit the increase under 1.5 degree celsius. Naturally, a large focus of these efforts is on the global energy sector, as 25% of 2010 global greenhouse gas emissions were a result of electricity and heat production(EPA, 2020).
Our goal is to use current powerplant and carbon emission data to predict how the number of emission and non-emission powerplants in a country impact their carbon emissions. The research question we explored is, “How does the number of Emissions and Non-Emissions powerplants per capita in a countrypredict their Carbon Emissions per capita?”

## Data Processing
Raw data from 3 different data sets (countries of the world.csv, global_power_plant_database.csv, owid-co2-data.csv) containing data about population, carbon emissions and powerplants for most countires around the world, was processed from the original csv file into lists of lists into formats that can be used for computations. 

## Regression
Implemented two different regression methods, using the Numpy python library and trained them on 20% of the data and computed the average error and comparing that to the SKlearn python libarary implementation of linear regression. Used our implementation to make predictions based on our coefficients.  

## Visualizations
Visualizations of the data were done using the Plotly (plotly.express and plotly.graphobjects) and Pandas python libraries. 
Data in the form of Lists were converted to Pandas Data Frames objects. Data and lines of best fit that were computed were viualized using plotly functions.
