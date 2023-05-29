import streamlit as st
import pandas as pd
import numpy as np
import plost
import plotly.express as px
from PIL import Image
import calendar 
# Page setting
st.set_page_config(layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Data
seattle_weather = pd.read_csv('https://raw.githubusercontent.com/tvst/plost/master/data/seattle-weather.csv', parse_dates=['date'])
stocks = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/stocks_toy.csv')

# Row A

a1, a2 = st.columns(2)
a1.image(Image.open('streamlit-logo-secondary-colormark-darktext.png'))
a2.metric("Temperature", seattle_weather['temp_max'].iloc[-1])



# Row B
data = seattle_weather
time_range = st.sidebar.selectbox('sélectionner la plage horaire', ['All','Year', 'Month', 'Day'], key='time_range')

# Define the date range based on the selected time range
if time_range == 'All':
    date_range = (data['date'].min(), data['date'].max())
else:
    year = st.sidebar.selectbox ('select year', sorted(data['date'].dt.year.unique()), key='year')
    if time_range == 'Year':
        date_range = (pd.Timestamp(f'{year}-01-01'), pd.Timestamp(f'{year}-12-31'))
    elif time_range == 'Month':
        m = st.sidebar.selectbox('Select Month', sorted(data.loc[data['date'].dt.year == year]['date'].dt.month.unique()), key='month')
        last_day = calendar.monthrange(year, m)[1]  # Get the last day of the specified month
        date_range = (pd.Timestamp(f'{year}-{m}-01'), pd.Timestamp(f'{year}-{m}-{last_day}'))
    elif time_range == 'Day':
        m = st.sidebar.selectbox('Select Month', sorted(data.loc[data['date'].dt.year == year]['date'].dt.month.unique()), key='month')
        day = st.sidebar.selectbox('Select Day', sorted(data.loc[(data['date'].dt.year == year) & (data['date'].dt.month == m )]['date'].dt.day.unique()), key='day')

        date_range = (pd.Timestamp(f'{year}-{m}-{day}'), pd.Timestamp(f'{year}-{m}-{day}'))

# Filter the data based on the selected date range
filtered_data = data.loc[(data['date'] >= date_range[0]) & (data['date'] <= date_range[1])]

# Add a plot type selector
plot_type = st.sidebar.selectbox('Select Plot Type', ['Line Plot', 'Scatter Plot', 'Bar Chart', 'Box Plot', 'Violin Plot'])

data_column = st.sidebar.selectbox('Select Data Column', ['temp_max', 'temp_min', 'precipitation', 'wind'])

# Create the plot
if plot_type == 'Line Plot':
    fig = px.line(filtered_data, x='date', y=data_column, title='Line Plot')
elif plot_type == 'Scatter Plot':
    fig = px.scatter(filtered_data, x='date', y=data_column, title='Scatter Plot')
elif plot_type == 'Bar Chart':
    fig = px.bar(filtered_data, x='date', y=data_column, title='Bar Chart')
elif plot_type == 'Box Plot':
    fig = px.box(filtered_data, x='date', y=data_column, title='Box Plot')
elif plot_type == 'Violin Plot':
    fig = px.violin(filtered_data, x='date', y=data_column, title='Violin Plot', box=True, points='all')


# Show the plot
st.plotly_chart(fig)

# Add a data table
st.write('Data Table')
st.write(filtered_data)
