import pandas as pd
import plotly.express as px
import streamlit as st

def run_quarter_comparison(quarters_name, df):

    quarters_name = ["MoreThanAvgDonator_" + q for q in quarters_name]

    quarters = df.groupby("cluster_labels").sum().reset_index()[["cluster_labels"] + quarters_name]

    quarters_melted = pd.melt(
        quarters, 
        id_vars=["cluster_labels"], 
        var_name="quarter_category", 
        value_name="quarter_value"
    )

    fig_chanels = px.scatter(
        quarters_melted, 
        x="cluster_labels", 
        y="quarter_category", 
        color="quarter_category", 
        size="quarter_value"
    )

    fig_chanels.update_layout(
        xaxis_title='Cluster',
        yaxis_title='Contacts',
        height=500,
        width=1700,
        legend=dict(
            font=dict(
                size=17
            )
        ),
        xaxis=dict(
            title=dict(
                font=dict(
                    size=17
                )
            ),
            tickfont=dict(
                size=17
            )
        ),
        yaxis=dict(
            title=dict(
                font=dict(
                    size=17
                )
            ),
            tickfont=dict(
                size=17
            )
        )
    )

    fig_chanels.update_traces(
        marker=dict(
            sizeref=8
        )
    )

    st.plotly_chart(fig_chanels)