"""
**@author : Kevin KURTZ**
**@email : kevin.kurtz@efrei.net**
"""

#
import streamlit as st
import pandas as pd
import plotly.express as px
import requests  # Pour charger le GeoJSON depuis une URL

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")

# Load data
data_emissions = pd.read_csv('emissions_ges_france.csv')
data_coordinates = pd.read_csv('communes_coordinates.csv', sep='|')
dep_data = pd.read_csv('communes-departement-region.csv')

# -------------------------- Clean emissions data -------------------------- #
data_emissions['Commune_format'] = data_emissions['Commune']  # Clone
data_emissions['Commune'] = data_emissions['Commune'].str.replace('-', '').str.replace(' ', '').str.replace('\'', '').str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

# ---------------------------- Clean temp data ----------------------------- #
dep_data = dep_data[['nom_commune_complet', 'nom_departement']]  # Keep only the columns we need
dep_data = dep_data.rename(columns={'nom_departement': 'Département', 'nom_commune_complet': 'Commune'})
dep_data['Commune'] = dep_data['Commune'].str.upper()
dep_data['Commune'] = dep_data['Commune'].str.replace('-', '').str.replace(' ', '').str.replace('\'', '').str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

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


# ---------------------------- Sidebar ----------------------------- #
with st.sidebar:
    st.title('🏭 Greenhouse Gas Emissions in France')


# ---------------------------- Main page ----------------------------- #
st.title('🏭 Greenhouse Gas Emissions in France')


# ---------------------------- App layout ----------------------------- #
# Columns
col = st.columns((1.5, 4.5, 2), gap='medium')
with col[0]:
    st.write('a')
with col[1]:
    st.write('b')
with col[2]:
    st.write('z')
    