import json
from matplotlib import pyplot as plt
import pandas as pd
import streamlit as st

class EKGdata:

    """Verwaltet EKG-Messdaten und stellt Funktionen zur Analyse und Visualisierung bereit."""

    def __init__(self, ekg_dict):

        """Initialisiert ein EKG-Objekt aus den Daten eines EKG-Tests."""

        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',]).iloc[::2].reset_index(drop=True)
        self.peaks = []


    def find_peaks(self, threshold=0, respacing_factor=5):

        """
        Erkennt lokale Maxima im EKG oberhalb eines Schwellwertes.

        Der Parameter respacing_factor bestimmt den minimalen Abstand
        zwischen zwei erkannten Peaks.
        """

        series = self.df["Messwerte in mV"]

        peaks = []
        last_peak = -respacing_factor

        for i in range(1, len(series) - 1):

            if (
                series.iloc[i] >= series.iloc[i - 1]
                and series.iloc[i] >= series.iloc[i + 1]
                and series.iloc[i] > threshold
            ):

                if not peaks:
                    peaks.append(series.index[i])
                    last_peak = i

                elif i - last_peak >= respacing_factor:
                    peaks.append(series.index[i])
                    last_peak = i

                else:
                    # Wenn der neue Peak höher ist als der letzte,
                    # ersetze den letzten Peak
                    if series.iloc[i] > self.df.loc[peaks[-1], "Messwerte in mV"]:
                        peaks[-1] = series.index[i]
                        last_peak = i

        self.peaks = peaks
        return peaks
    
    def calc_heart_rate(self, duration_min):
        return len(self.peaks) / duration_min

    def plot_time_series(self, df_plot=None, peaks=None):

        """Zeigt den ausgewählten EKG-Zeitbereich mit markierten Peaks an."""
        
        if df_plot is None:
            df_plot = self.df
        
        if peaks is None:
            peaks = self.peaks

        fig, ax = plt.subplots(figsize=(12, 5))

        ax.plot(
            df_plot["Zeit in ms"] / 1000,
            df_plot["Messwerte in mV"],
            label="EKG"
        )

        peaks_in_plot = [p for p in self.peaks if p in df_plot.index]

        ax.scatter(
            df_plot.loc[peaks_in_plot, "Zeit in ms"] / 1000,
            df_plot.loc[peaks_in_plot, "Messwerte in mV"],
            color="purple",
            label="Peaks"
        )

        ax.set_xlabel("Zeit [s]")
        ax.set_ylabel("Spannung [mV]")
        ax.set_title("EKG mit Peaks")
        ax.legend()

        st.pyplot(fig)

    def plot_hrv(self, df_plot=None):

        """Stellt die Herzratenvariabilität anhand der RR-Intervalle grafisch dar."""

        if df_plot is None:
            df_plot = self.df

        # Nur Peaks verwenden, die im ausgewählten Bereich liegen
        peaks_in_plot = [p for p in self.peaks if p in df_plot.index]

        if len(peaks_in_plot) < 2:
            st.warning("Zu wenige Peaks im ausgewählten Bereich.")
            return

        peak_times = df_plot.loc[peaks_in_plot, "Zeit in ms"].values

        rr_intervals = []
        time_axis = []

        for i in range(1, len(peak_times)):
            rr_intervals.append(peak_times[i] - peak_times[i - 1])
            time_axis.append(peak_times[i] / 1000)

        fig, ax = plt.subplots(figsize=(12, 4))

        ax.plot(
            time_axis,
            rr_intervals,    
            marker="o",
            markerfacecolor="purple",
            markeredgecolor="purple"
        )

        ax.set_title("Herzratenvariabilität")
        ax.set_xlabel("Zeit [s]")
        ax.set_ylabel("RR-Intervall [ms]")
        ax.grid(True)

        st.pyplot(fig)

    def plot_heart_rate(self, df_plot=None, window=5):

        """
    Zeigt die Herzfrequenz als gleitenden Durchschnitt über die Zeit.
        """

        if df_plot is None:
            df_plot = self.df

        peaks_in_plot = [p for p in self.peaks if p in df_plot.index]

        if len(peaks_in_plot) < 2:
            st.warning("Zu wenige Peaks im ausgewählten Bereich.")
            return

        peak_times = df_plot.loc[peaks_in_plot, "Zeit in ms"].values

        heart_rates = []
        time_axis = []

        for i in range(1, len(peak_times)):

            rr = peak_times[i] - peak_times[i-1]

            bpm = 60000 / rr

            heart_rates.append(bpm)

            time_axis.append(peak_times[i] / 1000)

        # gleitender Durchschnitt
        hr_smooth = (
            pd.Series(heart_rates)
            .rolling(window=window, center=True)
            .mean()
        )

        fig, ax = plt.subplots(figsize=(12,4))

        ax.plot(
            time_axis,
            hr_smooth,
            color="purple",
            linewidth=2
        )

        ax.set_title("Herzrate")
        ax.set_xlabel("Zeit [s]")
        ax.set_ylabel("Herzfrequenz [BPM]")
        ax.grid(True)

        st.pyplot(fig)

    @classmethod
    def load_by_id(cls, ekg_id, path="data/person_db.json"):

        
        """Lädt ein EKG anhand seiner ID aus der Datenbank."""
        

        with open(path) as file:
            person_data = json.load(file)

        for person in person_data:
            for ekg_df in person["ekg_tests"]:
                if ekg_df["id"] == ekg_id:
                    return cls(ekg_df)
        
        raise ValueError(f"EKG mit ID {ekg_id} nicht gefunden")
    



if __name__ == "__main__":
    print("This is a module with some functions to read the EKG data")

    file = open("data/person_db.json")
    person_data = json.load(file)

    ekg_dict = person_data[0]["ekg_tests"][0]
    print(ekg_dict)

    ekg = EKGdata(ekg_dict)

    print("\nErste Zeilen des EKG:")
    print(ekg.df.head())

    peaks = ekg.find_peaks(threshold=350)

    print(f"\nAnzahl Peaks: {len(peaks)}")
    print("Peaks:")
    print(peaks[:20])  # erste 20 Peaks ausgeben

    ekg.plot_time_series()

    ekg2 = EKGdata.load_by_id(1)

    print(ekg2.id)
    print(ekg2.date)
    print(ekg2.data)