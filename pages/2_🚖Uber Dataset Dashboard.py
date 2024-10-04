"""
**@author : Kevin KURTZ**
**@contact : contact@kevin-kurtz.fr**
"""


# --------------------------- Import libraries --------------------------- #
import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go


# --------------------------- Page Configuration ---------------------------- #
st.set_page_config(
    page_title="🚖 Uber Data Analysis - Dashboard",
    page_icon="🚖",
    layout="wide"
)


# ------------------------------ Load Data ----------------------------------- #
DATA_URL = "https://raw.githubusercontent.com/uber-web/kepler.gl-data/master/nyctrips/data.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    df['hour_pickup'] = df['tpep_pickup_datetime'].dt.hour
    df['hour_dropoff'] = df['tpep_dropoff_datetime'].dt.hour  # Corrigé pour dropoff
    df['day_pickup'] = df['tpep_pickup_datetime'].dt.day_name()
    df['trip_distance'] = pd.to_numeric(df['trip_distance'], errors='coerce')
    df['fare_amount'] = pd.to_numeric(df['fare_amount'], errors='coerce')
    return df

df = load_data()


# ---------------------------- Sidebar -------------------------------------- #
with st.sidebar:
    # Section: Information & Data Source
    st.header("📄 Information & Sources")
    st.markdown("""
    - **Data Source**: [Uber NYC Trip Data](https://github.com/uber-web/kepler.gl-data)
    """)
    st.markdown('---')
    
    # Section: Map Controls
    st.subheader("🌍 Arc Map Controls")
    pitch_value = st.slider("🔃 Adjust Map Pitch", min_value=0, max_value=85, value=20, step=1)
    bearing_value = st.slider("🔄 Adjust Map Rotation", min_value=0, max_value=360, value=0, step=1)

    st.markdown("<br><br><br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown('---')
    st.write('For more information, visit my [GitHub](https://github.com/ktzkvin/GHG-Emissions-Dashboard/tree/main)')


# ---------------------------- Introduction ---------------------------------- #
st.title("🚖 Uber Data Analysis Dashboard")
st.markdown("""
Welcome to the Uber Data Analysis dashboard! In this app, we will explore **Uber trips** in **New York City** with a focus on time, location and fare distribution. 🎉
""")


# ---------------------------- Analysis by Hour ----------------------------- #
st.header("📊 Ride Distribution by Hour")
st.markdown("""
In this section, let's take a look at the **distribution of pickups and dropoffs by hour** to identify the busiest times for Uber trips. 
""")

# Grouping data by hour to make sure all hours are represented
hours = list(range(24))

# Correctly extracting pickup and dropoff counts
pickup_counts = df['hour_pickup'].value_counts().reindex(hours, fill_value=0).sort_index()
dropoff_counts = df['hour_dropoff'].value_counts().reindex(hours, fill_value=0).sort_index()

# Superposed bar charts for pickups and dropoffs
fig = go.Figure()

# Pickup trace
fig.add_trace(go.Bar(
    x=pickup_counts.index,
    y=pickup_counts.values,
    name='Pickups 🚕',
    marker=dict(color='lightblue'),
    opacity=0.6,
    width=0.35
))

# Dropoff trace
fig.add_trace(go.Bar(
    x=dropoff_counts.index,
    y=dropoff_counts.values,
    name='Dropoffs 🏁',
    marker=dict(color='lightgreen'),
    opacity=0.6,
    width=0.35
))

fig.update_layout(
    title="🚖 Distribution of Pickups and Dropoffs by Hour",
    xaxis_title="Hour of the Day",
    yaxis_title="Number of Trips",
    xaxis=dict(tickmode='linear', tick0=0, dtick=1),
    barmode='overlay',
    bargap=0.15,
    bargroupgap=0.1,
    template='plotly_dark',
)

st.plotly_chart(fig)


# -------------------- Scatter Plots: Distance vs Price ---------------------- #
st.header("💰 Distance vs Fare Analysis")
st.markdown("""
Let's dive into the relationship between **trip distance** and **fare price** to understand pricing trends for Uber rides.
""")

# Scatter plot for fare amount vs trip distance (without tip)
fig_scatter1 = px.scatter(df, x='trip_distance', y='fare_amount', 
                          title="Fare vs Distance (Without Tip) 🚕💵",
                          labels={'trip_distance': 'Trip Distance (miles)', 'fare_amount': 'Fare ($)'},
                          template="plotly_dark",
                          color_discrete_sequence=['#FFA07A'])

# Scatter plot for total amount vs trip distance (with tip)
fig_scatter2 = px.scatter(df, x='trip_distance', y='total_amount', 
                          title="Total Fare vs Distance (With Tip) 🚕💵",
                          labels={'trip_distance': 'Trip Distance (miles)', 'total_amount': 'Total Fare ($)'},
                          template="plotly_dark",
                          color_discrete_sequence=['#00FA9A'])

# Display both scatter plots side by side
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_scatter1)
with col2:
    st.plotly_chart(fig_scatter2)


