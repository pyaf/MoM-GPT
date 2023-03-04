# MoM GPT! 🤗

A streamlit based application that creates minutes of the meetings (MoMs) with summary, discussion points, and action times in real time using ChatGPT API. It can also do the same using meeting transcripts.

Currently under development, feel free to contribute. 🤝

[!(demo)](tmp/demo.mp4)

### Installation 🛠️

1. Install requirements with `pip install -r requirements.txt`
2. Export your OpenAI API key `export OPENAI_API_KEY='XXXXX'`
3. Download neccessary nltk tokenizer `python -c 'import nltk; nltk.download("punkt")'`
4. Run the app `streamlit run app.py`

The app should open up automatically in your default browser.

### References

1. https://blog.devgenius.io/creating-meeting-minutes-using-openai-gpt-3-api-f79e5fc15eb1
2. https://openai.com/
3. https://github.com/streamlit/streamlit
