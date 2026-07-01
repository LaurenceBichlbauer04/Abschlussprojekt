import streamlit as st
from src.person import Person
from src.ekg_data import EKGdata
from src.read_data import load_person_data, get_name_to_id

def show():
    st.set_page_config(
        page_title="EKG Analyse Sheesh :)",
        page_icon="❤️",
        layout="wide"
    )

    st.title("EKG Analyse")
    st.divider()

    # -------------------------
    # PERSONENAUSWAHL
    # -------------------------
    person_data = load_person_data()
    name_to_id = get_name_to_id(person_data)

    selected_name = st.selectbox("Person auswählen", list(name_to_id.keys()))
    selected_id = name_to_id[selected_name]

    person = Person.load_by_id(selected_id)

    st.divider()

    # -------------------------
    # TESTAUSWAHL
    # -------------------------
    tests = person.ekg_tests

    if len(tests) > 1:
        selected_test = st.selectbox(
            "EKG-Test auswählen",
            tests,
            format_func=lambda test: f"Test {test['id']}"
        )
    else:
        selected_test = tests[0]

    ekg_data = EKGdata(selected_test)

    st.write("**Testdatum:**", selected_test["date"])

    # -------------------------
    # PERSON INFO
    # -------------------------
    left_col, right_col = st.columns([1, 2])

    with left_col:
        st.subheader(person.get_full_name())
        st.write("**Geburtsjahr:**", person.date_of_birth)
        st.write("**Maximale Herzfrequenz:**", person.calc_max_heart_rate())
        st.write("**Geschlecht:**", person.gender)

    with right_col:
        st.image(person.get_image(), width=250)

    st.divider()

    # -------------------------
    # EKG PARAMETER
    # -------------------------
    st.subheader("EKG-Daten")

    threshold = st.slider(
        "Peak-Schwellwert",
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

    start_idx, end_idx = st.slider(
        "Zeitbereich auswählen (Index)",
        min_value=0,
        max_value=len(ekg_data.df) - 1,
        value=(0, min(5000, len(ekg_data.df) - 1))
    )

    # -------------------------
    # DATEN FILTERUNG
    # -------------------------
    df_plot = ekg_data.df.iloc[start_idx:end_idx]

    # -------------------------
    # PEAKS
    # -------------------------
    all_peaks = ekg_data.find_peaks(
        threshold=threshold,
        respacing_factor=respacing_factor
    )

    peaks_in_range = [
        p for p in all_peaks
        if p >= start_idx and p < end_idx
    ]

    # -------------------------
    # ZEIT & HERZRATE
    # -------------------------
    time_ms = df_plot["Zeit in ms"]
    duration_ms = time_ms.iloc[-1] - time_ms.iloc[0]
    duration_min = duration_ms / 60000

    heart_rate = len(peaks_in_range) / duration_min if duration_min > 0 else 0

    # -------------------------
    # OUTPUT
    # -------------------------
    st.write("**Anzahl gefundener Peaks:**", len(peaks_in_range))

    st.write(
        "**Durchschnittliche Herzrate:**",
        round(heart_rate, 1),
        "BPM"
    )

    # -------------------------
    # PLOT
    # -------------------------
    ekg_data.plot_time_series(df_plot, peaks_in_range)