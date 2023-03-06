import os
from os.path import splitext, exists
import re
from io import StringIO
import datetime

import nltk
import docx2txt
import streamlit as st
from nltk.tokenize import word_tokenize


def clean_transcript(filepath: str) -> str:
    """Clean up the content of a subtitle file (vtt) to a string
    Args:
        filepath (str): path to vtt file
    Returns:
        str: clean content
    """
    if filepath.endswith(".vtt"):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    elif filepath.endswith(".docx"):
        content = docx2txt.process(filepath)
    else:
        print("Invalid file format.")
        return

    # replace <v> tags
    content = content.replace("<v ","").replace(">"," ").replace("</v","")

    # remove header & empty lines
    lines = [line.strip() for line in content.split("\n") if line.strip()]
    lines = lines[1:] if "WEBVTT" in lines[0].upper() else lines


    # remove indexes
    lines = [lines[i] for i in range(len(lines)) if not lines[i].isdigit()]

    # remove tcode
    pattern = r'[a-f\d]{8}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{12}\/\d+-\d'

    no_tcode_lines = [lines[i] for i in range(len(lines))
             if not re.match(pattern, lines[i])]
    if len(no_tcode_lines) < len(lines):
        st.write("Participant names were found to be encrypted in the transcript file. The app will summarize accordingly.\n")
        lines = no_tcode_lines

    # remove timestamps
    lines = [lines[i] for i in range(len(lines)) if "--" not in lines[i]]    # remove timestamps

    content = " ".join(lines)

    # remove duplicate spaces
    pattern = r"\s+"
    content = re.sub(pattern, r" ", content)

    # add space after punctuation marks if it doesn't exist
    pattern = r"([\.!?])(\w)"
    content = re.sub(pattern, r"\1 \2", content)

    return content


def vtt_to_clean_file(file_in: str, file_out=None, **kwargs) -> str:
    """Save clean content of a subtitle file to text file

    Args:
        file_in (str): path to vtt file
        file_out (None, optional): path to text file
        **kwargs (optional): arguments for other parameters
            - no_message (bool): do not show message of result.
                                 Default is False

    Returns:
        str: path to text file
    """
    # set default values
    no_message = kwargs.get("no_message", False)
    if not file_out:
        filename = splitext(file_in)[0]
        file_out = "%s.txt" % filename
        i = 0
        while exists(file_out):
            i += 1
            file_out = "%s_%s.txt" % (filename, i)

    content = clean_transcript(file_in)
    with open(file_out, "w+", encoding="utf-8") as fp:
        fp.write(content)
    if not no_message:
        print("clean content is written to file: %s" % file_out)

    return file_out


def count_tokens(filename):
    with open(filename, "r") as f:
        text = f.read()
    tokens = word_tokenize(text)
    return len(tokens)


def break_up_file(tokens, chunk_size, overlap_size):
    if len(tokens) <= chunk_size:
        yield tokens
    else:
        chunk = tokens[:chunk_size]
        yield chunk
        yield from break_up_file(
            tokens[chunk_size - overlap_size :], chunk_size, overlap_size
        )


def break_up_file_to_chunks(filename, chunk_size=2000, overlap_size=100):
    with open(filename, "r") as f:
        text = f.read()
    try:
        tokens = word_tokenize(text)
    except Exception as err:
        print(err)
        nltk.download('punkt')
    return list(break_up_file(tokens, chunk_size, overlap_size))


def convert_to_prompt_text(tokenized_text):
    prompt_text = " ".join(tokenized_text)
    prompt_text = prompt_text.replace(" 's", "'s")
    return prompt_text

@st.cache_data
def save_and_clean_file(uploaded_file):
    # To convert to a string based IO
    #stringio = StringIO(uploaded_file.getvalue()).decode("utf-7"))
    filename = uploaded_file.name
    file_in = f"tmp/{filename}"
    file_out = "".join(file_in.split('.')[:-1]) + "_cleaned.txt"
    # save the file temporarily
    with open(file_in, mode="wb") as f:
        f.write(uploaded_file.getvalue())
    filepath = vtt_to_clean_file(file_in, file_out)
    return filepath


