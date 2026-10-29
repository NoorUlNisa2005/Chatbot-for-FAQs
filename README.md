# FAQ Chatbot (NLP)

Matches a user's question to the most similar FAQ using NLTK preprocessing,
TF-IDF vectors and cosine similarity.

## Setup (VS Code terminal)
    python -m venv venv
    venv\Scripts\activate          # Windows   (Mac/Linux: source venv/bin/activate)
    pip install -r requirements.txt

## Run
    python main_cli.py    # terminal chatbot
    python main_gui.py    # chat window (optional UI)

The first run downloads small NLTK data packages (internet required once).

## Customise
Edit `faqs.json` with your own questions/answers. Tune `threshold` in `FAQChatbot`.
