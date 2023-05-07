from game.constants import GamestatusEnum
import streamlit as st


def change_game_state_to(state_to_enter: GamestatusEnum):
    st.session_state.game_status = state_to_enter
    st.experimental_rerun()
