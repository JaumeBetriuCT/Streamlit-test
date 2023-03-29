import streamlit as st
from datetime import date

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def dowload_button(df):
    csv = convert_df(df)

    st.download_button(
        label="Download clusering data as CSV",
        data=csv,
        file_name='data_model2.csv',
        mime='text/csv',
    )

def get_months_between_dates(start_date, end_date):
    months = []
    current_month = start_date.month
    current_year = start_date.year

    while current_year < end_date.year or (current_year == end_date.year and current_month <= end_date.month):
        months.append(date(current_year, current_month, 1))
        current_month += 1

        if current_month > 12:
            current_month = 1
            current_year += 1

    return months

def detect_quarter(date):
    month_date = date.month
    
    if (month_date == 12) | (month_date == 1) | (month_date == 2):
        return 1 # "Dec_Jan_Feb_quarter"
    if (3 <= month_date) & (month_date <= 5):
        return 2 #"Mar_Apr_May_quarter"
    if (6 <= month_date) & (month_date <= 8):
        return 3 #"Jun_Jul_Aug_quarter"
    if (9 <= month_date) & (month_date <= 11):
        return 4 #"Set_Oct_Nov_quarter"

def name_quarter(quarter_name):
    dict_quarter_names = {
        1: "Dec_Jan_Feb_quarter",
        2: "Mar_Apr_May_quarter",
        3: "Jun_Jul_Aug_quarter",
        4: "Set_Oct_Nov_quarter"
    }

    return dict_quarter_names[quarter_name]
