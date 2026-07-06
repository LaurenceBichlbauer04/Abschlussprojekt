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
            text="♡ Herzfrequenz <span style='font-size:14px; color:#A8B3C7'>(bpm)</span>",
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
            text="💧 SpO₂ <span style='font-size:14px; color:#A8B3C7'>(bpm)</span>",
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