
import streamlit as st

from LLM.openAI import init_open_ai_config, continue_story, extract_story_interaction_json, extract_json
from game.constants import GamestatusEnum
from game.game_state import change_game_state_to


def init_session():
    if "story" not in st.session_state:
        clear_state()


def reset():
    print("reset")
    clear_state()
    change_game_state_to(GamestatusEnum.PREPARE_STORY)
    st.experimental_rerun()


def clear_state():
    print("clear state")
    st.session_state.story = []
    st.session_state.current_interaction = 0
    st.session_state.game_status = GamestatusEnum.INIT
    st.session_state.story_start = ""
    st.session_state.language = "de"


def display_story():
    story_teller_responses = list(filter(lambda story_part: story_part["role"] == "assistant", st.session_state.story))
    for story_part in story_teller_responses:
        print(f'display: {story_part["content"]}')
        story = extract_json(story_part["content"])
        st.write(story["story_part"])

def continue_story_with_prompt(prompt: str):
    st.session_state.story = continue_story(
        st.session_state.story + [{"role": "user", "content": prompt}]
    )

def main():
    st.set_page_config(page_title="The AI Textadventure", page_icon="🤖")
    st.title("Text Adventure Game")
    if st.session_state.game_status == GamestatusEnum.INIT:
        st.write(
            "Willkommen zu unserem Text Adventure Game. Um das Spiel zu starten, wähle einen Geschichten start aus und klicke auf Start.")
        st.write("Wir brauchen deinen OpenAI Api Key um die Geschichte zu starten. Wir behalten den Key nur in der Session.")
        open_ai_api_key = st.text_input("OpenAI API Key")
        open_ai_version = st.radio("OpenAI Version", ["gpt-3", "gpt-4"])
        if st.button("Start"):
            init_open_ai_config(open_ai_api_key, open_ai_version)
            change_game_state_to(GamestatusEnum.PREPARE_STORY)

    if st.session_state.game_status == GamestatusEnum.PREPARE_STORY:
        st.write("Willkommen zu unserem Text Adventure Game. Um das Spiel zu starten, wähle einen Geschichten start aus und klicke auf Start.")
        story_start = st.text_input(label="Geschichten Start", value="Ein kleiner Igel möchte zum Mond fliegen.")
        language = st.text_input("Sprache")
        if st.button("Start"):
            st.session_state.game_started = True
            st.session_state.story_start = story_start
            if language:
                st.session_state.language = language
            else:
                st.session_state.language = "de"
            continue_story_with_prompt(story_start)
            change_game_state_to(GamestatusEnum.STARTED)

    if st.session_state.game_status == GamestatusEnum.STARTED:
        if st.session_state.current_interaction < 9:
            display_story()
            st.divider()
            with st.form("Was passiert als nächstes und welche Entscheidungen stehen dem Protagonisten zur Verfügung?"):
                story_interaction = extract_story_interaction_json(st.session_state.story)
                st.write(story_interaction["story_part"])
                options = [story_interaction["option_a"], story_interaction["option_b"], story_interaction["option_c"]]
                radio_selection = st.radio("Optionen", options, horizontal=False)
                submitted = st.form_submit_button("Weiter")
                if submitted:
                    continue_story_with_prompt(radio_selection)
                    st.session_state.current_interaction += 1
                    st.experimental_rerun()
        else:
            change_game_state_to(GamestatusEnum.FINISHED)

    if st.session_state.game_status == GamestatusEnum.FINISHED:
        st.write("Das Spiel ist zu Ende. Du kannst es neu starten.")
        st.divider()
        display_story()
        st.divider()
        if st.button("Neu starten"):
            reset()





if __name__ == "__main__":
    init_session()
    main()
