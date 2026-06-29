import streamlit as st
from src.person import Person
from src.ekg_data import EKGdata
from src.read_data import load_person_data, get_name_to_id

def show():



    st.title("EKG Analyse")

    st.divider()

    person_data = load_person_data()
    name_to_id = get_name_to_id(person_data)



    selected_name = st.selectbox("Person auswählen", list(name_to_id.keys()))

    selected_id = name_to_id[selected_name]

    st.divider()

    person = Person.load_by_id(selected_id)
    ekg_data = EKGdata.load_by_id(selected_id)



    left_col, right_col = st.columns([1, 2])


    with left_col:
        st.subheader(person.get_full_name())
        st.write("**Alter:**", person.calc_age())
        st.write("**Maximale Herzfrequenz:**", person.calc_max_heart_rate())
        st.write("**Geschlecht:**", person.gender)
    
    with right_col:
        st.image(person.get_image(), width=250)