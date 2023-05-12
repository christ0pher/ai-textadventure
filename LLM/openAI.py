from typing import List
from LLM.prompt import get_adventure_rules
import streamlit as st
import openai


def init_open_ai_config(api_key: str, open_ai_version: str):
    st.session_state.api_key = api_key
    if open_ai_version == "gpt-3":
        st.session_state.open_ai_version = "gpt-3.5-turbo"
    if open_ai_version == "gpt-4":
        st.session_state.open_ai_version = "gpt-4"


def continue_story(story: List[dict]):
    print(f"Getting the next sentence from OpenAI with the prompt: {story}")
    openai.api_key = st.session_state.api_key

    prompt = get_adventure_rules(st.session_state.language) + story
    print(f"Prompt: {prompt}")

    adventure_prompt = openai.ChatCompletion.create(
        model=st.session_state.open_ai_version, 
        messages=prompt,
    )

    print(f"returned: {adventure_prompt}")
    continued_story = story + [dict(adventure_prompt.choices[0].message)]
    print(f"returned: {continued_story}")
    return continued_story