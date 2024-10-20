import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk

# Page configuration
st.set_page_config(page_title="Kevin Kurtz Portfolio", layout="wide", page_icon=":bar_chart:")

# Sidebar
st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/kevin-kurtz/)")
st.sidebar.markdown("[GitHub](https://github.com/ktzkvin)")

# Header
st.title("Kevin Kurtz")
st.subheader("Data Scientist &nbsp;-&nbsp; M1 Data & AI Student at EFREI Paris")

# General profile
st.write("""
    Data & AI master's student at EFREI Paris, passionate about data science and artificial intelligence.
    My skills cover programming, data analysis and machine learning model development.
""")

# Horizontal separator
st.markdown("<hr>", unsafe_allow_html=True)

# Technical and Soft Skills side by side
st.header("💡 Skills Overview")
col1, col2 = st.columns(2)

# Hard Skills
with col1:
    st.subheader("Hard Skills")
    hard_skills = {
        'Skills': ['Python', 'Git', 'SQL', 'Pandas', 'TensorFlow', 'Matplotlib', 'Power BI', 'Scikit-learn'],
        'Proficiency': [8, 8, 5, 8, 7, 9, 6, 7]
    }
    df_hard_skills = pd.DataFrame(hard_skills)
    fig_hard_skills = px.line_polar(df_hard_skills, r='Proficiency', theta='Skills', line_close=True, 
                                    range_r=[0, 10], template="plotly_dark")
    fig_hard_skills.update_traces(fill='toself', fillcolor='rgba(0, 102, 255, 0.5)', line_color='rgba(0, 102, 255, 1)')
    st.plotly_chart(fig_hard_skills, use_container_width=True)

# Soft Skills
with col2:
    st.subheader("Soft Skills")
    soft_skills = {
        'Skills': ['Communication', 'Teamwork', 'Adaptability', 'Problem Solving', 'Creativity', 'Time Management'],
        'Proficiency': [7, 7, 8, 7, 9, 8]
    }
    df_soft_skills = pd.DataFrame(soft_skills)
    fig_soft_skills = px.line_polar(df_soft_skills, r='Proficiency', theta='Skills', line_close=True, 
                                    range_r=[0, 10], template="plotly_dark")
    fig_soft_skills.update_traces(fill='toself', fillcolor='rgba(0, 204, 102, 0.5)', line_color='rgba(0, 204, 102, 1)')
    st.plotly_chart(fig_soft_skills, use_container_width=True)

# Horizontal separator
st.markdown("<hr>", unsafe_allow_html=True)

# Academic Projects
st.header("📚 Academic Projects")

# Project 1
col3, col4 = st.columns([1, 3])
with col3:
    st.image("screenshots/Bougeons_Malin.jpg", use_column_width=True)
with col4:
    st.subheader("🚇 Bougeons Malin - Public Transport Optimization")
    st.write("""
        Development of a neural network algorithm to optimize the distribution of passengers in Paris public transport.  
        Technologies: TensorFlow, Python
    """)
    st.markdown(
        """
        <a href="https://github.com/ktzkvin/SMART" target="_blank">
            <button style="background-color: #4CAF50; border: none; color: white; padding: 10px 20px; text-align: center; 
            text-decoration: none; display: inline-block; font-size: 14px; margin: 4px 2px; cursor: pointer;">
                View on GitHub
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

st.write("")
st.write("")
st.write("")

# Project 2
col5, col6 = st.columns([1, 3])
with col5:
    st.image("screenshots/DVF.jpg", use_column_width=True)
with col6:
    st.subheader("🏠 DVF Data Analysis - Real Estate Price Modeling")
    st.write("""
        Modeling and predicting real estate prices in France, analyzing market trends over several years using Pandas and Matplotlib.  
        Technologies: Pandas, Matplotlib
    """)
    st.markdown(
        """
        <a href="https://github.com/ktzkvin/Mastercamp-DVF" target="_blank">
            <button style="background-color: #4CAF50; border: none; color: white; padding: 10px 20px; text-align: center; 
            text-decoration: none; display: inline-block; font-size: 14px; margin: 4px 2px; cursor: pointer;">
                View on GitHub
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

st.write("")
st.write("")
st.write("")

# Project 3
col7, col8 = st.columns([1, 3])
with col7:
    st.image("screenshots/Explain.jpg", use_column_width=True)
with col8:
    st.subheader("📜 EXPLAIN - Patent Classification System")
    st.write("""
        Development of an automatic patent classification system using Scikit-Learn.  
        Technologies: Scikit-Learn, Python
    """)
    st.markdown(
        """
        <a href="https://github.com/ktzkvin/Mastercamp-EXPLAIN" target="_blank">
            <button style="background-color: #4CAF50; border: none; color: white; padding: 10px 20px; text-align: center; 
            text-decoration: none; display: inline-block; font-size: 14px; margin: 4px 2px; cursor: pointer;">
                View on GitHub
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

# Horizontal separator
st.markdown("<hr>", unsafe_allow_html=True)

# Education Locations Section
st.header("🎓 Education Locations")

st.write("The maps below show the locations where I pursued my education: **EFREI Paris, France** and an **Exchange Program at Asia Pacific University, Kuala Lumpur, Malaysia**.")

# Data for the locations
paris_coords = pd.DataFrame({'lat': [48.8566], 'lon': [2.3522]})
kuala_lumpur_coords = pd.DataFrame({'lat': [3.1390], 'lon': [101.6869]})

# Setting up the map views
paris_view = pdk.ViewState(
    latitude=46.603354,
    longitude=2.3522,
    zoom=4,
)

kuala_lumpur_view = pdk.ViewState(
    latitude=3.1390,
    longitude=101.6869,
    zoom=5,
)

# Layers for the markers
paris_layer = pdk.Layer(
    "ScatterplotLayer",
    data=paris_coords,
    get_position='[lon, lat]',
    get_radius=5000,
    get_color=[255, 0, 0, 200],
    pickable=True
)

kuala_lumpur_layer = pdk.Layer(
    "ScatterplotLayer",
    data=kuala_lumpur_coords,
    get_position='[lon, lat]',
    get_radius=5000,
    get_color=[0, 0, 255, 200],
    pickable=True
)

# Displaying the maps side by side
col1, col2 = st.columns(2)
with col1:
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/streets-v11",  # Style de carte coloré
        initial_view_state=paris_view,
        layers=[paris_layer],
    ))
    st.subheader("Paris, France (EFREI)")

with col2:
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/streets-v11",  # Style de carte coloré
        initial_view_state=kuala_lumpur_view,
        layers=[kuala_lumpur_layer],
    ))
    st.subheader("Kuala Lumpur, Malaysia (Exchange Program)")

# Horizontal separator
st.markdown("<hr>", unsafe_allow_html=True)

# Contact Section
st.header("📞 Contact")
st.write("📧 contact@kevin-kurtz.fr &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 📞 +33 6 62 75 72 77 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 📍 Paris, France")

# Contact Form
st.subheader("Contact Form")
name = st.text_input("Name")
email = st.text_input("Email")
message = st.text_area("Message")
if st.button("Send"):
    st.write("Thank you for your message, I will get back to you soon.")
