"""
**@author : Kevin KURTZ**
**@email : kevin.kurtz@efrei.net**
"""

# import libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import requests  # Pour charger le GeoJSON depuis une URL

# Load data
data_emissions = pd.read_csv('emissions_ges_france.csv')
data_coordinates = pd.read_csv('communes_coordinates.csv', sep='|')
dep_data = pd.read_csv('communes-departement-region.csv')

# Set page config
st.set_page_config(
    page_title="GHG Emissions - Dashboard",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded")

# -------------------------- Clean emissions data -------------------------- #
data_emissions['Commune_format'] = data_emissions['Commune']  # Clone
data_emissions['Commune_format'] = data_emissions['Commune_format'].str.title()
data_emissions['Commune'] = data_emissions['Commune'].str.replace('-', '').str.replace(' ', '').str.replace('\'', '').str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

# ---------------------------- Clean temp data ----------------------------- #
dep_data = dep_data[['nom_commune_complet', 'nom_departement']]  # Keep only the columns we need
dep_data = dep_data.rename(columns={'nom_departement': 'Département', 'nom_commune_complet': 'Commune'})
dep_data['Commune'] = dep_data['Commune'].str.upper()
dep_data['Commune'] = dep_data['Commune'].str.replace('-', '').str.replace(' ', '').str.replace('\'', '').str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
dep_data = dep_data.drop_duplicates(subset='Commune')

# ------------------------- Clean coordinates data ------------------------- #
data_coordinates['Commune'] = data_coordinates['Commune'].str.upper()
data_coordinates['Commune'] = data_coordinates['Commune'].str.replace('-', '').str.replace(' ', '').str.replace('\'', '').str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
data_coordinates = data_coordinates.drop(columns=['id'])

# ---------------------------- Merge all data ----------------------------- #
data_merged = pd.merge(data_emissions, data_coordinates, on='Commune', how='left')
data_merged = pd.merge(data_merged, dep_data, on='Commune', how='left')


# Arrange columns
cols = data_merged.columns.tolist()
cols = cols[:2] + [cols[-1]] + cols[2:-1]
data_merged = data_merged[cols]
cols = data_merged.columns.tolist()
cols = cols[:1] + [cols[13]] + cols[1:13] + cols[14:]
data_merged = data_merged[cols]
data_merged = data_merged.rename(columns={'Commune_format': 'Commune_LF'})

# Create a total column, and convert all columns to numeric
data_merged[['Agriculture', 'Autres transports', 'Autres transports international', 'CO2 biomasse hors-total', 'Déchets', 'Energie', 'Industrie hors-énergie', 'Résidentiel', 'Routier', 'Tertiaire']] = data_merged[['Agriculture', 'Autres transports', 'Autres transports international', 'CO2 biomasse hors-total', 'Déchets', 'Energie', 'Industrie hors-énergie', 'Résidentiel', 'Routier', 'Tertiaire']].apply(pd.to_numeric, errors='coerce')
data_merged['Total'] = data_merged[['Agriculture', 'Autres transports', 'Autres transports international', 'CO2 biomasse hors-total', 'Déchets', 'Energie', 'Industrie hors-énergie', 'Résidentiel', 'Routier', 'Tertiaire']].sum(axis=1)


# ---------------------------- Sidebar ----------------------------- #
with st.sidebar:
    st.title('🏭 Greenhouse Gas Emissions in France')


# ---------------------------- Main page ----------------------------- #
st.title('🏭 Greenhouse Gas Emissions in France')

# Columns
col = st.columns((1.5, 4.5, 2), gap='medium')  
with col[0]:
    st.write('a')

with col[1]:
    st.write('b')

with col[2]:
    st.markdown('#### 🥇 Top Communes')
 
    data_merged_sorted = data_merged.sort_values(by='Total', ascending=False)

    st.dataframe(data_merged_sorted,
                 hide_index=True,
                 column_order=['Commune_LF', 'Total'],
                 column_config={
                     'Commune_LF': st.column_config.TextColumn('Commune'),
                     'Total': st.column_config.ProgressColumn('Tonne de CO₂eq', format='%.2f', min_value=0, max_value=max(data_merged['Total']))
                     },
                 width=800
                 )
    
    with st.expander('🔍 Details', expanded=True):
        st.write('''
        - Data source: [Inventaire de gaz a effet de serre territorialisé - Data Gouv](https://www.data.gouv.fr/fr/datasets/inventaire-de-gaz-a-effet-de-serre-territorialise/)
        - :orange[**Note**]: The data is from **2016** and is subject to change.
        ''')