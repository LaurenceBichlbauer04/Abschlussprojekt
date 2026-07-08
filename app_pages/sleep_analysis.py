import streamlit as st
from src.sleep_data import sleep_data
from src.read_data import save_uploaded_smartwatch_file

def metric_card(title, value, icon=""):

    """Zeigt eine formatierte Kennzahlenkarte mit Titel, Wert und optionalem Symbol an."""

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{icon} {title}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def sleepscore_card(score):
    """
    Erstellt eine größere Karte für die Schlafqualität.

    Der Text wird abhängig vom berechneten Schlafscore angepasst.
    """
    if score >= 85:
        title = "Ausgezeichnet geschlafen 🌟"
        text = "Dein Schlaf war sehr erholsam."
    elif score >= 70:
        title = "Gut geschlafen 👍"
        text = "Du hast insgesamt gut geschlafen."
    elif score >= 50:
        title = "Weniger gut geschlafen 😐"
        text = "Dein Schlaf war teilweise unruhig oder zu kurz."
    else:
        title = "Schlecht geschlafen 😴"
        text = "Dein Schlaf war deutlich beeinträchtigt."

    st.markdown(f"""
        <div class="metric-card" style="height: 300px; text-align:center;">
            <div class="metric-title">Schlafqualität</div>
            <div style="
                margin: 30px auto 10px auto;
                width: 150px;
                height: 150px;
                border-radius: 50%;
                border: 14px solid #6ee75f;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 42px;
                font-weight: 800;
                color: white;">
                {score}
            </div>
            <div style="color:white; font-weight:700;">{title}</div>
            <div style="color:#A8B3C7; font-size:13px; margin-top:10px;">
                {text}
            </div>
        </div>
    """, unsafe_allow_html=True)


@st.dialog("Neue Schlafdaten hochladen")
def upload_sleep_dialog(person):
    """
    Öffnet einen Dialog zum Hochladen neuer Schlafdaten.

    Die Datei wird gespeichert und anschließend bei der aktuellen Person
    in der JSON-Datei ergänzt.
    """
    uploaded_file = st.file_uploader(
        "CSV-Datei auswählen",
        type=["csv"]
    )

    date = st.date_input("Datum der Schlafanalyse")

    if uploaded_file is not None:
        if st.button("Speichern"):
            file_path = save_uploaded_smartwatch_file(uploaded_file)

            person.add_smartwatch_data(
                date=date.strftime("%d.%m.%Y"),
                file_path=file_path
            )

            st.success("Datei erfolgreich hinzugefügt.")
            st.rerun()


def show():
    """
    Zeigt die Schlafanalyse-Seite der Streamlit-App an.

    Die Seite lädt die Schlafdaten der angemeldeten Person,
    berechnet Schlafphasen, Kennzahlen und Diagramme.
    """
    st.set_page_config(
        page_title="Schlafanalyse",
        page_icon="💤",
        layout="wide"
    )

    # CSS für Layout, Karten und Plotly-Diagramme
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

    # Prüfen, ob ein User vorhanden ist
    if "user" not in st.session_state:
        st.warning("Bitte zuerst einloggen.")
        return

    person = st.session_state.user

    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

    # Header mit Titel, Datumsauswahl und Upload-Button
    header = st.columns([1, 2])

    with header[0]:
        st.title("🌙 Schlafanalyse")

    with header[1]:
        subheader = st.columns(2)
        options_date = [p["date"] for p in person.smartwatch_data]

        if len(options_date) > 0:
            with subheader[0]:
                selected_date = st.selectbox(
                    "Datum der Schlafanalyse",
                    options=options_date,
                    key="selected_sleep_date"
                )

            with subheader[1]:
                if st.button("📤 Schlafdaten hochladen"):
                    upload_sleep_dialog(person)
        else:
            selected_date = None

    # Falls keine Daten vorhanden sind, Upload-Möglichkeit anzeigen
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

    # Passende Datei zum ausgewählten Datum suchen
    selected_entry = next(
        p for p in person.smartwatch_data
        if p["date"] == selected_date
    )

    file = selected_entry["result_link"]

    # Schlafdaten laden und analysieren
    sleep = sleep_data(file)
    sleep.load_data()
    sleep.filter_data()
    sleep.calculate_sleep_phases()

    result = sleep.calculate_sleep_score()

    st.divider()

    # Obere Kennzahlen
    cards = st.columns(5)

    with cards[0]:
        metric_card("Schlafdauer", f'{result["sleep_duration_hours"]} h', "🕒")

    with cards[1]:
        metric_card("Schlafqualität", f'{result["sleep_score"]} /100', "⭐")

    with cards[2]:
        sleep_efficiency = round(100 - result["awake_percent"])
        metric_card("Schlafeffizienz", f"{sleep_efficiency} %", "◎")

    with cards[3]:
        metric_card("Durchschnitt SpO₂", f'{result["avg_spo2"]} %', "💧")

    with cards[4]:
        metric_card("Durchschnitt Herzfrequenz", f'{result["avg_heart_rate"]} bpm', "♡")

    st.divider()

    # Mittlere Reihe: Schlafphasen + Score-Karte
    mid = st.columns([2, 1])

    with mid[0]:
        fig_phases = sleep.plot_sleep_phases()
        st.plotly_chart(
            fig_phases,
            width="stretch",
            config={"displayModeBar": False}
        )

    with mid[1]:
        sleepscore_card(result["sleep_score"])

    st.divider()

    # Untere Reihe: Herzfrequenz und SpO2
    bottom = st.columns(2)

    with bottom[0]:
        fig_hr = sleep.plot_heart_rate()
        st.plotly_chart(
            fig_hr,
            width="stretch",
            config={"displayModeBar": False}
        )

    with bottom[1]:
        fig_spo2 = sleep.plot_spo2_rate()
        st.plotly_chart(
            fig_spo2,
            width="stretch",
            config={"displayModeBar": False}
        )

    # Warnhinweis bei auffälligen SpO2-Abfällen
    if result["apnea_warning"]:
        st.toast(
            "⚠️ Mögliche Schlafapnoe erkannt. Bitte ärztlich abklären lassen.",
            icon="⚠️"
        )