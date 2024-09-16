# 🏭 GHG Emissions Dashboard - France

Welcome to the interactive dashboard for greenhouse gas (GHG) emissions in France! 🌍 This project uses **Streamlit** and **Plotly** to visualize emissions by sector and department, with interactive options to explore data in various CO₂ equivalent units.

## 📋 Features

- 📊 **Emissions Visualization**: A map of France with a choropleth of emissions by department.
- 🏆 **Top Communes and Departments**: Display of the most and least polluting departments.
- 📊 **Emissions by Sector**: Detailed charts showing emissions by various sectors (agriculture, transport, industry, etc.).
- 💾 **Data Download**: Download raw data files in CSV format.

![Dashboard Screenshot](screenshots/dashboard_overview.png)

## 🚀 Installation and Setup

### Prerequisites

Ensure you have **Python 3.8+** and **Streamlit** installed.

### Installation

1. Clone the GitHub repository:

   ```bash
   git clone https://github.com/ktzkvin/GHG-Emissions-Dashboard.git
   cd GHG-Emissions-Dashboard

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt

### Running the Application

1. Run the application using **Streamlit**:

   ```bash
   streamlit run dashboard.py

2. Access the dashboard via your browser at: `http://localhost:8501`.

![Screenshot Heatmap](screenshots/heatmap_emissions.png)

## 📊 Example Visualizations

### Emissions Map by Department

Visualize the total GHG emissions by department across an interactive map.

![France Heatmap](screenshots/france_heatmap.png)

### Top Polluting Departments

Discover the departments with the highest and lowest CO₂eq emissions.

![Top Pollutant Departments](screenshots/top_pollutants.png)

### Emissions by Sector

An interactive bar chart to explore emissions across different sectors.

![Sector Emissions](screenshots/sector_emissions.png)

## 🧩 Technologies Used

- **Streamlit** for the interactive user interface.
- **Plotly** for interactive charts.
- **Pandas** for data manipulation.

## 📥 Download Data

Click the integrated download button on the dashboard to retrieve the CSV files used in this project.

## 💡 Notes

- The data is based on the 2016 territorial greenhouse gas inventory. The data is subject to updates.
- CO₂eq conversion factors are sourced from reliable sources like **Alterna Énergie**.

---
