import json
from matplotlib import pyplot as plt
import pandas as pd
import streamlit as st

class EKGdata:

    """Verwaltet das Einlesen, Analysieren und Darstellen von EKG-Messdaten."""

    def __init__(self, ekg_dict):
        #pass
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',]).iloc[::2].reset_index(drop=True)
        self.peaks = []


    def find_peaks(self, threshold=0, respacing_factor=5):

        """
        Erkennt lokale Maxima im EKG-Signal.

        Es werden nur Peaks oberhalb des Schwellwertes erkannt.
        Der Parameter respacing_factor legt den Mindestabstand
        zwischen zwei erkannten Peaks fest.
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
    
    @classmethod
    def load_by_id(cls, ekg_id, path="data/person_db.json"):

        """
        Lädt anhand der EKG-ID den zugehörigen Datensatz aus der JSON-Datei.
        """

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