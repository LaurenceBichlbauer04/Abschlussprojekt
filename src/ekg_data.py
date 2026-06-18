import json
from matplotlib import pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st
# %% Objekt-Welt

# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

class EKGdata:

## Konstruktor der Klasse soll die Daten einlesen

    def __init__(self, ekg_dict):
        #pass
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',])
       # self.df = self.df.iloc[:5000]  # Entferne die erste Zeile, da sie nur die Spaltennamen enthält
        self.peaks = 0

    def plot_time_series(self):

        # Erstellte einen Line Plot, der ersten 2000 Werte mit der Zeit aus der x-Achse
        self.fig = px.line(self.df.head(2000), x="Zeit in ms", y="Messwerte in mV")
        #return self.fig 

    def find_peaks(self, threshold = 0, respacing_factor = 5):
        series = self.df["Messwerte in mV"]
        series = series.iloc[::respacing_factor]
    
        # Filter the series
        #series = series[series>threshold]


        peaks = []
        last = 0
        current = 0
        next = 0

        for index, row in series.items():
            last = current
            current = next
            next = row

            if last < current and current > next and current > threshold:
                peaks.append(index-respacing_factor)
        
        self.peaks = peaks
        return peaks

    def plot_time_series(self):
        if self.peaks == 0:
            self.find_peaks()
        
        fig, ax = plt.subplots(figsize=(12, 5))

        ax.plot(
            self.df["Zeit in ms"],
            self.df["Messwerte in mV"],
            label="EKG"
        )

        ax.scatter(
            self.df.loc[self.peaks, "Zeit in ms"],
            self.df.loc[self.peaks, "Messwerte in mV"],
            color="red",
            label="Peaks"
        )

        ax.set_xlabel("Zeit [ms]")
        ax.set_ylabel("Spannung [mV]")
        ax.set_title("EKG mit Peaks")
        ax.legend()

        st.pyplot(fig)
    
    @classmethod
    def load_by_id(cls, ekg_id, path="data/person_db.json"):
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