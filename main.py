import streamlit as st
from src.person import Person
from src.ekg_data import EKGdata
from src.read_data import load_person_data, get_name_to_id
from pages import overview, sleep_analysis, account, ekg_analysis

st.set_page_config(
    layout="wide",
    page_title="Schlafanalyse",
    page_icon= "🌙"
    )

st.sidebar.title("🌙 Schlafanalyse")

page = st.sidebar.radio(
    "",
    [
        "🏠 Übersicht",
        "💤 Schlafanalyse",
        "❤️ EKG-Datenanalyse",
        "👤 Benutzer"
    ],
    label_visibility="collapsed",
    horizontal= False
)

if page == "🏠 Übersicht":
    overview.show()

elif page == "📊 Analyse":
    sleep_analysis.show()

elif page == "❤️ EKG-Datenanalyse":
    ekg_analysis.show()

elif page == "👤 Account":
    account.show()

