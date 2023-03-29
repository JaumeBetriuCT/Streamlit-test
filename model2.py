import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import plotly.subplots as sp
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from utils import dowload_button, detect_quarter, get_months_between_dates, name_quarter
from quarter_comparison import run_quarter_comparison

def run_cluster2():
    st.write("kk")
    df = pd.read_csv("data_model2.csv")

    cluster_labels = sorted(df["cluster_labels"].unique())
    cluster_labels.pop(2)
    cluster_labels.pop(len(cluster_labels)-1)
    cluster_labels = cluster_labels + ["cluster_10", "cluster_outliers"]

    cluster_percentages = 100 * df["cluster_labels"].value_counts() / len(df)
    cluster_percentages = cluster_percentages.reindex(cluster_labels)
    s = cluster_percentages

    # create the pie chart
    fig_0_0 = go.Figure(
        data=go.Pie(
            labels=s.index,
            values=s.values,
            textinfo='label+percent',
            hole=0.3,
            insidetextorientation='horizontal',
            marker=dict(colors=px.colors.qualitative.Set3),
            sort=False
        )
    )

    # update the layout of the pie chart
    fig_0_0.update_layout(
        legend=dict(
            traceorder='normal',
            font=dict(size=12),
            title=dict(text='Clusters', font=dict(size=14)),
            itemsizing='constant',
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)',
            borderwidth=0,
            orientation='v',
            yanchor='top',
            y=1,
            xanchor='left',
            x=0.01,
            itemclick='toggleothers'
        ),
        height=675,
        width=800
    )

    def run_emergency_model2(df, top_clusters):

        comp_prop = df.copy()
        comp_prop = comp_prop.loc[comp_prop["cluster_labels"] != "cluster_outliers"]
        comp_prop = comp_prop.groupby(by=["cluster_labels"]).agg({"emergency_prop":"mean"})
        comp_prop = comp_prop.reset_index()
        comp_prop["no_emergency"] = round(1 - comp_prop["emergency_prop"], 2)
        comp_prop["emergency_prop"] = round(comp_prop["emergency_prop"], 2)
        comp_prop.sort_values(by="emergency_prop", ascending=False, inplace=True)

        top_emergency_clusters = list(comp_prop["cluster_labels"][:top_clusters])

        comp_prop = comp_prop.loc[comp_prop["cluster_labels"].isin(top_emergency_clusters)]

        colors = px.colors.qualitative.Set3
        fig_0_1 = go.Figure()

        fig_0_1.add_trace(
            go.Bar(x=comp_prop["cluster_labels"], 
                y=comp_prop["no_emergency"], 
                text=comp_prop["no_emergency"], 
                name="No emergency", 
                textposition='auto', 
                marker_color=colors[8])
        )
        fig_0_1.add_trace(
            go.Bar(x=comp_prop["cluster_labels"], 
                y=comp_prop["emergency_prop"], 
                text=comp_prop["emergency_prop"], 
                name="Emergency", 
                textposition='auto', 
                marker_color=colors[3])
        )
        fig_0_1.update_layout(
            height=500,
            width=950,
            barmode='stack'
        )

        return fig_0_1

    col_3, col_4 = st.columns(2)
    with col_3:
        st.subheader("Clusters distribution:")
        st.plotly_chart(fig_0_0)
    with col_4:
        st.subheader("Emergency plots:")
        selected_clusters = st.slider("Select the number of top emergency clusters:", 
            min_value=1, 
            max_value=len(df["cluster_labels"].unique()),
            value=3
        )
        fig_0_1 = run_emergency_model2(df, selected_clusters)
        st.plotly_chart(fig_0_1)

    # COMPARISON BETWEEN CHANELS
    st.header("Comparison between chanels:")

    chanels = st.multiselect(
        label = "Select the chanels that you would like to compare:",
        options = df["canal_fav"].unique(),
        default = ["Emailings", "Mailing"],
    )

    comp = df.loc[df["canal_fav"].isin(chanels)]
    comp = comp.groupby(by=["cluster_labels", "canal_fav"]).count()[["id", "emergency_prop"]].drop("emergency_prop", axis=1)

    comp = comp.reindex(cluster_labels, level=0)
    comp.reset_index(inplace=True)

    chanel_datasets = []
    for chanel in chanels:
        chanel_datasets.append(comp.loc[comp["canal_fav"] == chanel])

    colors = px.colors.qualitative.Set3

    fig_chanels = go.Figure()
    for i, chanel_dataset in enumerate(chanel_datasets):
        # We take the id as the y axis because after doing the groupby the column id represents the count
        fig_chanels.add_trace(
            go.Bar(
                x=chanel_dataset["cluster_labels"], 
                y=chanel_dataset["id"], 
                text=chanel_dataset["id"], 
                name=chanel_dataset["canal_fav"].unique()[0], 
                textposition='auto', 
                marker_color=colors[i]
            )
        )

    # update the layout of the plot
    fig_chanels.update_layout(
        xaxis_title='Cluster',
        yaxis_title='Contacts',
        height=700,
        width=1700,
        barmode="stack"
    )
    
    st.plotly_chart(fig_chanels)
    # END COMPARISON BETWEEN CHANELS

    # COMPARISON BETWEEN QUARTERS
    st.header("Comparison between quarters:")
    with st.columns(2)[0]:
        range_dates = st.date_input(
            label = "Please enter the range of dates in which you want to launch the campaign:",
            value = (pd.to_datetime("2023-02-01"), pd.to_datetime("2023-03-10")),
        )
    
    months_in_between = get_months_between_dates(range_dates[0], range_dates[1])

    quarters = list(set([detect_quarter(month) for month in months_in_between]))

    quarters_name = [name_quarter(quarter) for quarter in quarters]

    with st.columns(2)[0]:
        if len(quarters_name) == 1:
            st.info(f"You have selected the quarter: {quarters_name[0]}")
        else:
            st.info(f"You have selected the quarters: {quarters_name}")


    run_quarter_comparison(quarters_name)
        
    # END COMPARISON BETWEEN QUARTERS

    col_7, col_8 = st.columns(2)
    with col_7:
        st.subheader("Dataframe:")
        st.write(df)
    with col_8:
        st.subheader("Download:")
        st.write("Whole dataset:")
        dowload_button(df)
        st.write("Id's and cluster clasification:")
        dowload_button(df[["id", "cluster_labels"]])


