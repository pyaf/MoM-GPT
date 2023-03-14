# MoM GPT! 🤗

A streamlit based application that creates minutes of the meetings (MoMs) with summary, discussion points, and action times in real time using ChatGPT API. It can also do the same using meeting transcripts.

Currently under development, feel free to contribute. 🤝

https://user-images.githubusercontent.com/17473589/222925358-70d5872b-05aa-4fa7-836a-e4d33a8751f9.mp4


### Installation 🛠️

1. Install requirements with `pip install -r requirements.txt`
2. Export your OpenAI API key `export OPENAI_API_KEY='XXXXX'`
3. Download neccessary nltk tokenizer `python -c 'import nltk; nltk.download("punkt")'`
4. Run the app `streamlit run app.py`

The app should open up automatically in your default browser.

### File formats

1. Google meet: Export the meeting transcript as a .docx file

2. Teams: Export the meeting trascript as a .vtt file. How to do it? [Check it out here](https://support.zoom.us/hc/en-us/articles/115004794983-Audio-transcription-for-cloud-recordings)

3. Zoom: Export the meeting transcript as a .vtt file. How to do it? [Check it out here](https://support.microsoft.com/en-us/office/view-live-transcription-in-a-teams-meeting-dc1a8f23-2e20-4684-885e-2152e06a4a8b)

### References

1. https://blog.devgenius.io/creating-meeting-minutes-using-openai-gpt-3-api-f79e5fc15eb1
2. https://openai.com/
3. https://github.com/streamlit/streamlit



