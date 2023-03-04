import streamlit as st
from gpt import get_meeting_summary, get_action_items
from transcripts import save_and_clean_file, count_tokens


st.markdown("# Welcome to MoM GPT! 🤗")
st.markdown(
    "##### This app lets you create minutes of the meetings (MoMs) with summary, discussion points, and action times in real time using ChatGPT."
)
st.markdown(
    "##### And guess what, you can also use the meeting transcripts to do the same. 😉"
)

st.markdown("")
uploaded_file = st.file_uploader("Choose your transcript file")


if uploaded_file is not None:
    latest_iteration = st.empty()
    bar = st.progress(0)

    status = st.text("Uploading and Cleaning file...")
    filepath = save_and_clean_file(uploaded_file)
    print(filepath)
    status.text("Uploading and Cleaning file... Done")
    bar.progress(10)

    #token_count = count_tokens(filepath)
    #st.write(f"Number of tokens: {token_count}")

    status.text("Creating a summary...")
    meeting_summary = get_meeting_summary(filepath)
    status.text("Creating a summary... Done")
    st.markdown("#### Meeting Summary")
    st.markdown(meeting_summary)
    bar.progress(50)

    status.text("Extracting action items...")
    action_items = get_action_items(filepath)
    status.text("")
    st.markdown("#### Action Items")
    st.markdown(action_items)
    bar.progress(100)

    st.markdown("#### Hope it helped!")
    st.balloons()

footer = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    text-align: center;
}
</style>
<div class="footer">
    <p>Developed with ❤️  by <a style="text-decoration: none;" href="https://github.com/pyaf/">pyaf</a></p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
