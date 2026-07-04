import streamlit as st

from app_pages import registration

def show():

    if "page" not in st.session_state:
        st.session_state.page = "login"

    if st.session_state.page == "register":
        registration.show()
        st.stop()


    st.title("Login")

    username = st.text_input("Benutzername", key="login_username")
    password = st.text_input("Passwort", type="password", key="login_password")

    cols = st.columns(2)
    with cols[0]:
        if st.button("Einloggen", use_container_width=True):

            if username == "admin" and password == "1234":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Benutzername oder Passwort falsch")
    with cols[1]:
        if st.button("Registrieren", use_container_width=True):
            st.session_state.page = "register"
            st.rerun()