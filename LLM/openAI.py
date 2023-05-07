from typing import List
from LLM.prompt import get_adventure_prompt
import streamlit as st
import requests


def init_open_ai_config(api_key: str, open_ai_version: str):
    st.session_state.api_key = api_key
    if open_ai_version == "gpt-3":
        st.session_state.open_ai_version = "gpt-3.5-turbo"
    if open_ai_version == "gpt-4":
        st.session_state.open_ai_version = "gpt-4"


def call_openai_api(story: List[dict]):
    print(f"Getting the next sentence from OpenAI with the prompt: {story}")
    headers = {'Authorization': f'Bearer {st.session_state.api_key}'}

    adventure_prompt = get_adventure_prompt(st.session_state.language)
    adventure_prompt.extend(story)

    data = {
     "model": st.session_state.open_ai_version,
     "messages": adventure_prompt,
     "temperature": 0.7
    }
    try:
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    except:
        print("Error requesting")
    print(response.json())
    return {"role": "system", "content": response.json()['choices'][0]['message']['content'].strip()}