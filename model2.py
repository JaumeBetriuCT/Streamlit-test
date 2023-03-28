import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import plotly.subplots as sp
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from utils import dowload_button

def run_cluster2():
    df = pd.read_csv("data_clusters.csv")

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
        title='Cluster Distribution',
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

    #Comparation between captacion digital y offline

    comp = df.loc[(df["canal_fav"] == "Captacion_digital") | (df["canal_fav"] == "Captacion_offline")]
    comp = comp.groupby(by=["cluster_labels", "canal_fav"]).count()

    comp = comp.reindex(cluster_labels, level=0)
    comp.reset_index(inplace=True)

    digital = comp.loc[comp["canal_fav"] == "Captacion_digital"]
    offline = comp.loc[comp["canal_fav"] == "Captacion_offline"]

    colors = px.colors.qualitative.Set3

    fig_1_1 = go.Figure()
    fig_1_1.add_trace(go.Bar(x=digital["cluster_labels"], y=digital["emergency_prop"], text=digital["emergency_prop"], name="Digital", textposition='auto', marker_color=colors[5]))
    fig_1_1.add_trace(go.Bar(x=offline["cluster_labels"], y=offline["emergency_prop"], text=offline["emergency_prop"], name="Offline", textposition='auto', marker_color=colors[6]))

    # update the layout of the plot
    fig_1_1.update_layout(
        title='Comparison between Digital and Offline chanels',
        xaxis_title='Cluster',
        yaxis_title='Contacts',
        height=625,
        width=825
    )

    #Comparation between captacion emailing y mailing

    comp = df.loc[(df["canal_fav"] == "Emailings") | (df["canal_fav"] == "Mailing")]
    comp = comp.groupby(by=["cluster_labels", "canal_fav"]).count()

    comp = comp.reindex(cluster_labels, level=0)
    comp.reset_index(inplace=True)

    digital = comp.loc[comp["canal_fav"] == "Emailings"]
    offline = comp.loc[comp["canal_fav"] == "Mailing"]

    colors = px.colors.qualitative.Set3

    fig_2_2 = go.Figure()
    fig_2_2.add_trace(go.Bar(x=digital["cluster_labels"], y=digital["emergency_prop"], text=digital["emergency_prop"], name="Emailings", textposition='auto', marker_color=colors[2]))
    fig_2_2.add_trace(go.Bar(x=offline["cluster_labels"], y=offline["emergency_prop"], text=offline["emergency_prop"], name="Mailing", textposition='auto', marker_color=colors[3]))

    # update the layout of the plot
    fig_2_2.update_layout(
        title='Comparison between Emailing and Mailing chanels',
        xaxis_title='Cluster',
        yaxis_title='Contacts',
        height=625,
        width=825
    )

    clusters = []

    for clus in cluster_labels:
        clusters.append(df.loc[df["cluster_labels"] == clus])
    clusters = iter(clusters)

    fig_4_4 = sp.make_subplots(rows=6, cols=2, specs=[[{'type': 'pie'}]*2]*6)

    for i in range(1,7):
        for j in range(1,3):
            dataframe = next(clusters)
            labels = [
                "Verano",
                "Otoño",
                "Invierno/Navidad",
                "Primavera"
            ]
            values = [
                dataframe["MoreThanAvgDonator_Jun_Jul_Aug_quarter"].sum(),
                dataframe["MoreThanAvgDonator_Set_Oct_Nov_quarter"].sum(),
                dataframe["MoreThanAvgDonator_Dec_Jan_Feb_quarter"].sum(),
                dataframe["MoreThanAvgDonator_Mar_Apr_May_quarter"].sum()
            ]
            
            fig_4_4.add_trace(
                go.Pie(
                    labels = labels,
                    values = values,
                    textinfo='label',
                    hole=0.3,
                    insidetextorientation='horizontal',
                    marker=dict(colors=px.colors.qualitative.Set3),
                    sort=False,
                    title=dataframe["cluster_labels"].unique()[0],
                    title_font=dict(size=18),
                    domain={'x': [0, 1], 'y': [0, 1]}
                ),
                row=i,
                col=j
            )

    fig_4_4.update_layout(
        title='Distribución de los trimestres en los diferentes clusters',
        height=3000,
        width=1300
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
        st.plotly_chart(fig_0_0)
    with col_4:
        st.subheader("Emergency plots:")
        selected_clusters = st.slider("Select the number of top emergency clusters:", 
            min_value=1, 
            max_value=len(df["cluster_labels"].unique())
        )
        fig_0_1 = run_emergency_model2(df, selected_clusters)
        st.plotly_chart(fig_0_1)

    col_5, col_6 = st.columns(2)
    with col_5:
        st.plotly_chart(fig_1_1)
    with col_6:
        st.plotly_chart(fig_2_2)
    

