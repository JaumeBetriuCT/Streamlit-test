import streamlit as st
import plotly.graph_objects as go

# Generate some random data for the bar plot
x_data = ['A', 'B', 'C', 'D', 'E']
y_data = [1, 2, 3, 4, 5]

# Create the bar plot using Plotly
fig = go.Figure(data=[go.Bar(x=x_data, y=y_data)])

# Set the plot title and axis labels
fig.update_layout(title='Random Bar Plot', xaxis_title='X Axis', yaxis_title='Y Axis')

# Show the plot
fig.show()