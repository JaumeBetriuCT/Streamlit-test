import streamlit as st

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def dowload_button(df):
    csv = convert_df(df)

    st.download_button(
        label="Download clusering data as CSV",
        data=csv,
        file_name='clustering_data.csv',
        mime='text/csv',
    )