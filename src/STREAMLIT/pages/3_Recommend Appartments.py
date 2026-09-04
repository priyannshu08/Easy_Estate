import streamlit as st
import pickle
import pandas as pd
import numpy as np


import os

# Resolve paths relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '../../..'))
MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')
DATASETS_DIR = os.path.join(SCRIPT_DIR, '..', 'datasets')

st.set_page_config(page_title="Recommend Appartments")

location_df = pickle.load(open(os.path.join(MODELS_DIR, 'location_distance.pkl'),'rb'))

cosine_sim1 = pickle.load(open(os.path.join(MODELS_DIR, 'cosine_sim1.pkl'),'rb'))
cosine_sim2 = pickle.load(open(os.path.join(MODELS_DIR, 'cosine_sim2.pkl'),'rb'))
cosine_sim3 = pickle.load(open(os.path.join(MODELS_DIR, 'cosine_sim3.pkl'),'rb'))


def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3
    # cosine_sim_matrix = cosine_sim3

    # Get the similarity scores for the property using its name as the index
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))

    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]

    # Retrieve the names of the top properties using the indices
    top_properties = location_df.index[top_indices].tolist()

    # Create a dataframe with the results
    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })

    return recommendations_df


st.title('Apartment Recommendation System')

# Get available properties
available_properties = location_df.index.tolist()

# Let user select a property
selected_property = st.selectbox('Select a Property', available_properties)

if selected_property:
    st.header(f'Recommendations for {selected_property}')
    recommendations = recommend_properties_with_scores(selected_property)
    st.dataframe(recommendations)

# Note: This is a simple recommendation system for now
# The actual location-based search functionality would need additional setup

st.title('Recommend Appartments')
selected_appartment = st.selectbox('Select an appartment',sorted(location_df.index.to_list()))

if st.button('Recommend'):
    recommendation_df = recommend_properties_with_scores(selected_appartment)

    st.dataframe(recommendation_df)



