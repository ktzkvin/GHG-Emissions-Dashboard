"""
**@author : Kevin KURTZ**
**@email : contact@kevin-kurtz.fr**
"""

import streamlit as st

st.set_page_config(page_title="Kevin Kurtz", page_icon="👋", layout="centered")

st.markdown(
    """
    <style>
    h1 {
        font-size: 3em;
    }
    .description {
        padding-top: 30px;
        font-family: 'Courier New', monospace;
        font-size: 1.1em;
        max-width: 600px;
        margin: 0 auto;
        text-align: justify;
    }
    .emoji-container {
        display: flex;
        align-items: center; /* Alignement vertical du texte et de l'emoji */
        position: absolute;
        top: -350px; /* Position que tu avais spécifiée */
        left: -420px; /* Position que tu avais spécifiée */
    }
    .floating-emoji {
        font-size: 1.5em; /* Taille plus petite */
        animation: bounce 0.8s infinite alternate; /* Animation rapide */
        margin-right: 10px; /* Espace entre l'emoji et le texte */
    }
    .static-text {
        font-size: 1.1em; /* Taille du texte statique */
        color: #ffffff; /* Couleur du texte */
    }
    @keyframes bounce {
        0% { transform: translateX(0); }
        100% { transform: translateX(10px); }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.write("")
st.write("")
st.write("")


st.markdown("<h1>Hi, I'm Kevin Kurtz! 👋</h1>", unsafe_allow_html=True)

st.markdown(
    """
    <p class="description">
    Welcome to my personal Streamlit app! <br>
    I'm a student in computer science and I'm passionate about Data Science 📊 and machine learning 🤖. <br><br>
    I created this app to share some of my projects 🚀 and experiments 🧪. Feel free to explore and don't hesitate to contact me if you have any questions or suggestions.
    </p>    
    """, unsafe_allow_html=True
)

st.markdown(
    """
    <div class="emoji-container">
        <span class="floating-emoji">👈</span>
        <span class="static-text">&nbsp;&nbsp;Try to click there!</span> 
    </div>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown("## Keep in Touch")
    st.markdown("📧 [Email me](mailto:contact@kevin-kurtz.fr)")
    st.markdown("💻 [GitHub](https://github.com/ktzkvin)")
