import streamlit as st
from src.person import Person
from src.ekg_data import EKGdata
from src.read_data import load_person_data, get_name_to_id
from app_pages import overview, sleep_analysis, account, ekg_analysis, login

st.markdown("""
<style>

/* Titel */
[data-testid="stSidebar"] h1 {
    font-size: 2.5rem;
}

/* Radio-Buttons */
[data-testid="stSidebar"] label {
    font-size: 2rem;
    font-weight: 700;
}

/* Abstand zwischen den Einträgen */
[data-testid="stSidebar"] div[role="radiogroup"] > label {
    padding-top: 10px;
    padding-bottom: 30px;
}

/* Größere Kreise */
[data-testid="stSidebar"] input[type="radio"] {
    transform: scale(3);
}
            
[data-testid="stSidebar"] img {
    margin-top: -50px;
    margin-bottom: -50px;
}
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login.show()
    st.stop()


st.sidebar.image("data/pictures/icon.png")
st.sidebar.title("Schlafanalyse")

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

elif page == "💤 Schlafanalyse":
    sleep_analysis.show()

elif page == "❤️ EKG-Datenanalyse":
    ekg_analysis.show()

elif page == "👤 Benutzer":
    account.show()

st.sidebar.subheader("Platzhalter Name des aktuellen Profils")

st.sidebar.subheader("Platzhalter Bild des aktuellen Profils")