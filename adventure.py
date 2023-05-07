from typing import List

import streamlit as st
import requests

from constants import GamestatusEnum


def change_game_state_to(state_to_enter: GamestatusEnum):
    st.session_state.game_status = state_to_enter
    st.experimental_rerun()


def init_open_ai_config(api_key: str, open_ai_version: str):
    st.session_state.api_key = api_key
    if open_ai_version == "gpt-3":
        st.session_state.open_ai_version = "gpt-3.5-turbo"
    if open_ai_version == "gpt-4":
        st.session_state.open_ai_version = "gpt-4"


def call_openai_api(story: List[dict]):
    print(f"Getting the next sentence from OpenAI with the prompt: {story}")
    headers = {'Authorization': f'Bearer {st.session_state.api_key}'}

    game_state = [{"role": "system", "content": "You are a game master for a text adventure."},
                  {"role": "system", "content": "The user is the player in this text adventure."},
                  {"role": "system", "content": """Der Spieler will eine Spannende Geschichte spielen. Ein Spiel dauert 10 Iteraktionen. In jeder interaktion hat der Spieler 3 optionen (A,B,C) aus denen der Spieler wählen muss wie die Geschichte weitergeht. Du wartest bei jeder Interaktion darauf, dass der Spieler eine Option ausgewählt hat. Der Spieler kennt ich immer nur die aktuelle Interaktion und neue Interaktionen werden erst generiert, wenn der Spieler eine Option gewählt hat."""},
                  ]
    game_state.extend(story)
    data = {
     "model": st.session_state.open_ai_version,
     "messages": game_state,
     "temperature": 0.7
    }
    try:
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    except:
        print("Error requesting")
    print(response.json())
    return {"role": "system", "content": response.json()['choices'][0]['message']['content'].strip()}


def init_session():
    if "story" not in st.session_state:
        print("Initializing session state")
        st.session_state.story = []
        st.session_state.current_interaction = 0
        st.session_state.game_status = GamestatusEnum.INIT
        st.session_state.story_start = ""


def main():
    st.set_page_config(page_title="The AI Textadventure", page_icon="🤖")
    st.title("Text Adventure Game")
    if st.session_state.game_status == GamestatusEnum.INIT:
        st.write(
            "Willkommen zu unserem Text Adventure Game. Um das Spiel zu starten, wähle einen Geschichten start aus und klicke auf Start.")
        st.write("Wir brauchen deinen OpenAI Api Key um die Geschichte zu starten. Wir behaletn den Key nur in der Session.")
        open_ai_api_key = st.text_input("OpenAI API Key")
        open_ai_version = st.radio("OpenAI Version", ["gpt-3", "gpt-4"])
        if st.button("Start"):
            init_open_ai_config(open_ai_api_key, open_ai_version)
            change_game_state_to(GamestatusEnum.PREPARE_STORY)

    if st.session_state.game_status == GamestatusEnum.PREPARE_STORY:
        print("Game not started")
        st.write("Willkommen zu unserem Text Adventure Game. Um das Spiel zu starten, wähle einen Geschichten start aus und klicke auf Start.")
        story_start = st.text_input("Geschichten Start")
        if st.button("Start"):
            st.session_state.game_started = True
            st.session_state.story_start = story_start
            st.session_state.story = [{"role": "user", "content": story_start}]
            new_story_part = call_openai_api(st.session_state.story)
            st.session_state.story.append(new_story_part)
            change_game_state_to(GamestatusEnum.STARTED)

    if st.session_state.game_status == GamestatusEnum.STARTED:
        if st.session_state.current_interaction < 9:
            for story_part in st.session_state.story[:-1]:
                st.write(story_part["content"])
            with st.form("Was passiert als nächstes und welche Entscheidungen stehen dem Protagonisten zur Verfügung?"):
                st.write(st.session_state.story[-1]["content"])
                radio_selection = st.radio("Optionen", ["A", "B", "C"])
                # Every form must have a submit button.
                submitted = st.form_submit_button("Weiter")
                if submitted:
                    st.session_state.story.append(
                        {"role": "user", "content": radio_selection})
                    next_part = call_openai_api(st.session_state.story)
                    st.session_state.story.append(next_part)
                    st.session_state.current_interaction += 1
                    st.experimental_rerun()


if __name__ == "__main__":
    print("Starting the game")
    init_session()
    main()
