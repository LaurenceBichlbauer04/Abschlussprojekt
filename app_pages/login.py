import streamlit as st
from src.person import Person
from src.crypt import check_password
from app_pages import registration

def show():

    st.set_page_config(
        page_title="Login",
        page_icon="👤",
        layout="wide"
    )


    if "page" not in st.session_state:
        st.session_state.page = "login"

    if st.session_state.page == "register":
        registration.show()
        st.stop()

    cols = st.columns(2)
    with cols[0]:
        st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
        st.image("data/pictures/icon.png", width= 750)
    
    with cols[1]:
        st.markdown("<div style='height: 200px;'></div>", unsafe_allow_html=True)
        st.title("Login")
        
        username = st.text_input("Benutzername", key="login_username")
        password = st.text_input("Passwort", type="password", key="login_password")

        cols1 = st.columns(2)
        with cols1[0]:
            if st.button("Einloggen", use_container_width=True):
                
                user = Person.load_by_username(username)
                if user == None:
                    st.error("Benutzername nicht gefunden")
                # if username == "admin" and password == "1234":
                elif check_password(password, user.hash_pwd) == True:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Passwort falsch")
        with cols1[1]:
            if st.button("Registrieren", use_container_width=True):
                st.session_state.page = "register"
                st.rerun()