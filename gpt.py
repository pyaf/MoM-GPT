import os
import openai
import streamlit as st
from transcripts import convert_to_prompt_text, break_up_file_to_chunks


def davinci_request(
    prompt_request,
    temperature=0.5,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
):
    """Uses OpenAI's completion API to interact with 'text-davinci-003' model"""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_request,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )
    return response["choices"][0]["text"].strip()

@st.cache_data
def get_meeting_summary(filepath):
    """Function for getting the meeting summary from a meeting transcript file"""
    # summarize the transcript chunk-wise
    prompt_response = []
    chunks = break_up_file_to_chunks(filepath)
    for i, chunk in enumerate(chunks):
        prompt_request = "Summarize this meeting transcript: " + convert_to_prompt_text(
            chunks[i]
        )
        response = davinci_request(prompt_request)
        prompt_response.append(response)

    # consolidate all the chunk-wise summaries to create a master summary
    prompt_request = "Consoloidate these meeting summaries: " + str(prompt_response)
    meeting_summary = davinci_request(prompt_request)
    return meeting_summary

@st.cache_data
def get_action_items(filepath):
    """Function for getting the action items from a meeting transcript file"""
    # extract action items chunkwise
    action_response = []
    chunks = break_up_file_to_chunks(filepath)
    for i, chunk in enumerate(chunks):
        prompt_request = (
            "Provide a list of action items with a due date from the provided meeting transcript text: "
            + convert_to_prompt_text(chunks[i])
        )
        response = davinci_request(prompt_request)
        action_response.append(response)

    # consolidate all the chunk-wise action items
    prompt_request = "Consoloidate these meeting action items: " + str(action_response)
    meeting_action_items = davinci_request(prompt_request)
    return meeting_action_items
