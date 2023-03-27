import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.header("Test clustering")
st.subheader("Sub Title")

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
    )
)

st.plotly_chart(fig_0_0)