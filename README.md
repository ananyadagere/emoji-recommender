**README.md**  

# Emoji Recommender  

## Description  
The Emoji Recommender is a real-time tool that suggests relevant emojis based on the user's input. It analyzes text for emotions, sarcasm, and Gen Z slang to provide accurate emoji recommendations. Users can click on suggested emojis to insert them into their text.  

## Features  
- Detects emotions using an NLP model and suggests appropriate emojis.  
- Recognizes Gen Z slang and maps it to relevant emojis.  
- Fetches emoji data from an online dataset to provide context-based recommendations.  
- Interactive UI with clickable emoji suggestions.  

## Technologies Used  
- Python  
- Transformers (Hugging Face)  
- NLP (SpaCy, NLTK)  
- IPyWidgets (for interactive UI in Google Colab)  
- Requests (for fetching emoji dataset)  

## Installation  
```bash
pip install requests transformers torch spacy fuzzywuzzy nltk emoji==2.2.0  
python -m spacy download en_core_web_sm  
```

## Usage  
Run the script in Google Colab or a Jupyter Notebook to start typing and receive emoji recommendations in real time.
