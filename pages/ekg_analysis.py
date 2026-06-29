import streamlit as st
import json
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


    st.divider()
    st.subheader("EKG-Daten")

    threshold = st.slider(
           "Peak-Schellenwert",
           min_value=240,
           max_value=400,
           value=340,
           step=10
    )

    respacing_factor = st.slider(
           "Abtast-Abstand",
            min_value=1,
            max_value=20,
            value=5
    )

    peaks = ekg_data.find_peaks(threshold=threshold,respacing_factor=respacing_factor)

    st.write("**Anzahl gefundener Peaks:** ", len(peaks))


    ekg_data.plot_time_series()