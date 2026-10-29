"""Text preprocessing utilities built on NLTK."""

from __future__ import annotations

import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer

# Words that look like stopwords but change the meaning of a question.
_KEEP_WORDS = {"not", "no", "can", "how", "what", "when", "where", "why", "do"}


def ensure_nltk_resources() -> None:
    """Download the required NLTK corpora on first run (no-op afterwards)."""
    resources = {
        "corpora/stopwords": "stopwords",
        "corpora/wordnet": "wordnet",
        "corpora/omw-1.4": "omw-1.4",
    }
    for path, name in resources.items():
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(name, quiet=True)


class TextPreprocessor:
    """Lowercase -> clean -> tokenize -> remove stopwords -> lemmatize."""

    def __init__(self) -> None:
        ensure_nltk_resources()
        self._tokenizer = RegexpTokenizer(r"[a-z0-9]+")
        self._lemmatizer = WordNetLemmatizer()
        self._stopwords = set(stopwords.words("english")) - _KEEP_WORDS

    def clean(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"https?://\S+", " ", text)  # remove URLs
        return re.sub(r"\s+", " ", text).strip()

    def tokenize(self, text: str) -> list[str]:
        return self._tokenizer.tokenize(self.clean(text))

    def preprocess(self, text: str) -> str:
        """Return the normalised text as a single space-separated string."""
        tokens = [t for t in self.tokenize(text) if t not in self._stopwords]
        tokens = [self._lemmatizer.lemmatize(t) for t in tokens]
        return " ".join(tokens)
