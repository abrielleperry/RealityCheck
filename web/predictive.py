import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

# Load the data
data_path = 'data/fire.csv'
data = pd.read_csv(data_path)

# Initial preprocessing: conversion, missing values handling, etc.
data['datetime'] = pd.to_datetime(data['date'] + ' ' + data['time'])
data.drop(['date', 'time'], axis=1, inplace=True)
data = data.dropna(subset=['incident'])

# Aggregating daily incidents
daily_incidents = data.groupby(
    [data['datetime'].dt.date, 'incident']).size().reset_index(name='count')

# Ensure the index is a DatetimeIndex
daily_incidents['datetime'] = pd.to_datetime(daily_incidents['datetime'])
incident_data = daily_incidents[daily_incidents['incident'] == 'Building fire']
incident_data.set_index('datetime', inplace=True)

# Resample data to ensure continuous dates for ARIMA
incident_time_series = incident_data['count'].resample('D').sum()

# Define the ARIMA model parameters
model = ARIMA(incident_time_series, order=(1, 1, 1))

# Fit the model
fitted_model = model.fit()

# Display the summary of the fitted model
model_summary = fitted_model.summary()
print(model_summary)
