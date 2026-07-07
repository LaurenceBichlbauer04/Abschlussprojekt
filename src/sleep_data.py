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
            if (movement <= movement_low and hrv >= df["hrv_filtered"].median() and respiration >= df["respiration_filtered"].median()):
                return "REM-Phase"

            # Leichter Schlaf
            return "leichter Schlaf"

        df["sleep_phase"] = df.apply(classify_phase, axis=1)

        self.data = df

        return df
    
    def calculate_sleep_score(self):
        df = self.data.copy()

        df["timestamp"] = pd.to_datetime(df["timestamp"])

        start_time = df["timestamp"].min()
        end_time = df["timestamp"].max()

        sleep_duration_hours = (end_time - start_time).total_seconds() / 3600

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

        # Tiefschlaf
        if deep_sleep_ratio < 0.10:
            score -= 15
        elif deep_sleep_ratio < 0.15:
            score -= 8

        # REM-Schlaf
        if rem_sleep_ratio < 0.10:
            score -= 10
        elif rem_sleep_ratio < 0.15:
            score -= 5

        # Wachphasen / Bewegung
        if awake_ratio > 0.20:
            score -= 15
        elif awake_ratio > 0.10:
            score -= 8

        if avg_movement > df["movement"].quantile(0.75):
            score -= 5

        # Sauerstoffsättigung
        if avg_spo2 < 92:
            score -= 25
        elif avg_spo2 < 95:
            score -= 10

        if min_spo2 < 88:
            score -= 15
        elif min_spo2 < 90:
            score -= 8

        score = max(0, min(100, round(score)))

        # einfache Schlafapnoe-Warnung
        apnea_warning = False
        apnea_text = "Keine auffälligen Hinweise auf Schlafapnoe erkannt."

        low_spo2_events = df[df["spo2"] < 90]

        if len(low_spo2_events) > 3:
            apnea_warning = True
            apnea_text = (
                "Achtung: Es gibt auffällige SpO₂-Abfälle. "
                "Das kann ein Hinweis auf Atemaussetzer im Schlaf sein"
            )

        result = {
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

        return result
    
    def plot_sleep_phases(self):
        df = self.data.copy()

        df["timestamp"] = pd.to_datetime(df["timestamp"])

        phase_map = {
            "Tiefschlaf": 0,
            "leichter Schlaf": 1,
            "REM-Phase": 2,
            "Wach": 3
        }

        color_map = {
            "Tiefschlaf": "#0f4cbd",
            "leichter Schlaf": "#38bdf8",
            "REM-Phase": "#8b5cf6",
            "Wach": "#fb923c"
        }

        df["phase_value"] = df["sleep_phase"].map(phase_map)

        fig = go.Figure()

        for phase in ["Wach", "REM-Phase", "leichter Schlaf", "Tiefschlaf"]:
            phase_df = df[df["sleep_phase"] == phase]

            fig.add_trace(
                go.Scatter(
                    x=phase_df["timestamp"],
                    y=phase_df["phase_value"],
                    mode="markers",
                    name=phase,
                    marker=dict(
                        color=color_map[phase],
                        size=9,
                        symbol="square"
                    ),
                    hovertemplate=(
                        "Zeit: %{x|%H:%M}<br>"
                        f"Phase: {phase}<extra></extra>"
                    )
                )
            )

        fig.add_trace(
            go.Scatter(
                x=df["timestamp"],
                y=df["phase_value"],
                mode="lines",
                line=dict(
                    color="rgba(255,255,255,0.18)",
                    width=1,
                    shape="hv"
                ),
                showlegend=False,
                hoverinfo="skip"
            )
        )

        fig.update_layout(
            title=dict(
                text="Schlafphasen",
                x=0.02,
                y=0.95,
                xanchor="left",
                yanchor="top",
                font=dict(size=17, color="#E6EDF3")
            ),
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="#E6EDF3"),
            height=310,
            margin=dict(l=70, r=25, t=55, b=45),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                font=dict(color="#A8B3C7", size=12)
            ),
            xaxis=dict(
                title=None,
                showgrid=False,
                zeroline=False,
                tickfont=dict(color="#A8B3C7"),
                tickformat="%H:%M"
            ),
            yaxis=dict(
                title=None,
                tickmode="array",
                tickvals=[0, 1, 2, 3],
                ticktext=["Tiefschlaf", "Leichtschlaf", "REM-Phase", "Wach"],
                showgrid=True,
                gridcolor="rgba(255,255,255,0.08)",
                zeroline=False,
                tickfont=dict(color="#A8B3C7"),
                range=[-0.5, 3.5]
            ),
            hovermode="closest"
        )

        return fig
    
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