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

        day = 1
        if pd.notna(row['Day']):
            day = int(row['Day'])
            
        
        date_with_timezone = datetime(year, month, day, 8, 0, 0, tzinfo=pytz.UTC)
        return date_with_timezone
    
    except Exception as e:
        return pd.NaT


df = pd.read_csv('assign2_25S_wastedata.csv')

#df['Weight (lbs)'] = df['Weight (lbs)'].replace('', np.nan)
if df['Weight (lbs)'].dtype == 'object':
    df['Weight (lbs)'] = df['Weight (lbs)'].str.replace(',','')

df['Weight (lbs)'] = pd.to_numeric(df['Weight (lbs)'], errors='coerce')
df['Weight (lbs)'] = df['Weight (lbs)'].fillna(0)

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

#Options for multiselect
options = df['Category'].unique().tolist()
selected_values = st.multiselect(
    "Select categories:",
    options=options,
    default=options
)

date_range = st.slider(
    'Date Range:',
    min_value=min_date,
    max_value=max_date,
    value=(min_date,max_date)
)

filtered_by_date_and_option = df[(df['date'].dt.date >= date_range[0]) & (df['date'].dt.date <= date_range[1]) & df['Category'].isin(selected_values)]
pivot_table_df = filtered_by_date_and_option.pivot_table(
    index='date',
    columns='Category',
    values='Weight (lbs)',
    aggfunc='sum'
)

print(pivot_table_df.head())
st.write(pivot_table_df.dtypes)
st.line_chart(pivot_table_df)