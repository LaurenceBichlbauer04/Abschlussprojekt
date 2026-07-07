import streamlit as st
import os
from src.crypt import hash_password
from src.read_data import add_person
from src.person import Person

def show():
    error = None
    st.set_page_config(
        page_title="Registrierung",
        page_icon="👤",
        layout="wide"
    )
    col = st.columns(2)

    with col[0]:
        st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
        st.image("data/pictures/icon.png", width= 750)

    with col[1]:
        st.title("Neues Konto erstellen")
        #st.divider()
        

        gender_options = {
        "Mann": "male",
        "Frau": "female",
        "Divers": "diverse" 
        }

        
        firstname = st.text_input("Vorname", key="reg_firstname")
        lastname = st.text_input("Nachname", key="reg_lastname")
        gender = st.selectbox("Geschlecht", gender_options.keys())
        date_of_birth = st.number_input("Geburtsjahr", key="reg_date_of_birth", min_value=1900, max_value=2027, value=2000, step= 1)
        username = st.text_input("Benutzername", key="reg_username")
        password1 = st.text_input("Passwort", type="password", key= "reg_password1")
        password2 = st.text_input("Passwort wiederholen", type="password", key= "reg_password2")

        picture_file = st.file_uploader(
            "Profilbild auswählen",
            type=["jpg", "jpeg", "png"]
        )
        
        col1 = st.columns(2)

        with col1[0]:
            if st.button("Registrieren", width="stretch"): 
                error = check_person(firstname, lastname, username, password1, password2)
                if  error == None:
                    hash_pwd = hash_password(password1)
                    if picture_file is None:
                        st.error("Bitte ein Profilbild auswählen.")

                    else:
                        import os

                        save_path = os.path.join(
                            "data",
                            "pictures",
                            picture_file.name
                        )

                        with open(save_path, "wb") as f:
                            f.write(picture_file.getbuffer())

                        add_person(
                            username,
                            hash_pwd,
                            date_of_birth,
                            firstname,
                            lastname,
                            gender,
                            save_path
                        )
                        user = Person.load_by_username(username)
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.user_id = user.id
                        st.rerun()
                    add_person(username, hash_pwd, date_of_birth, firstname, lastname, gender)
                    user = Person.load_by_username(username)
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.rerun()

        with col1[1]:
            if st.button("zum Login zurück", width="stretch"):
                st.session_state.page = "login"
                st.rerun()
        if error != None:
            st.error(error)



def check_person(firstname, lastname, username, password1, password2):
    if firstname.strip() == "":
        return "Bitte Vornamen eingeben"
    if lastname.strip() == "":
        return "Bitte Nachnamen eingeben"
    if username.strip() == "":
        return "Bitte Benutzername eingeben"
    if Person.load_by_username(username) != None:
        return "Benutzername bereits verfügbar"
    if password1 != password2:
        return "Passwort stimmt nicht überein"
    return None
    
