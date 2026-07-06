import streamlit as st
import pandas as pd
from src.sleep_data import sleep_data

def show():
    st.markdown(
    """
    <style>
    [data-testid="stPlotlyChart"] {
        background: #0f172a;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.set_page_config(
        page_title="Schlafanalyse",
        page_icon="💤",
        layout="wide"
    )
    
    st.title("Schlafanalyse")

    person = st.session_state.user

    
    st.write(person.get_full_name())
    #st.write(person.smartwatch_data)
    data = person.smartwatch_data
    file = data[0]["result_link"]
    
    
    sleep001 = sleep_data(file)
    sleep001.load_data()
    sleep001.filter_data()
    print(sleep001.data)
    fig = sleep001.plot_heart_rate()
    fig2 = sleep001.plot_spo2_rate()

    cols = st.columns(2)

    with cols[0]:

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with cols[1]:  
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    
    
