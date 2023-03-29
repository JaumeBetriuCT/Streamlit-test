import streamlit as st
from pathlib import Path
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from model2 import run_cluster2
from PIL import Image
import time

st.set_page_config(layout="wide")
                   
with open('credentials.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:

    msf_log = Image.open("MSF_dual_English_-WEB-RGB-4-scaled.jpg")
    
    st.write("<h1 style='font-size: 80px;'>Welcome to MSF Clustering application!</h1>", unsafe_allow_html=True)

    _, col2 = st.columns(2)

    with col2:
        st.image(msf_log, width=700)

    st.sidebar.title("Choose the model:")
    model_option = st.sidebar.selectbox(
        label = "Please, select the model you would like to acces:", 
        options = ["Model 1", "Model 2", "Model 3"],
        index = 1
    )
    
    if model_option == "Model 2":
        time.sleep(5)
        with st.spinner("Loading dashboard"):
            st.write("<h1 style='font-size: 60px;'>Model 2:</h1>", unsafe_allow_html=True)
            run_cluster2()
    
    if model_option == "Model 1":
        time.sleep(5)
        with st.spinner("Loading dashboard"):
            st.write("<h1 style='font-size: 60px;'>Model 1:</h1>", unsafe_allow_html=True)
    #       run_cluster1()
    
    if model_option == "Model 3":
        time.sleep(5)
        with st.spinner("Loading dashboard"):
            st.write("<h1 style='font-size: 60px;'>Model 3:</h1>", unsafe_allow_html=True)
    #       run_cluster1()

    authenticator.logout('Logout', 'main')

    

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
