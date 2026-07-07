import pandas as pd
import plotly.graph_objects as go


class sleep_data:
    """
    Klasse zur Verarbeitung und Analyse von Schlafdaten.

    Die Klasse lädt Smartwatch-Daten aus einer CSV-Datei, filtert Messwerte,
    berechnet Schlafphasen, erstellt einen Schlafscore und erzeugt Plotly-Diagramme.
    """

    def __init__(self, result_link):
        """
        Erstellt ein sleep_data-Objekt.

        Parameters:
            result_link (str): Pfad zur CSV-Datei mit den Schlafdaten.
        """
        self.result_link = result_link
        self.data = None

    def load_data(self):
        """
        Lädt die CSV-Datei in einen Pandas DataFrame.

        Returns:
            pd.DataFrame: Geladene Schlafdaten.
        """
        self.data = pd.read_csv(self.result_link)
        return self.data

    def filter_data(self):
        """
        Glättet wichtige Messwerte mit einem gleitenden Fenster.

        Dadurch werden starke Ausreißer reduziert und die Werte eignen sich besser
        für Diagramme und die spätere Schlafphasen-Erkennung.

        Returns:
            pd.DataFrame: DataFrame mit zusätzlichen gefilterten Spalten.
        """
        if self.data is None:
            self.load_data()

        # Herzfrequenz glätten
        self.data["heart_rate_filtered"] = self.data["heart_rate"].rolling(
            window=5,
            min_periods=1,
            center=True
        ).mean()

        # HRV glätten
        self.data["hrv_filtered"] = self.data["hrv"].rolling(
            window=5,
            min_periods=1,
            center=True
        ).mean()

        # SpO2 glätten
        self.data["spo2_filtered"] = self.data["spo2"].rolling(
            window=5,
            min_periods=1,
            center=True
        ).median()

        # Bewegung glätten
        self.data["movement_filtered"] = self.data["movement"].rolling(
            window=5,
            center=True,
            min_periods=1
        ).mean()

        # Atemfrequenz glätten
        self.data["respiration_filtered"] = self.data["respiration_rate"].rolling(
            window=5,
            center=True,
            min_periods=1
        ).mean()

        return self.data

    def calculate_sleep_phases(self):
        """
        Berechnet einfache Schlafphasen anhand der gefilterten Messwerte.

        Die Schlafphasen werden regelbasiert aus Herzfrequenz, HRV,
        Bewegung und Atemfrequenz abgeleitet.

        Returns:
            pd.DataFrame: DataFrame mit zusätzlicher Spalte 'sleep_phase'.
        """
        if self.data is None or "heart_rate_filtered" not in self.data.columns:
            self.filter_data()

        df = self.data.copy()

        # Dynamische Grenzwerte passend zu den jeweiligen Daten berechnen
        hr_low = df["heart_rate_filtered"].quantile(0.30)
        hr_high = df["heart_rate_filtered"].quantile(0.70)

        movement_low = df["movement_filtered"].quantile(0.30)
        movement_high = df["movement_filtered"].quantile(0.70)

        respiration_low = df["respiration_filtered"].quantile(0.30)

        hrv_median = df["hrv_filtered"].median()
        respiration_median = df["respiration_filtered"].median()

        def classify_phase(row):
            """
            Ordnet einer einzelnen Datenzeile eine Schlafphase zu.
            """
            hr = row["heart_rate_filtered"]
            hrv = row["hrv_filtered"]
            movement = row["movement_filtered"]
            respiration = row["respiration_filtered"]

            if movement >= movement_high and hr >= hr_high:
                return "Wach"

            if hr <= hr_low and movement <= movement_low and respiration <= respiration_low:
                return "Tiefschlaf"

            if movement <= movement_low and hrv >= hrv_median and respiration >= respiration_median:
                return "REM-Phase"

            return "leichter Schlaf"

        df["sleep_phase"] = df.apply(classify_phase, axis=1)

        self.data = df
        return df

    def calculate_sleep_score(self):
        """
        Berechnet einen einfachen Schlafscore und wichtige Kennzahlen.

        Bewertet werden unter anderem Schlafdauer, Tiefschlafanteil,
        REM-Anteil, Wachphasen, Bewegung und SpO2-Werte.

        Returns:
            dict: Schlafscore, Schlafdauer, Durchschnittswerte und Warnhinweise.
        """
        df = self.data.copy()
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        start_time = df["timestamp"].min()
        end_time = df["timestamp"].max()

        # Schlafdauer = Zeit im Bett minus Wachzeit
        sleep_duration_hours = (
            ((end_time - start_time).total_seconds() / 60)
            - len(df[df["sleep_phase"] == "Wach"])
        ) / 60

        avg_spo2 = df["spo2"].mean()
        min_spo2 = df["spo2"].min()
        avg_hr = df["heart_rate"].mean()
        avg_hrv = df["hrv"].mean()
        avg_movement = df["movement"].mean()

        phase_counts = df["sleep_phase"].value_counts(normalize=True)

        deep_sleep_ratio = phase_counts.get("Tiefschlaf", 0)
        rem_sleep_ratio = phase_counts.get("REM-Phase", 0)
        awake_ratio = phase_counts.get("Wach", 0)

        score = 100

        # Schlafdauer bewerten
        if sleep_duration_hours < 5:
            score -= 25
        elif sleep_duration_hours < 6:
            score -= 15
        elif sleep_duration_hours < 7:
            score -= 8
        elif sleep_duration_hours > 9:
            score -= 5

        # Schlafphasen bewerten
        if deep_sleep_ratio < 0.10:
            score -= 15
        elif deep_sleep_ratio < 0.15:
            score -= 8

        if rem_sleep_ratio < 0.10:
            score -= 10
        elif rem_sleep_ratio < 0.15:
            score -= 5

        # Wachphasen und Bewegung bewerten
        if awake_ratio > 0.20:
            score -= 15
        elif awake_ratio > 0.10:
            score -= 8

        if avg_movement > df["movement"].quantile(0.75):
            score -= 5

        # Sauerstoffsättigung bewerten
        if avg_spo2 < 92:
            score -= 25
        elif avg_spo2 < 95:
            score -= 10

        if min_spo2 < 88:
            score -= 15
        elif min_spo2 < 90:
            score -= 8

        score = max(0, min(100, round(score)))

        # Einfache Warnlogik für mögliche Atemaussetzer
        low_spo2_events = df[df["spo2"] < 90]

        apnea_warning = len(low_spo2_events) > 3
        apnea_text = "Keine auffälligen Hinweise auf Schlafapnoe erkannt."

        if apnea_warning:
            apnea_text = (
                "Achtung: Es gibt auffällige SpO₂-Abfälle. "
                "Das kann ein Hinweis auf Atemaussetzer im Schlaf sein."
            )

        return {
            "sleep_score": score,
            "sleep_duration_hours": round(sleep_duration_hours, 2),
            "start_time": start_time,
            "end_time": end_time,
            "avg_spo2": round(avg_spo2, 1),
            "min_spo2": round(min_spo2, 1),
            "avg_heart_rate": round(avg_hr, 1),
            "avg_hrv": round(avg_hrv, 1),
            "deep_sleep_percent": round(deep_sleep_ratio * 100, 1),
            "rem_sleep_percent": round(rem_sleep_ratio * 100, 1),
            "awake_percent": round(awake_ratio * 100, 1),
            "apnea_warning": apnea_warning,
            "apnea_text": apnea_text
        }