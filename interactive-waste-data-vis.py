import pandas as pd
import streamlit as st
from datetime import datetime
import pytz
import re
import numpy as np


def create_date(row):
    try:
        year = int(row['Year'])
        
        month = int(row['MonthNum'])
        
        date_with_timezone = datetime(year, month, 1, 0, 0, 0, tzinfo=pytz.UTC)
        return date_with_timezone
    
    except Exception as e:
        return pd.NaT


df = pd.read_csv('assign2_25S_wastedata.csv')

if df['Weight (lbs)'].dtype == 'object':
    df['Weight (lbs)'] = df['Weight (lbs)'].str.replace(',','')

df['Weight (lbs)'] = pd.to_numeric(df['Weight (lbs)'], errors='coerce')
df['Weight (lbs)'] = df['Weight (lbs)'].fillna(0).astype('float64')

month_map = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
    'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
    'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
}
df['MonthNum'] = df['Month'].map(month_map)
df = df.dropna(subset=['MonthNum']).copy()

df['date'] = df.apply(create_date, axis=1)
df = df.dropna(subset=['date'])

min_date = df['date'].min().date()
max_date = df['date'].max().date()

# Create a list of month-year dates for the slider
dates = pd.date_range(start=min_date, end=max_date, freq='MS').tolist()
date_labels = [d.strftime('%m-%Y') for d in dates]

# Map the formatted dates back to actual datetime objects
date_dict = dict(zip(date_labels, dates))

options = df['Category'].unique().tolist()
selected_values = st.multiselect(
    "Select categories:",
    options=options,
    default=options
)

# Create slider with formatted date labels
selected_date_labels = st.select_slider(
    'Date Range:',
    options=date_labels,
    value=(date_labels[0], date_labels[-1])
)

# Convert selected labels back to datetime for filtering
start_date = date_dict[selected_date_labels[0]].date()
end_date = date_dict[selected_date_labels[1]].date()

# Use these dates for filtering
filtered_by_date_and_option = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date) & df['Category'].isin(selected_values)]
filtered_by_date_and_option['date'] = filtered_by_date_and_option['date'].dt.strftime('%Y-%m')
pivot_table_df = filtered_by_date_and_option.pivot_table(
    index='date',
    columns='Category',
    values='Weight (lbs)',
    aggfunc='sum'
).fillna(0)

#pivot_table_df = pivot_table_df.resample('M').sum()

st.line_chart(pivot_table_df)
st.write(pivot_table_df)
