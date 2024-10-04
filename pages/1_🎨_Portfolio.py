"""
**@author : Kevin KURTZ**
**@contact : contact@kevin-kurtz.fr**
"""

# --------------------------- Import libraries --------------------------- #
import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------- Page Configuration ---------------------------- #
st.set_page_config(page_title="Portfolio - Kevin Kurtz", page_icon="🎓", layout="wide")

# --------------------------- Sidebar Contact ---------------------------- #
with st.sidebar:
    st.header("Contact Information")
    st.markdown("""
    - 📧 **Email**: [contact@kevin-kurtz.fr](mailto:contact@kevin-kurtz.fr)
    - 🌐 **LinkedIn**: [Kevin Kurtz](https://www.linkedin.com/in/kevin-kurtz/)
    - 💻 **GitHub**: [ktzkvin](https://github.com/ktzkvin)
    """)
    st.markdown("---")
    st.write("This portfolio showcases my skills, projects, and professional experiences.")

# --------------------------- Introduction ------------------------------- #
st.title("🎓 Kevin Kurtz's Portfolio")
st.markdown("""
I am a Master's student in **Data and AI** at EFREI Paris, passionate about **Data Science**, 
**Machine Learning**, and **Artificial Intelligence**. Below, you'll find an interactive overview of my skills, projects, and experiences.
""")

# ---------------------- Spider Chart of Skills -------------------------- #
st.header("Technical Skills")

# Data for the spider chart (replace with your actual skill data)
skills = {
    'Skills': ['Python', 'Git', 'SQL', 'Pandas', 'TensorFlow', 'Matplotlib', 'Power BI', 'Scikit-learn'],
    'Proficiency': [8, 7, 6, 8, 7, 7, 5, 6]
}

df_skills = pd.DataFrame(skills)

# Create the spider chart using Plotly
fig = px.line_polar(df_skills, r='Proficiency', theta='Skills', line_close=True, 
                    title="Kevin's Technical Skills", range_r=[0, 10], template="plotly_dark")

fig.update_traces(fill='toself')

# Display the chart
st.plotly_chart(fig)

# --------------------- Horizontal Timeline for Experience ---------------- #
st.header("Professional Experience")

# HTML and CSS for the horizontal timeline
timeline_html = """
<div class="timeline-container">
    <div class="timeline-item">
        <div class="timeline-date">Jan 2023 - Feb 2023</div>
        <div class="timeline-content">
            <h3>Data Science Intern</h3>
            <p>Darty Nation - Assisted clients and optimized their shopping experience through data analysis.</p>
        </div>
    </div>
    <div class="timeline-item">
        <div class="timeline-date">Nov 2021 - Present</div>
        <div class="timeline-content">
            <h3>Student Assistant</h3>
            <p>Restaurant l’Inattendu - Provided support in kitchen and service, contributing to the overall customer experience.</p>
        </div>
    </div>
    <!-- Add more timeline items here -->
</div>
"""

# CSS for styling the horizontal timeline
timeline_css = """
<style>
.timeline-container {
    display: flex;
    overflow-x: auto;
    white-space: nowrap;
    padding: 20px;
}
.timeline-item {
    display: inline-block;
    background: #1f1f1f;
    color: white;
    border-radius: 10px;
    padding: 20px;
    margin-right: 20px;
    min-width: 250px;
    max-width: 300px;
}
.timeline-date {
    font-weight: bold;
    margin-bottom: 10px;
}
.timeline-content h3 {
    margin: 0;
    font-size: 1.2em;
}
.timeline-content p {
    margin-top: 10px;
    font-size: 0.9em;
    color: #aaa;
}
</style>
"""

# Display the timeline in Streamlit
st.markdown(timeline_css, unsafe_allow_html=True)
st.markdown(timeline_html, unsafe_allow_html=True)

# ------------------------ Project Cards ------------------------------- #
st.header("Projects")

# Project data (replace with your actual projects)
projects = [
    {
        "title": "Machine Learning Dashboard",
        "description": "An interactive dashboard showcasing various machine learning models and their performance on different datasets.",
        "tech_stack": "Python, Streamlit, Scikit-learn, Plotly",
        "link": "https://github.com/ktzkvin/ml-dashboard"
    },
    {
        "title": "Data Visualization with Plotly",
        "description": "A project focused on creating engaging data visualizations using Plotly and Streamlit for a smooth user experience.",
        "tech_stack": "Python, Plotly, Streamlit",
        "link": "https://github.com/ktzkvin/data-viz-plotly"
    },
    {
        "title": "NLP Sentiment Analysis",
        "description": "Natural language processing project analyzing sentiments from large datasets using machine learning algorithms.",
        "tech_stack": "Python, NLTK, Scikit-learn",
        "link": "https://github.com/ktzkvin/nlp-sentiment-analysis"
    }
]

# Display project cards in 3 columns
col1, col2, col3 = st.columns(3)

for index, project in enumerate(projects):
    if index % 3 == 0:
        with col1:
            st.markdown(f"### [{project['title']}]({project['link']})")
            st.write(project['description'])
            st.write(f"**Tech Stack**: {project['tech_stack']}")
    elif index % 3 == 1:
        with col2:
            st.markdown(f"### [{project['title']}]({project['link']})")
            st.write(project['description'])
            st.write(f"**Tech Stack**: {project['tech_stack']}")
    else:
        with col3:
            st.markdown(f"### [{project['title']}]({project['link']})")
            st.write(project['description'])
            st.write(f"**Tech Stack**: {project['tech_stack']}")
