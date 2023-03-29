import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def run_quarter_comparison(quarters_name):

    st.write("To do")

    # colors = px.colors.qualitative.Set3

    # fig_chanels = go.Figure()
    # for i, chanel_dataset in enumerate(chanel_datasets):
    #     # We take the id as the y axis because after doing the groupby the column id represents the count
    #     fig_chanels.add_trace(
    #         go.Bar(
    #             x=chanel_dataset["cluster_labels"], 
    #             y=chanel_dataset["id"], 
    #             text=chanel_dataset["id"], 
    #             name=chanel_dataset["canal_fav"].unique()[0], 
    #             textposition='auto', 
    #             marker_color=colors[i]
    #         )
    #     )

    # # update the layout of the plot
    # fig_chanels.update_layout(
    #     xaxis_title='Cluster',
    #     yaxis_title='Contacts',
    #     height=700,
    #     width=1700,
    #     barmode="stack"
    # )
    
    # st.plotly_chart(fig_chanels)