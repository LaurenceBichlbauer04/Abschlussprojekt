import streamlit as st
import os
from src.person import Person
from src.ekg_data import EKGdata
from src.read_data import load_person_data, get_name_to_id, add_person, add_ekg_test, delete_person, update_person

def show():
    st.set_page_config(
        page_title="Benutzer",
        page_icon="👤",
        layout="wide"
    )

    st.title("Benutzer")

    st.divider()

    person_data = load_person_data()
    name_to_id = get_name_to_id(person_data)



    selected_name = st.selectbox("Person auswählen", list(name_to_id.keys()))

    selected_id = name_to_id[selected_name]

    st.divider()

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

        picture_path = st.text_input(
            "Bildpfad",
            value = person.picture_path
        )

        submitted = st.form_submit_button("Änderungen speichern")

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
            st.success("Person wurde gelöscht.")
            st.rerun()

    st.divider()

    st.subheader("Neue Person hinzufügen")

    with st.form("add_person_form"):

        firstname = st.text_input("Vorname")
        lastname = st.text_input("Nachname")

        birth_year = st.number_input(
            "Geburtsjahr",
            min_value=1900,
            max_value=2100,
            value=2000
        )

        gender = st.selectbox(
            "Geschlecht",
            ["male", "female"]
        )

        picture_path = st.text_input(
            "Pfad zum Bild"
        )

        submitted = st.form_submit_button("Person hinzufügen")

        if submitted:

            if not os.path.exists(picture_path):
                st.error("Bild wurde nicht gefunden.")
            
            else:
                new_id = add_person(
                    firstname,
                    lastname,
                    birth_year,
                    gender,
                    picture_path
                )

            st.success(f"Person mit ID {new_id} hinzugefügt.")

    st.divider()

    st.subheader("Neuen EKG-Test hinzufügen")

    with st.form("add_test_form"):

        test_date = st.date_input("Testdatum")

        result_link = st.text_input(
            "Pfad zur EKG-Datei"
        )

        submitted = st.form_submit_button("EKG-Test hinzufügen")

        if submitted:

            if not os.path.exists(result_link):
                st.error("EKG-Datei wurde nicht gefunden.")

            else:

                add_ekg_test(
                    selected_id,
                    test_date,
                    result_link
                )

            st.success("EKG-Test erfolgreich hinzugefügt.")