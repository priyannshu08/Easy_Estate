import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns


import os

# Resolve paths relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '../../..'))
MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')
DATASETS_DIR = os.path.join(SCRIPT_DIR, '..', 'datasets')

st.set_page_config(page_title="Plotting Demo")

st.title('Analytics')

new_df = pd.read_csv(os.path.join(DATASETS_DIR, 'data_viz1.csv'))
feature_text = pickle.load(open(os.path.join(MODELS_DIR, 'feature_text.pkl'),'rb'))


group_df = new_df[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']].groupby(new_df['sector']).mean()

st.header('Sector Price per Sqft Geomap')
fig = px.scatter_map(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                  color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                  mapbox_style="open-street-map",text=group_df.index)


st.plotly_chart(fig,use_container_width=True)

st.header('Features Wordcloud')

wordcloud = WordCloud(width = 800, height = 800,
                      background_color ='black',
                      stopwords = set(['s']),  # Any stopwords you'd like to exclude
                      min_font_size = 10).generate(feature_text)

fig, ax = plt.subplots(figsize = (8, 8), facecolor = None)
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
plt.tight_layout(pad = 0)
st.pyplot(fig)

st.header('Area Vs Price')

property_type = st.selectbox('Select Property Type', ['flat','house'])

if property_type == 'house':
    fig1 = px.scatter(new_df[new_df['property_type'] == 'house'], x="built_up_area", y="price", color="sector", title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)
else:
    fig1 = px.scatter(new_df[new_df['property_type'] == 'flat'], x="built_up_area", y="price", color="sector",
                      title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)

st.header('BHK Pie Chart')

sector_options = new_df['sector'].unique().tolist()
sector_options.insert(0,'overall')

selected_sector = st.selectbox('Select Sector', sector_options)

if selected_sector == 'overall':
    # Count properties by bedRoom
    bhk_counts = new_df['bedRoom'].value_counts().reset_index()
    bhk_counts.columns = ['bedRoom', 'count']
    fig2 = px.pie(bhk_counts, values='count', names='bedRoom', title='Property Distribution by BHK')

    st.plotly_chart(fig2, use_container_width=True)
else:
    # Count properties by bedRoom for selected sector
    sector_df = new_df[new_df['sector'] == selected_sector]
    bhk_counts = sector_df['bedRoom'].value_counts().reset_index()
    bhk_counts.columns = ['bedRoom', 'count']
    fig2 = px.pie(bhk_counts, values='count', names='bedRoom', title=f'Property Distribution by BHK - {selected_sector}')

    st.plotly_chart(fig2, use_container_width=True)

st.header('Side by Side BHK price comparison')

fig3 = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price', title='BHK Price Range')

st.plotly_chart(fig3, use_container_width=True)


st.header('Side by Side Distplot for property type')

fig3 = plt.figure(figsize=(10, 4))
sns.histplot(new_df[new_df['property_type'] == 'house']['price'], label='house', kde=True)
sns.histplot(new_df[new_df['property_type'] == 'flat']['price'], label='flat', kde=True)
plt.legend()
st.pyplot(fig3)