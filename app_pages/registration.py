import streamlit as st

def show():
    st.title("Registration")
    #st.divider()
    st.subheader("Neues Konto erstellen")

    firstname = st.text_input("Vorname", key="reg_firstname")
    lastname = st.text_input("Nachname", key="reg_lastname")
    username = st.text_input("Benutzername", key="reg_username")
    password1 = st.text_input("Passwort", type="password", key= "reg_password1")
    password2 = st.text_input("Passwort wiederholen", type="password", key= "reg_password2")
    
    col = st.columns(2)

    with col[0]:
        if st.button("Registrieren", use_container_width=True) and (password1 == password2):
            # if check_person == True:

            #überprüft person
            st.error("Platzhalter")
        else:
            st.error("Passwort stimmt nicht überein")
    
    with col[1]:
        if st.button("zum Login zurück", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

# def check_person():
    
