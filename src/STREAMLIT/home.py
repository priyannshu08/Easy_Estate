import streamlit as st

st.set_page_config(
    page_title="Gurgaon Real Estate Analytics App",
    page_icon="🏡",
    layout="wide"
)

st.write("# Welcome to the Gurgaon Real Estate Analytics App! 🏡")

st.markdown("""
## Navigation
Use the sidebar to navigate to different sections:

- **Price Predictor** - Predict property prices based on various features
- **Analysis App** - Explore data visualizations and analytics
- **Recommend Apartments** - Get apartment recommendations based on your preferences

Get started by selecting a page from the sidebar!
""")

st.info("💡 Navigate using the menu in the left sidebar to access different features of the app.")
