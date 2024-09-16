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


# -------------------------- Load data -------------------------- #
data_emissions = pd.read_csv('csv-data/emissions_ges_france.csv')
data_coordinates = pd.read_csv('csv-data/communes_coordinates.csv', sep='|')
data_dep = pd.read_csv('csv-data/communes-departement-region.csv')


# -------------------------- Set page config -------------------------- #
st.set_page_config(
    page_title="GHG Emissions - Dashboard",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------- Clean emissions data -------------------------- #
data_emissions['Commune_LF'] = data_emissions['Commune']  # Clone
data_emissions['Commune_LF'] = data_emissions['Commune_LF'].str.title()
data_emissions['Commune'] = data_emissions['Commune'].str.replace('-', '').str.replace(' ', '').str.replace('\'', '').str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

# Remove duplicates of Paris + we need to add all the emissions of all districts
data_emissions = data_emissions.replace({'PARIS1ERARRONDISSEMENT': 'PARIS', 'PARIS2EARRONDISSEMENT': 'PARIS', 'PARIS3EARRONDISSEMENT': 'PARIS', 'PARIS4EARRONDISSEMENT': 'PARIS', 'PARIS5EARRONDISSEMENT': 'PARIS', 'PARIS6EARRONDISSEMENT': 'PARIS', 'PARIS7EARRONDISSEMENT': 'PARIS', 'PARIS8EARRONDISSEMENT': 'PARIS', 'PARIS9EARRONDISSEMENT': 'PARIS', 'PARIS10EARRONDISSEMENT': 'PARIS', 'PARIS11EARRONDISSEMENT': 'PARIS', 'PARIS12EARRONDISSEMENT': 'PARIS', 'PARIS13EARRONDISSEMENT': 'PARIS', 'PARIS14EARRONDISSEMENT': 'PARIS', 'PARIS15EARRONDISSEMENT': 'PARIS', 'PARIS16EARRONDISSEMENT': 'PARIS', 'PARIS17EARRONDISSEMENT': 'PARIS', 'PARIS18EARRONDISSEMENT': 'PARIS', 'PARIS19EARRONDISSEMENT': 'PARIS', 'PARIS20EARRONDISSEMENT': 'PARIS'})

# Regroup data for Paris
paris_data = data_emissions[data_emissions['Commune'] == 'PARIS']
other_data = data_emissions[data_emissions['Commune'] != 'PARIS']

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

# Concatenate data
data_emissions = pd.concat([other_data, paris_grouped], ignore_index=True)


# ---------------------------- Clean temp data ----------------------------- #
data_dep = data_dep[['nom_commune_complet', 'nom_departement']]
data_dep = data_dep.rename(columns={'nom_departement': 'Département', 'nom_commune_complet': 'Commune'})
data_dep['Commune'] = data_dep['Commune'].str.upper()
data_dep['Commune'] = data_dep['Commune'].str.replace('-', '').str.replace(' ', '').str.replace('\'', '').str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

# Remove duplicates
data_dep = data_dep.replace({'PARIS01': 'PARIS', 'PARIS02': 'PARIS', 'PARIS03': 'PARIS', 'PARIS04': 'PARIS', 'PARIS05': 'PARIS', 'PARIS06': 'PARIS', 'PARIS07': 'PARIS', 'PARIS08': 'PARIS', 'PARIS09': 'PARIS', 'PARIS10': 'PARIS', 'PARIS11': 'PARIS', 'PARIS12': 'PARIS', 'PARIS13': 'PARIS', 'PARIS14': 'PARIS', 'PARIS15': 'PARIS', 'PARIS16': 'PARIS', 'PARIS17': 'PARIS', 'PARIS18': 'PARIS', 'PARIS19': 'PARIS', 'PARIS20': 'PARIS'})
data_dep = data_dep.drop_duplicates(subset='Commune')


# ------------------------- Clean coordinates data ------------------------- #
data_coordinates['Commune'] = data_coordinates['Commune'].str.upper()
data_coordinates['Commune'] = data_coordinates['Commune'].str.replace('-', '').str.replace(' ', '').str.replace('\'', '').str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
data_coordinates = data_coordinates.drop(columns=['id'])


# ---------------------------- Merge all data ----------------------------- #
data_merged = pd.merge(data_emissions, data_coordinates, on='Commune', how='left')
data_merged = pd.merge(data_merged, data_dep, on='Commune', how='left')

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


# ---------------------------- Functions ----------------------------- #

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



# ---------------------------- Sidebar ----------------------------- #
with st.sidebar:
    st.title('🛠️ Contrôles du Tableau de Bord')

    # Sélection de l'unité
    st.markdown('## ☁ CO₂ Equivalent')

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

    # Glossary Section
    st.markdown('## 📖 Glossary')
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

    # Download Data Section
    csv_emissions = data_emissions.to_csv(index=False)
    csv_coordinates = data_coordinates.to_csv(index=False)
    csv_dep = data_dep.to_csv(index=False)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        zip_file.writestr('emissions_ges_france.csv', csv_emissions)
        zip_file.writestr('communes_coordinates.csv', csv_coordinates)
        zip_file.writestr('communes-departement-region.csv', csv_dep)
    zip_buffer.seek(0)

    # Create a download button for the ZIP file
    st.download_button(
        label='Download Data Files (ZIP)',
        data=zip_buffer,
        file_name='data_files.zip',
        mime='application/zip'
    )

    st.markdown('---')
    st.write('For more information, visit my [GitHub](https://github.com/ktzkvin/GHG-Emissions-Dashboard/tree/main)')


# ---------------------------- Main page ----------------------------- #
st.title('🏭 Greenhouse Gas Emissions in France')
st.markdown('---')

# Columns
col = st.columns((1.8, 4.2, 2), gap='medium')  

data_by_departement = data_merged.groupby('Département').agg({'Total': 'sum'}).reset_index()
top_departements = data_by_departement.nlargest(9, 'Total')
fig_top_pie = px.pie(
    top_departements, 
    names='Département', 
    values='Total', 
    title='Worst Departments (+ Pollutants)',
    labels={'Département': '', 'Total': ''},  
    color_discrete_sequence=px.colors.sequential.Reds_r
)

bottom_departements = data_by_departement.nsmallest(9, 'Total')
fig_bottom_pie = px.pie(
    bottom_departements, 
    names='Département', 
    values='Total', 
    title='Best Departments (- Pollutants)',
    labels={'Département': '', 'Total': ''},  
    color_discrete_sequence=px.colors.sequential.YlGn
)

fig_top_pie.update_traces(textinfo='label+percent', textposition='inside', insidetextorientation='radial')
fig_top_pie.update_layout(showlegend=False, margin=dict(t=50, b=30, l=0, r=0), height=300, width=300)

fig_bottom_pie.update_traces(textinfo='label+percent', textposition='inside', insidetextorientation='radial')
fig_bottom_pie.update_layout(showlegend=False, margin=dict(t=50, b=30, l=0, r=0), height=300, width=300)


with col[0]:
    st.markdown('#### 🏆 Top 10', unsafe_allow_html=True)
    st.write("")
    st.plotly_chart(fig_top_pie, use_container_width=True)
    st.markdown('---')
    st.plotly_chart(fig_bottom_pie, use_container_width=True)


with col[1]:
    st.markdown('#### 🌍 Map of France with Emissions by Department')
    france_heatmap()

    st.markdown('---')

    st.markdown('#### 📊 Emissions by Sector in France')
    
    # Data by sector
    data_by_sector = data_merged[['Agriculture', 'Autres transports', 'Déchets', 'Energie', 'Industrie hors-énergie', 'Résidentiel', 'Routier', 'Tertiaire']].sum().reset_index()
    data_by_sector['index'] = ['Agriculture', 'Other transports', 'Waste', 'Energy', 'Industry excluding energy', 'Residential', 'Road', 'Tertiary']
    data_by_sector.columns = ['Secteur', 'Emissions']
    
    # Bar chart
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



with col[2]:
    st.markdown('#### 🥇 Top Communes')
    st.write("")
    data_merged_sorted = data_merged.sort_values(by='Total', ascending=False).copy()

    #
    data_merged_sorted['Total_converted'] = data_merged_sorted['Total'] * unit_factor
    max_total_converted = data_merged['Total'].max() * unit_factor

    st.dataframe(
        data_merged_sorted,
        hide_index=True,
        column_order=['Commune_LF', 'Total_converted'],
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
    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander('🔍 Details', expanded=True):
        st.write('''
        - Data source: [Inventaire de gaz a effet de serre territorialisé](https://www.data.gouv.fr/fr/datasets/inventaire-de-gaz-a-effet-de-serre-territorialise/)  (Data Gouv)
        - :orange[**Note**]: The data is from **2016** and is subject to change.
        ''')
        st.caption('Conversion factors based on [Alterna Énergie](https://www.alterna-energie.fr/blog-article/1-tonne-de-co2-equivalent-comprendre-cet-indice#:~:text=Le%20terme%20%E2%80%9CCO%E2%82%82%20%C3%A9quivalent%E2%80%9D%20(,%2C%20protoxyde%20d\'azote%E2%80%A6)).')
