import streamlit as st
from src.person import Person
from src.ekg_data import EKGdata
from src.person import Person
from app_pages import sleep_analysis, account, ekg_analysis, login

st.markdown("""
<style>

/* Gesamte rechte Seite */
.stApp {
    background-color: #0E1624;
}
/* Oberer Header */
[data-testid="stHeader"] {
    background-color: #0E1624;
}
/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07111f 0%, #0b1020 100%);
}

/* Sidebar-Inhalt */
[data-testid="stSidebar"] > div:first-child {
    padding: 1.4rem 1rem;
}

/* Logo */
[data-testid="stSidebar"] img {
    width: 85px;
    display: block;
    margin: 0 auto 18px auto;
    border-radius: 50%;
}

/* Titel */
[data-testid="stSidebar"] h1 {
    font-size: 1.45rem;
    text-align: center;
    margin-bottom: 18px;
}

/* Radio Cards */
[data-testid="stSidebar"] div[role="radiogroup"] > label {
    background-color: transparent;
    border-radius: 10px;
    padding: 8px 10px;
    margin-bottom: 4px;
}

/* Hover */
[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
    background-color: rgba(255,255,255,0.08);
}

/* Text */
[data-testid="stSidebar"] div[role="radiogroup"] label p {
    font-size: 0.9rem;
    font-weight: 600;
}

/* Radio Kreis */
[data-testid="stSidebar"] input[type="radio"] {
    transform: scale(1.15);
}

/* Logout unten fixieren */
[data-testid="stSidebar"] .stButton {
    position: fixed;
    bottom: 24px;
    left: 18px;
    width: 250px;
}

/* Logout Button */
[data-testid="stSidebar"] .stButton button {
    background-color: #e63946;
    color: white;
    border: none;
    border-radius: 12px;
    height: 44px;
    font-weight: 700;
}

[data-testid="stSidebar"] .stButton button:hover {
    background-color: #c92f3b;
    color: white;
}

</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login.show()
    st.stop()


st.sidebar.image("data/pictures/icon.png", width= "stretch")
st.sidebar.title("Schlafanalyse")

page = st.sidebar.radio(
    "",
    [
        # "🏠 Übersicht",
        "💤 Schlafanalyse",
        "❤️ EKG-Datenanalyse",
        "👤 Benutzer"
    ],
    label_visibility="collapsed",
    horizontal= False
)

# if page == "🏠 Übersicht":
#     overview.show()

if page == "💤 Schlafanalyse":
    sleep_analysis.show()

elif page == "❤️ EKG-Datenanalyse":
    ekg_analysis.show()

elif page == "👤 Benutzer":
    account.show()

#st.sidebar.subheader("Platzhalter Name des aktuellen Profils")

#st.sidebar.markdown("<div style='height: 200px;'></div>", unsafe_allow_html=True)


#st.sidebar.markdown("<div class='logout-space'></div>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)
person = st.session_state.user
st.sidebar.write("Eingeloggt : " + person.get_full_name())
if st.sidebar.button("Logout", width="stretch"):
    st.session_state.logged_in = False
    st.rerun()
