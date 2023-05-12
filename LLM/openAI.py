from json import JSONDecodeError
from typing import List
from LLM.prompt import get_adventure_rules
import streamlit as st
import openai
import re
import json


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

    print(f"Response: {adventure_prompt}")
    continued_story = story + [dict(adventure_prompt.choices[0].message)]
    print(f"Continued: {continued_story}")
    return continued_story


def extract_story_interaction_json(story: list) -> dict:
    last_response = story[-1]
    assert last_response["role"] == "assistant"
    return extract_json(last_response["content"])


def extract_json(response_content: str) -> dict:
    # Extract story response as json 
    pattern = r"```json(.*?)```"
    match = re.search(pattern, response_content, re.DOTALL)
    
    if match:
        extracted_json = json.loads(match.group(1).strip())
    else:
        try:
            extracted_json = json.loads(response_content)
        except JSONDecodeError:
            extracted_json = {"story_part": response_content}

    print(f'extracted_json: {extracted_json}')
    return dict(extracted_json)
