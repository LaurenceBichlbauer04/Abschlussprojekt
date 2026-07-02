import streamlit as st

from app_pages import registration

def show():
    st.title("Login")

    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")

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
            registration.show()
            st.stop()