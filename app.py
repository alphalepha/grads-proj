import streamlit as st
from components.login import login
from datetime import datetime
import json
from components.utils import plot_performance_with_emojis, display_leaderboard, styling, custom_divider

st.set_page_config(page_title="grads game", layout="wide", page_icon='🥦')

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

styling()
col1, col2, col3 = st.columns([8, 1, 1])
col1.markdown("<span class='highlight'> Success depends upon previous preparation, and without such preparation, there is sure to be failure. </span> -- Confucius.", unsafe_allow_html=True)
if col2.button(label='Fiesta!', use_container_width=True):
    st.balloons()
if col3.button('Refresh data', use_container_width=True):
    st.rerun()
st.divider()

start_date = st.secrets["dates"]["start_date"]
end_date = (datetime.today()).strftime('%Y-%m-%d')
players_data = st.secrets["players"]["players"]  # JSON string

fig, fig_stocks, leaderboard_df = plot_performance_with_emojis(players_data, start_date, end_date)

if len(fig.data) == 0 and len(fig_stocks.data) == 0 and leaderboard_df.empty:
    st.warning('No data available.')
    st.stop()

col1, col2 = st.columns([8, 2])
col1.markdown("<H3 style='margin: 0;'><span class='highlight'>Performance Chart (Chart will reset when game starts officially)</span></H3>", unsafe_allow_html=True)
col1.plotly_chart(fig)
col2.markdown("<H3 style='margin: 0;'><span class='highlight'>LEADERBOARD</span></H3>", unsafe_allow_html=True)
col2.dataframe(display_leaderboard(leaderboard_df), hide_index=True, use_container_width=True)

custom_divider(color="#007BFF", thickness="3px", margin="20px 0")

st.markdown("<H5 style='margin: 0;'><span class='highlight'>Individual Stocks</span></H3>", unsafe_allow_html=True)
st.plotly_chart(fig_stocks)