# ------------------------ Geographic Data Visualization --------------------- #
st.header("🌍 Uber Trip Locations")
st.markdown("""
Let's explore the **geographic distribution** of Uber pickups and dropoffs. You can toggle between the **Pickup Locations**, **Dropoff Locations**, and the **Arc Layer Map** to visualize the routes.
""")

# Tabs to switch between Pickup, Dropoff and Arc Map views
tab1, tab2, tab3 = st.tabs(["Pickup Locations", "Dropoff Locations", "Arc Layer Map"])

# For Pickup locations
with tab1:
    st.subheader("📍 Pickup Locations - Hexagon Map")
    pickup_layer = pdk.Layer(
        "HexagonLayer",
        data=df[['pickup_latitude', 'pickup_longitude']],
        get_position=['pickup_longitude', 'pickup_latitude'],
        radius=5,
        elevation_scale=2,
        elevation_range=[0, 1000],
        pickable=True,
        extruded=True,
    )

    pickup_view_state = pdk.ViewState(
        latitude=df['pickup_latitude'].mean(),
        longitude=df['pickup_longitude'].mean(),
        zoom=12,
        pitch=20,
    )

    pickup_map = pdk.Deck(
        layers=[pickup_layer],
        initial_view_state=pickup_view_state,
    )
    st.pydeck_chart(pickup_map, height=750)

# For Dropoff locations
with tab2:
    st.subheader("🏁 Dropoff Locations - Hexagon Map")
    dropoff_layer = pdk.Layer(
        "HexagonLayer",
        data=df[['dropoff_latitude', 'dropoff_longitude']],
        get_position=['dropoff_longitude', 'dropoff_latitude'],
        radius=5,
        elevation_scale=2,
        elevation_range=[0, 1000],
        pickable=True,
        extruded=True,
    )

    dropoff_view_state = pdk.ViewState(
        latitude=df['dropoff_latitude'].mean(),
        longitude=df['dropoff_longitude'].mean(),
        zoom=12,
        pitch=20,
    )

    dropoff_map = pdk.Deck(
        layers=[dropoff_layer],
        initial_view_state=dropoff_view_state,
    )
    st.pydeck_chart(dropoff_map, height=750)

# Arc Layer for Pickup and Dropoff locations
with tab3:
    st.subheader("🛣️ Arc Layer Map - Visualizing Routes between Pickup and Dropoff Points")
    st.markdown("""
    The **Arc Layer Map** provides a visual connection between Uber pickup and dropoff points, allowing us to see the flow of trips across New York City.
    """)

    arc_layer = pdk.Layer(
        "ArcLayer",
        data=df[['pickup_latitude', 'pickup_longitude', 'dropoff_latitude', 'dropoff_longitude']],
        get_source_position=['pickup_longitude', 'pickup_latitude'],
        get_target_position=['dropoff_longitude', 'dropoff_latitude'],
        get_source_color=[0, 128, 255],
        get_target_color=[255, 0, 0],
        auto_highlight=True,
        width_scale=0.01,
        get_width=3,
        pickable=True,
    )

    # View state for the Arc Layer Map
    arc_view_state = pdk.ViewState(
        latitude=df['pickup_latitude'].mean(),
        longitude=df['pickup_longitude'].mean(),
        zoom=10,
        pitch=pitch_value,
        bearing=bearing_value

    )

    # Create the map with ArcLayer
    arc_map = pdk.Deck(
        layers=[arc_layer],
        initial_view_state=arc_view_state,
        tooltip={"text": "Pickup: {pickup_latitude}, {pickup_longitude}\nDropoff: {dropoff_latitude}, {dropoff_longitude}"}
    )

    # Render
    st.pydeck_chart(arc_map, height=750)
