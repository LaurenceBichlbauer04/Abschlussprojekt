import streamlit as st
import pandas as pd
from src.sleep_data import sleep_data
from src.read_data import save_uploaded_smartwatch_file
from src.person import Person

def show():
    st.set_page_config(
        page_title="Schlafanalyse",
        page_icon="💤",
        layout="wide"
    )

    st.markdown("""
    <style>
    [data-testid="stPlotlyChart"] {
        background: #0f172a;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 8px;
    }
    .block-container{
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    person = st.session_state.user

    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

    titlecol = st.columns(2)

    with titlecol[0]:
        st.title("Schlafanalyse")

    with titlecol[1]:
        options_date = [p["date"] for p in person.smartwatch_data]

        if len(options_date) > 0:
            selected_date = st.selectbox(
                "Datum der Schlafanalyse",
                options=options_date
            )
        else:
            selected_date = None

    if selected_date is None:
        st.warning("Für diese Person wurden noch keine Smartwatch-Daten gefunden.")

        uploaded_file = st.file_uploader(
            "Smartwatch-Datei hochladen",
            type=["csv", "json"]
        )

        date = st.date_input("Datum der Schlafanalyse")

        if uploaded_file is not None:
            if st.button("Datei speichern"):
                file_path = save_uploaded_smartwatch_file(uploaded_file)

                person.add_smartwatch_data(
                    date=date.strftime("%d.%m.%Y"),
                    file_path=file_path
                )

                st.success("Datei erfolgreich hinzugefügt.")
                st.rerun()

        return

    selected_entry = next(
        p for p in person.smartwatch_data
        if p["date"] == selected_date
    )

    file = selected_entry["result_link"]

    sleep001 = sleep_data(file)
    sleep001.load_data()
    sleep001.filter_data()

    fig = sleep001.plot_heart_rate()
    fig2 = sleep001.plot_spo2_rate()

    cols = st.columns(2)

    with cols[0]:
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with cols[1]:
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
