import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(layout="wide")
# Set the title of the app
st.title('Boston Property Assessment FY2024 Dashboard')

# Load the dataset
@st.cache_data  # This decorator caches the data loading to speed up app loading
def load_data():
    # path = "/Users/amoghagadde/Desktop/Amogha/Northeastern/SEM_2/Comp_Viz/Projects/Project_4/fy2024-property-assessment-data_1_5_2024.csv"
    path = "fy2024-property-assessment-data_1_5_2024.csv"
    df = pd.read_csv(path)
    return df

df = load_data()
df['TOTAL_VALUE'] = df['TOTAL_VALUE'].str.replace(',','').astype(int)
df['ZIP_CODE'] = df.ZIP_CODE.apply(lambda x: f'0{x:.0f}')
# Display the first few rows of the dataframe
st.write("Data Overview:", df.head())

col_1, col_2, col_3 = st.columns([2,1,2])

with col_1:
    # Plotting
    location = st.selectbox(
        'Which location are you interested in?', df.CITY.unique())
    # df_overall_cond = df[df['CITY'] == location].groupby('OVERALL_COND', as_index=False)['PID'].count()
    df_overall_cond = df[df['CITY'] == location]
    fig = px.pie(df_overall_cond, names='OVERALL_COND', title=f'Condition of Houses in {location}')
    st.plotly_chart(fig, use_container_width=True)

with col_2:
    # Selection box for choosing a column to plot
    option = st.selectbox(
        'Which column do you want to explore?',
        df.columns)

    # Display basic statistics for the selected column
    st.write(f"Statistics for {option}:", df[option].describe())

with col_3:
    fig_line = px.scatter(df, x='LIVING_AREA', y='TOTAL_VALUE', trendline="ols",
                    title='Property Value vs. Living Area')
    st.plotly_chart(fig_line, use_container_width=True)

zip_code = col_1.selectbox(
    'Which location are you interested in?', df.ZIP_CODE.unique())
filtered_df = df[df['ZIP_CODE'] == zip_code]
cond_counts = filtered_df['OVERALL_COND'].value_counts().nlargest(5)

# Plotting the bar chart with log scale on y-axis and counts on the bars
fig_bar = px.bar(cond_counts, 
            title='Average Property Value by ZIP Code')
st.plotly_chart(fig_bar, use_container_width=True)