import pandas as pd
import streamlit as st
from datetime import datetime
import pytz


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


