import streamlit as st
import os
from src.person import Person
from src.read_data import  add_ekg_test, delete_person, update_person

def show():
    st.set_page_config(
        page_title="Benutzer",
        page_icon="👤",
        layout="wide"
    )

    st.title("Benutzer")

    st.divider()

    selected_id = st.session_state.user_id
    person = Person.load_by_id(selected_id)

    left_col, right_col = st.columns([1, 2])


    with left_col:
        st.subheader(person.get_full_name())
        st.write("**Alter:**", person.calc_age())
        st.write("**Maximale Herzfrequenz:**", person.calc_max_heart_rate())
        st.write("**Geschlecht:**", person.gender)
    
    with right_col:
        image = person.get_image()

        if image is not None:
            st.image(image, width=250)
        else:
            st.warning("Bild konnte nicht geladen werden.")

    st.subheader("Person bearbeiten")

    with st.form("edit_person_form"):

        firstname = st.text_input(
            "Vorname",
            value=person.firstname
        )

        lastname = st.text_input(
            "Nachname",
            value=person.lastname
        )

        birth_year = st.number_input(
            "Geburtsjahr",
            min_value=1900,
            max_value=2100,
            value=person.date_of_birth
        )

        gender = st.selectbox(
            "Geschlecht",
            ["male", "female"],
            index = 0 if person.gender == "male" else 1
        )

        picture_file = st.file_uploader(
            "Neues Profilbild auswählen",
            type=["jpg", "jpeg", "png"]
        )

        submitted = st.form_submit_button("Änderungen speichern")

        # Standardmäßig das bisherige Bild behalten
        picture_path = person.picture_path

        # Falls ein neues Bild hochgeladen wurde
        if picture_file is not None:

            picture_path = os.path.join(
                "data",
                "pictures",
                picture_file.name
            )

            with open(picture_path, "wb") as file:
                file.write(picture_file.getbuffer())

        if submitted:
            update_person(
                selected_id,
                firstname,
                lastname,
                birth_year,
                gender,
                picture_path
            )

            st.success("Person wurde aktualisiert.")
            st.rerun()


    st.subheader("Person löschen")

    confirm = st.checkbox("Ich möchte diese Person wirklich löschen.")

    if confirm:
        if st.button("🗑️ Person endgültig löschen"):
            delete_person(selected_id)
            st.session_state.logged_in = False
            st.success("Person wurde gelöscht.")
            st.rerun()

    st.divider()

    st.subheader("Neuen EKG-Test hinzufügen")

    with st.form("add_test_form"):

        test_date = st.date_input("Testdatum")

        ekg_file = st.file_uploader(
            "EKG-Datei auswählen",
            type=["txt"]
        )

        submitted = st.form_submit_button("EKG-Test hinzufügen")

        if submitted:

            if ekg_file is None:
                st.error("Bitte eine EKG-Datei auswählen.")

            else:

                result_link = os.path.join(
                    "data",
                    "ekg_data",
                    ekg_file.name
                )

                with open(result_link, "wb") as file:
                    file.write(ekg_file.getbuffer())

                add_ekg_test(
                    selected_id,
                    test_date,
                    result_link
                )

                st.success("EKG-Test erfolgreich hinzugefügt.")