import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Charger les données
data = pd.read_csv('emissions_ges_france.csv')
coordinates = pd.read_csv('communes_coordinates.csv', sep='|')

# Nettoyer les données (mettre les noms de communes en majuscules)
coordinates['Commune'] = coordinates['Commune'].str.upper()

# Fusionner les données
data_geo = pd.merge(data, coordinates, on='Commune', how='left')

# Calcul des émissions totales par commune
emission_columns = ['Agriculture', 'Autres transports', 'CO2 biomasse hors-total', 'Déchets', 'Energie', 'Industrie hors-énergie', 'Résidentiel', 'Routier', 'Tertiaire']
data_geo['Emissions Totales'] = data_geo[emission_columns].sum(axis=1)

# Filtrer les lignes avec des valeurs NaN dans 'Latitude' ou 'Longitude'
data_geo = data_geo.dropna(subset=['Latitude', 'Longitude'])

# Créer la carte
m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

# Ajouter les marqueurs pour chaque commune
for i, row in data_geo.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=row['Emissions Totales'] / 1000,  # Ajuster la taille du cercle
        popup=f"{row['Commune'].title()}: {row['Emissions Totales']} tonnes",
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(m)

# Afficher la carte dans Streamlit
folium_static(m)
