import streamlit as st
import pandas as pd
import numpy as np

########## USAGE: ###########
#                           #
# streamlit run .\main.py   #
#############################


# Set the page title
st.title('Basic Random Data Visualization with Streamlit')

# Create some sample data
# Generate 100 rows and 3 columns of random data
df = pd.DataFrame(
    np.random.randn(100, 3),
    columns=['a', 'b', 'c']
)

# Display the raw data (optional, using an expandable element)
with st.expander("View Raw Data"):
    st.write(df)

# Create a line chart using Streamlit's native charting
st.subheader('Line Chart of Random Data')
st.line_chart(df)

# Create a bar chart
st.subheader('Bar Chart of Column "a" Values')
# For a bar chart, we might only use one column or specify x and y
st.bar_chart(df['a'])

# Create a simple interactive map (requires latitude/longitude data)
st.subheader('Map of Random Coordinates')
map_data = pd.DataFrame(
    np.random.randn(50, 2) / [50, 50] + [32.09, 34.82],# Centered around our school
    columns=['latitude', 'longitude']
)
st.map(map_data)