"""
**@author : Kevin KURTZ**
**@email : contact@kevin-kurtz.fr**
"""

# -------------------------- import libraries -------------------------- #
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io
import zipfile


# ------------------------------ Load data ------------------------------ #
data_emissions = pd.read_csv('csv-data/emissions_ges_france.csv')
data_dep = pd.read_csv('csv-data/communes-departement-region.csv')


# --------------------------- Set page config --------------------------- #
st.set_page_config(
    page_title="GHG Emissions - Dashboard",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ------------------------ Clean emissions data ------------------------- #

# Clone the 'Commune' column for display purposes (commune name with proper formatting)
data_emissions['Commune_LF'] = data_emissions['Commune']
data_emissions['Commune_LF'] = data_emissions['Commune_LF'].str.title()

data_emissions['Commune'] = data_emissions['Commune'].str.replace('-', '').str.replace(' ', '').str.replace('\'', '')
data_emissions['Commune'] = data_emissions['Commune'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

# Merge the arrondissements of Paris, Lyon, and Marseille into single entries
data_emissions = data_emissions.replace({
    'PARIS1ERARRONDISSEMENT': 'PARIS', 'PARIS2EARRONDISSEMENT': 'PARIS', 'PARIS3EARRONDISSEMENT': 'PARIS', 
    'PARIS4EARRONDISSEMENT': 'PARIS', 'PARIS5EARRONDISSEMENT': 'PARIS', 'PARIS6EARRONDISSEMENT': 'PARIS', 
    'PARIS7EARRONDISSEMENT': 'PARIS', 'PARIS8EARRONDISSEMENT': 'PARIS', 'PARIS9EARRONDISSEMENT': 'PARIS', 
    'PARIS10EARRONDISSEMENT': 'PARIS', 'PARIS11EARRONDISSEMENT': 'PARIS', 'PARIS12EARRONDISSEMENT': 'PARIS', 
    'PARIS13EARRONDISSEMENT': 'PARIS', 'PARIS14EARRONDISSEMENT': 'PARIS', 'PARIS15EARRONDISSEMENT': 'PARIS', 
    'PARIS16EARRONDISSEMENT': 'PARIS', 'PARIS17EARRONDISSEMENT': 'PARIS', 'PARIS18EARRONDISSEMENT': 'PARIS', 
    'PARIS19EARRONDISSEMENT': 'PARIS', 'PARIS20EARRONDISSEMENT': 'PARIS',
    
    'LYON1ERARRONDISSEMENT': 'LYON', 'LYON2EARRONDISSEMENT': 'LYON', 'LYON3EARRONDISSEMENT': 'LYON',
    'LYON4EARRONDISSEMENT': 'LYON', 'LYON5EARRONDISSEMENT': 'LYON', 'LYON6EARRONDISSEMENT': 'LYON',
    'LYON7EARRONDISSEMENT': 'LYON', 'LYON8EARRONDISSEMENT': 'LYON', 'LYON9EARRONDISSEMENT': 'LYON',
    
    'MARSEILLE1ERARRONDISSEMENT': 'MARSEILLE', 'MARSEILLE2EARRONDISSEMENT': 'MARSEILLE', 
    'MARSEILLE3EARRONDISSEMENT': 'MARSEILLE', 'MARSEILLE4EARRONDISSEMENT': 'MARSEILLE', 
    'MARSEILLE5EARRONDISSEMENT': 'MARSEILLE', 'MARSEILLE6EARRONDISSEMENT': 'MARSEILLE', 
    'MARSEILLE7EARRONDISSEMENT': 'MARSEILLE', 'MARSEILLE8EARRONDISSEMENT': 'MARSEILLE', 
    'MARSEILLE9EARRONDISSEMENT': 'MARSEILLE', 'MARSEILLE10EARRONDISSEMENT': 'MARSEILLE', 
    'MARSEILLE11EARRONDISSEMENT': 'MARSEILLE', 'MARSEILLE12EARRONDISSEMENT': 'MARSEILLE', 
    'MARSEILLE13EARRONDISSEMENT': 'MARSEILLE', 'MARSEILLE14EARRONDISSEMENT': 'MARSEILLE', 
    'MARSEILLE15EARRONDISSEMENT': 'MARSEILLE', 'MARSEILLE16EARRONDISSEMENT': 'MARSEILLE'
})

# Separate the data for Paris, Lyon, Marseille and group their arrondissements
paris_data = data_emissions[data_emissions['Commune'] == 'PARIS']
lyon_data = data_emissions[data_emissions['Commune'] == 'LYON']
marseille_data = data_emissions[data_emissions['Commune'] == 'MARSEILLE']

other_data = data_emissions[(data_emissions['Commune'] != 'PARIS') & (data_emissions['Commune'] != 'LYON') & (data_emissions['Commune'] != 'MARSEILLE')]

# Aggregate the data for Paris, Lyon, and Marseille
paris_grouped = paris_data.groupby('Commune').agg({
    'Agriculture': 'sum', 
    'Autres transports': 'sum', 
    'Autres transports international': 'sum', 
    'CO2 biomasse hors-total': 'sum', 
    'Déchets': 'sum', 
    'Energie': 'sum', 
    'Industrie hors-énergie': 'sum', 
    'Résidentiel': 'sum', 
    'Routier': 'sum', 
    'Tertiaire': 'sum'
}).reset_index()
paris_grouped['Commune_LF'] = 'Paris'

lyon_grouped = lyon_data.groupby('Commune').agg({
    'Agriculture': 'sum', 
    'Autres transports': 'sum', 
    'Autres transports international': 'sum', 
    'CO2 biomasse hors-total': 'sum', 
    'Déchets': 'sum', 
    'Energie': 'sum', 
    'Industrie hors-énergie': 'sum', 
    'Résidentiel': 'sum', 
    'Routier': 'sum', 
    'Tertiaire': 'sum'
}).reset_index()
lyon_grouped['Commune_LF'] = 'Lyon'

marseille_grouped = marseille_data.groupby('Commune').agg({
    'Agriculture': 'sum', 
    'Autres transports': 'sum', 
    'Autres transports international': 'sum', 
    'CO2 biomasse hors-total': 'sum', 
    'Déchets': 'sum', 
    'Energie': 'sum', 
    'Industrie hors-énergie': 'sum', 
    'Résidentiel': 'sum', 
    'Routier': 'sum', 
    'Tertiaire': 'sum'
}).reset_index()
marseille_grouped['Commune_LF'] = 'Marseille'

# Concatenate with other communes
data_emissions = pd.concat([other_data, paris_grouped, lyon_grouped, marseille_grouped], ignore_index=True)


# --------------------------- Clean temp data ---------------------------- #
data_dep = data_dep[['nom_commune_complet', 'nom_departement']]
data_dep = data_dep.rename(columns={'nom_departement': 'Département', 'nom_commune_complet': 'Commune'})
data_dep['Commune'] = data_dep['Commune'].str.upper()
data_dep['Commune'] = data_dep['Commune'].str.replace('-', '').str.replace(' ', '').str.replace('\'', '').str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

# Remove duplicates
data_dep = data_dep.replace({'PARIS01': 'PARIS', 'PARIS02': 'PARIS', 'PARIS03': 'PARIS', 'PARIS04': 'PARIS', 'PARIS05': 'PARIS', 'PARIS06': 'PARIS', 'PARIS07': 'PARIS', 'PARIS08': 'PARIS', 'PARIS09': 'PARIS', 'PARIS10': 'PARIS', 'PARIS11': 'PARIS', 'PARIS12': 'PARIS', 'PARIS13': 'PARIS', 'PARIS14': 'PARIS', 'PARIS15': 'PARIS', 'PARIS16': 'PARIS', 'PARIS17': 'PARIS', 'PARIS18': 'PARIS', 'PARIS19': 'PARIS', 'PARIS20': 'PARIS'})
data_dep = data_dep.drop_duplicates(subset='Commune')


# ---------------------------- Merge all data ---------------------------- #
data_merged = pd.merge(data_emissions, data_dep, on='Commune', how='left')

# Arrange columns
cols = data_merged.columns.tolist()
cols = cols[:2] + [cols[-1]] + cols[2:-1]
data_merged = data_merged[cols]
cols = data_merged.columns.tolist()
cols = cols[:1] + [cols[13]] + cols[1:13] + cols[14:]
data_merged = data_merged[cols]

# Create a total column, and convert all columns to numeric
data_merged[['Agriculture', 'Autres transports', 'Autres transports international', 'CO2 biomasse hors-total', 'Déchets', 'Energie', 'Industrie hors-énergie', 'Résidentiel', 'Routier', 'Tertiaire']] = data_merged[['Agriculture', 'Autres transports', 'Autres transports international', 'CO2 biomasse hors-total', 'Déchets', 'Energie', 'Industrie hors-énergie', 'Résidentiel', 'Routier', 'Tertiaire']].apply(pd.to_numeric, errors='coerce')
data_merged['Total'] = data_merged[['Agriculture', 'Autres transports', 'Autres transports international', 'CO2 biomasse hors-total', 'Déchets', 'Energie', 'Industrie hors-énergie', 'Résidentiel', 'Routier', 'Tertiaire']].sum(axis=1)

# Add the correct 'Département' for Paris, Lyon, and Marseille
data_merged.loc[data_merged['Commune'] == 'PARIS', 'Département'] = 'Paris'
data_merged.loc[data_merged['Commune'] == 'LYON', 'Département'] = 'Rhône'
data_merged.loc[data_merged['Commune'] == 'MARSEILLE', 'Département'] = 'Bouches-du-Rhône'

# Add the correct 'INSEE commune' code for Paris, Lyon, and Marseille
data_merged.loc[data_merged['Commune'] == 'PARIS', 'INSEE commune'] = '75056'
data_merged.loc[data_merged['Commune'] == 'LYON', 'INSEE commune'] = '69385'
data_merged.loc[data_merged['Commune'] == 'MARSEILLE', 'INSEE commune'] = '13055'

# ------------------------------ Functions ------------------------------- #

def france_heatmap():
    url_geojson = 'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson'
    response = requests.get(url_geojson)
    geojson_departements = response.json()

    data_by_departement = data_merged.groupby('Département').agg({'Total': 'sum'}).reset_index()

    fig_map = px.choropleth_mapbox(
        data_by_departement, 
        geojson=geojson_departements, 
        locations='Département', 
        featureidkey='properties.nom',
        color='Total',
        color_continuous_scale="Viridis",
        range_color=(0, data_by_departement['Total'].max()),
        mapbox_style="carto-darkmatter",
        zoom=4.5,
        center={"lat": 46.603354, "lon": 1.888334},
        opacity=0.5,
        labels={'Total': 'Tonne of CO₂eq'}
    )

    st.write("")
    fig_map.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig_map, use_container_width=True)


# ------------------------------ Sidebar -------------------------------- #
with st.sidebar:
    st.title('🛠️ Dashboard Controls')

    # Add a slider for selecting the unit
    equivalents_factors = {
        '☁ Tonnes of CO₂eq': 1,
        '🚗 Km driven in a gasoline car': 4_596,
        '✈️ Km flown in a plane': 4_348,
        '🚄 Km traveled by TGV': 423_729,
        '📱 Smartphones produced': 32,
        '👖 Jeans produced': 42,
        '🍔 Beef burgers consumed': 167,
        '📺 Hours of video streaming': 15_621,
        '💡 Years of electric heating': 1.5,
    }

    selected_unit = st.selectbox('Select unit for CO₂eq', options=list(equivalents_factors.keys()), index=0)
    unit_factor = equivalents_factors[selected_unit]

    with st.expander('📖 Glossary', expanded=False):
        st.info('''
        **🌍 CO₂ Equivalent (CO₂eq)**: Compares emissions from different greenhouse gases based on their global warming potential.

        **🛢️ Tonnes of CO₂eq**: One metric tonne (1,000 kg) of CO₂ or equivalent amount of other greenhouse gases.

        **📌 Sectors**:

        - **🌾 Agriculture**: Emissions from farming activities.
        - **🚗 Transport**: Emissions from vehicles, planes, ships.
        - **🏭 Industry**: Emissions from industrial processes.
        - **🏠 Residential**: Emissions from household energy use.
        - **🏢 Tertiary**: Emissions from service industries.
        - **⚡ Energy**: Emissions from energy production/consumption.
        - **♻️ Waste**: Emissions from waste management.
        - **🛣️ Road**: Emissions specifically from road transport.
        ''')



    # Data download section remains the same
    st.markdown('---')
    st.write('For more information, visit my [GitHub](https://github.com/ktzkvin/GHG-Emissions-Dashboard/tree/main)')


# ------------------------------ Main page ------------------------------- #
st.title('🏭 Greenhouse Gas Emissions in France')
st.markdown('---')

# 3 Columns as before
col = st.columns((1.8, 4.2, 2), gap='medium')

# TOP 10 and WORST DEPARTMENTS as before, with unified titles and opened expanders
with col[0]:
    with st.expander('🏆 Top 10 Polluting Departments', expanded=True):
        data_by_departement = data_merged.groupby('Département').agg({'Total': 'sum'}).reset_index()
        top_departements = data_by_departement.nlargest(9, 'Total')
        fig_top_pie = px.pie(
            top_departements, 
            names='Département', 
            values='Total', 
            title='Top 10 Most Polluting Departments',
            labels={'Département': '', 'Total': ''},  
            color_discrete_sequence=px.colors.sequential.Reds_r
        )
        fig_top_pie.update_traces(textinfo='label+percent', textposition='inside', insidetextorientation='radial')
        fig_top_pie.update_layout(showlegend=False, margin=dict(t=50, b=30, l=0, r=0), height=300, width=300)
        st.plotly_chart(fig_top_pie, use_container_width=True)
    
    st.markdown('---')
    
    with st.expander('🌍 Top 10 Least Polluting Departments', expanded=True):
        bottom_departements = data_by_departement.nsmallest(9, 'Total')
        fig_bottom_pie = px.pie(
            bottom_departements, 
            names='Département', 
            values='Total', 
            title='Top 10 Least Polluting Departments',
            labels={'Département': '', 'Total': ''},  
            color_discrete_sequence=px.colors.sequential.YlGn
        )
        fig_bottom_pie.update_traces(textinfo='label+percent', textposition='inside', insidetextorientation='radial')
        fig_bottom_pie.update_layout(showlegend=False, margin=dict(t=50, b=30, l=0, r=0), height=300, width=300)
        st.plotly_chart(fig_bottom_pie, use_container_width=True)

# MAP and sector breakdown (Use Tabs here to add more interaction)
with col[1]:
    st.markdown('#### 📍 Map of France with Emissions by Department')
    
    # Use Tabs to switch between Map and Breakdown
    tabs = st.tabs(["France Map", "Sector Breakdown"])

    with tabs[0]:
        france_heatmap()

    with tabs[1]:
        st.markdown('#### 📊 Emissions by Sector')
        data_by_sector = data_merged[['Agriculture', 'Autres transports', 'Déchets', 'Energie', 'Industrie hors-énergie', 'Résidentiel', 'Routier', 'Tertiaire']].sum().reset_index()
        data_by_sector['index'] = ['Agriculture', 'Other transports', 'Waste', 'Energy', 'Industry excluding energy', 'Residential', 'Road', 'Tertiary']
        data_by_sector.columns = ['Secteur', 'Emissions']
        fig_bar = px.bar(
            data_by_sector, 
            x='Secteur', 
            y='Emissions', 
            labels={'Emissions': 'Tonne of CO₂eq', 'Secteur': 'Sector'}, 
            color='Emissions', 
            color_continuous_scale='RdYlGn_r'
        )
        fig_bar.update_layout(showlegend=False, margin=dict(t=30, b=30, l=0, r=0), height=400)
        st.plotly_chart(fig_bar, use_container_width=True)

# TOP COMMUNES section (Show all communes)
with col[2]:
    st.markdown('#### 🥇 Top Communes')
    st.write("")

    # Show all communes sorted by total emissions
    data_merged_sorted = data_merged.sort_values(by='Total', ascending=False).copy()
    data_merged_sorted['Total_converted'] = data_merged_sorted['Total'] * unit_factor
    max_total_converted = data_merged['Total'].max() * unit_factor

    st.dataframe(
        data_merged_sorted[['Commune_LF', 'Total_converted']],
        hide_index=True,
        column_config={
            'Commune_LF': st.column_config.TextColumn('Commune'),
            'Total_converted': st.column_config.ProgressColumn(
                selected_unit,
                format='%.2f',
                min_value=0,
                max_value=max_total_converted
            )
        },
        width=800
    )

    # Add Expander with extra analysis details
    with st.expander('🔍 Explore More Details', expanded=False):
        st.write('''
        - Data source: [Inventaire de gaz a effet de serre territorialisé](https://www.data.gouv.fr/fr/datasets/inventaire-de-gaz-a-effet-de-serre-territorialise/)  (Data Gouv)
        - Note: The data is from **2016** and may change in future years.
        ''')

st.markdown("### Compare Departments")
selected_departments = st.multiselect(
    "Select two departments to compare their emissions",
    options=data_merged['Département'].unique(),
    default=['Paris', 'Rhône']
)

comparison_data = data_merged[data_merged['Département'].isin(selected_departments)]
fig_comparison = px.bar(comparison_data, x='Département', y='Total', color='Département', title="GHG Emissions Comparison")
st.plotly_chart(fig_comparison, use_container_width=True)
