import json
from matplotlib import pyplot as plt
import pandas as pd
import streamlit as st
import plotly.graph_objects as go


class sleep_data:
    def __init__(self, result_link):
        self.result_link = result_link
        self.data = None
        

    def load_data(self):
        self.data = pd.read_csv(self.result_link)
        return self.data
    
    def filter_data(self):
        if self.data is None:
            self.load_data
        
        self.data["heart_rate_filtered"] = self.data["heart_rate"].rolling(
            window=5,
            min_periods=1,
            center=True
        ).mean()

        self.data["hrv_filtered"] = self.data["hrv"].rolling(
            window=5,
            min_periods=1,
            center=True
        ).median()

        self.data["spo2_filtered"] = self.data["spo2"].rolling(
            window=5,
            min_periods=1,
            center=True
        ).median()

        self.data["hrv_filtered"] = self.data["hrv"].rolling(
        window=5,
        center=True,
        min_periods=1
        ).mean()

        self.data["movement_filtered"] = self.data["movement"].rolling(
            window=5,
            center=True,
            min_periods=1
        ).mean()

        self.data["respiration_filtered"] = self.data["respiration_rate"].rolling(
            window=5,
            center=True,
            min_periods=1
        ).mean()

        return self.data
    
    
    def plot_heart_rate(self):
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=self.data.index,
                y=self.data["heart_rate_filtered"],   # ggf. Spaltenname anpassen
                mode="lines",
                name="Herzfrequenz",
                line=dict(color="red", width=2)
            )
        )

        fig.update_layout(
        title=dict(
            text="❤️ Herzfrequenz <span style='font-size:14px; color:#A8B3C7'>(bpm)</span>",
            x=0.02,
            y=0.95,
            xanchor="left",
            yanchor="top",
            font=dict(size=16, color="#E6EDF3"),
        ),

        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",

        font=dict(color="#E6EDF3"),

        height=220,
        margin=dict(l=40, r=25, t=45, b=35),

        xaxis=dict(
            title=None,
            showgrid=False,
            zeroline=False,
            showline=False,
            tickfont=dict(color="#A8B3C7"),
        ),

        yaxis=dict(
            title=None,
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)",
            zeroline=False,
            showline=False,
            tickfont=dict(color="#A8B3C7"),
        ),

        hovermode="x unified",
        showlegend=False,
        )

        fig.update_yaxes(range=[40, 100], dtick=25)

        return fig

    def plot_spo2_rate(self):
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=self.data.index,
                y=self.data["spo2_filtered"],   # ggf. Spaltenname anpassen
                mode="lines",
                name="Sauerstoffsättigung",
                line=dict(color="#4cc9f0", width=2)
            )
        )

        fig.update_layout(
        title=dict(
            text="💧 SpO₂ <span style='font-size:14px; color:#A8B3C7'>(%)</span>",
            x=0.02,
            y=0.95,
            xanchor="left",
            yanchor="top",
            font=dict(size=16, color="#E6EDF3"),
        ),

        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",

        font=dict(color="#E6EDF3"),

        height=220,
        margin=dict(l=40, r=25, t=45, b=35),

        xaxis=dict(
            title=None,
            showgrid=False,
            zeroline=False,
            showline=False,
            tickfont=dict(color="#A8B3C7"),
        ),

        yaxis=dict(
            title=None,
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)",
            zeroline=False,
            showline=False,
            tickfont=dict(color="#A8B3C7"),
        ),

        hovermode="x unified",
        showlegend=False,
        )

        fig.update_yaxes(range=[80, 100], dtick=5)

        return fig
    

    def calculate_sleep_phases(self):
        if self.data["heart_rate_filtered"] is None:
            self.filter_data()

        df = self.data.copy()

        # Grenzwerte dynamisch aus den eigenen Daten berechnen
        hr_low = df["heart_rate_filtered"].quantile(0.30)
        hr_high = df["heart_rate_filtered"].quantile(0.70)

        hrv_low = df["hrv_filtered"].quantile(0.30)
        hrv_high = df["hrv_filtered"].quantile(0.70)

        movement_low = df["movement_filtered"].quantile(0.30)
        movement_high = df["movement_filtered"].quantile(0.70)

        respiration_low = df["respiration_filtered"].quantile(0.30)
        respiration_high = df["respiration_filtered"].quantile(0.70)

        def classify_phase(row):
            hr = row["heart_rate_filtered"]
            hrv = row["hrv_filtered"]
            movement = row["movement_filtered"]
            respiration = row["respiration_filtered"]
            spo2 = row["spo2"]

            # Wach
            if movement >= movement_high and hr >= hr_high:
                return "Wach"

            # Tiefschlaf
            if hr <= hr_low and movement <= movement_low and respiration <= respiration_low:
                return "Tiefschlaf"

            # REM-Schlaf
            if hr >= hr_high and hrv >= hrv_high and movement <= movement_low:
                return "REM-Phase"

            # Leichter Schlaf
            return "leichter Schlaf"

        df["sleep_phase"] = df.apply(classify_phase, axis=1)

        self.data = df

        return df
    
if __name__ == "__main__":

    sleep = sleep_data("data/smartwatch_data/sleep_001.csv")

    sleep.load_data()
    sleep.filter_data()
    sleep.calculate_sleep_phases()

    print(sleep.data[[
        "timestamp",
        "heart_rate",
        "hrv",
        "spo2",
        "movement",
        "sleep_phase"
    ]].head(60))