# -*- coding: utf-8 -*-
"""emojiGenerator.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14evDL1HJUxzNmOAZ0RgRkp-8jm_Ikeaw
"""

# Install required libraries
!pip install requests transformers torch spacy fuzzywuzzy nltk emoji==2.2.0
!python -m spacy download en_core_web_sm

# Import libraries
import requests
import json
from transformers import pipeline
from IPython.display import display
import ipywidgets as widgets

# Load emotion detection pipeline
emotion_analyzer = pipeline("text-classification", model="joeddav/distilbert-base-uncased-go-emotions-student")

# Gen Z slang dictionary
gen_z_slang = {
    "fire": "🔥",
    "dead": "💀",
    "ded": "💀",
    "lit": "🎉",
    "sick": "🤒",
    "goat": "🐐",
    "mood": "😔",
    "clown": "🤡",
    "salty": "🧂",
    "ghost": "👻",
    "flex": "💪",
}

# Emotion-to-emoji mapping
emotion_to_emoji = {
    "joy": "😊",
    "excitement": "😃",
    "surprise": "😲",
    "sadness": "😢",
    "anger": "😡",
    "fear": "😨",
    "disgust": "🤢",
    "neutral": "😐",
}

# Fetch the emoji dataset from GitHub
url = "https://raw.githubusercontent.com/github/gemoji/refs/heads/master/db/emoji.json"
response = requests.get(url)
if response.status_code == 200:
    emoji_data = response.json()  # Load JSON data
else:
    raise Exception(f"Failed to fetch dataset. Status code: {response.status_code}")

# Function to recommend emojis
def recommend_emojis(text):
    # Convert text to lowercase for case-insensitive matching
    text_lower = text.lower()

    # Step 1: Check for Gen Z slang
    slang_emojis = []
    for slang_word, emoji_char in gen_z_slang.items():
        if slang_word in text_lower:
            slang_emojis.append(emoji_char)
    if slang_emojis:
        return slang_emojis

    # Step 2: Detect emotion if no slang is found
    emotion_result = emotion_analyzer(text)[0]
    emotion = emotion_result["label"]
    emotion_score = emotion_result["score"]
    if emotion in emotion_to_emoji:
        return [emotion_to_emoji[emotion]]

    # Step 3: Check for other emojis based on keywords in the dataset
    recommended_emojis = []
    for emoji_entry in emoji_data:
        description = emoji_entry["description"].lower()
        aliases = [alias.lower() for alias in emoji_entry["aliases"]]
        tags = [tag.lower() for tag in emoji_entry["tags"]]

        # Check if any word in the input matches the description, aliases, or tags
        if any(word in description for word in text_lower.split()) or \
           any(word in aliases for word in text_lower.split()) or \
           any(word in tags for word in text_lower.split()):
            recommended_emojis.append(emoji_entry["emoji"])

    # Default to neutral emoji if no slang, emotion, or keywords are detected
    if not recommended_emojis:
        recommended_emojis.append("😐")

    return recommended_emojis

# Text input widget
text_input = widgets.Text(placeholder="Type something...")
output = widgets.Output()
emoji_buttons = widgets.HBox()  # Container for emoji buttons

# Function to handle input changes
def on_type(change):
    with output:
        output.clear_output()
        text = change["new"]
        if text.strip():  # Only process if text is not empty
            emojis = recommend_emojis(text)
            # Clear previous emoji buttons
            emoji_buttons.children = []
            # Create a button for each recommended emoji
            for emoji_char in emojis:
                button = widgets.Button(description=emoji_char, layout=widgets.Layout(width="auto"))
                button.on_click(lambda b, emoji=emoji_char: on_emoji_click(emoji))
                emoji_buttons.children += (button,)
            print("Recommended Emojis:")
            display(emoji_buttons)

# Function to handle emoji button clicks
def on_emoji_click(emoji_char):
    # Append the clicked emoji to the text input
    text_input.value += emoji_char

# Attach the handler to the text input
text_input.observe(on_type, names="value")

# Display the input and output widgets
display(text_input, output)