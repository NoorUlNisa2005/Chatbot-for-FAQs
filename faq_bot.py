"""Core FAQ chatbot engine: TF-IDF vectors + cosine similarity matching."""

from __future__ import annotations

import json
import random
import re
from dataclasses import dataclass, field
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nlp_utils import TextPreprocessor

DEFAULT_FAQ_PATH = Path(__file__).parent / "faqs.json"

SMALL_TALK = [
    (re.compile(r"\b(hi|hello|hey|good (morning|afternoon|evening))\b", re.I),
     ["Hello! 👋 How can I help you today?", "Hi there! Ask me anything about our store."]),
    (re.compile(r"\b(thanks?|thank you|thx)\b", re.I),
     ["You're welcome! Anything else I can help with?", "Happy to help! 😊"]),
    (re.compile(r"\b(bye|goodbye|see you|quit|exit)\b", re.I),
     ["Goodbye! Have a great day! 👋"]),
]

FALLBACK = ("I'm sorry, I couldn't find a good answer to that. "
            "Please try rephrasing, or contact support@shopeasy.example.")


@dataclass
class BotReply:
    answer: str
    score: float = 0.0
    matched_question: str | None = None
    suggestions: list[str] = field(default_factory=list)
    is_fallback: bool = False


class FAQChatbot:
    def __init__(self, faq_path: str | Path = DEFAULT_FAQ_PATH, threshold: float = 0.25) -> None:
        self.threshold = threshold
        self.faqs = self._load_faqs(faq_path)
        self.preprocessor = TextPreprocessor()

        self._processed = [self.preprocessor.preprocess(f["question"]) for f in self.faqs]
        self._vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self._matrix = self._vectorizer.fit_transform(self._processed)

    @staticmethod
    def _load_faqs(path: str | Path) -> list[dict]:
        with open(path, "r", encoding="utf-8") as fh:
            faqs = json.load(fh)
        if not faqs:
            raise ValueError("The FAQ file is empty.")
        return faqs

    def _small_talk(self, text: str) -> BotReply | None:
        for pattern, replies in SMALL_TALK:
            if pattern.search(text) and len(text.split()) <= 4:
                return BotReply(answer=random.choice(replies))
        return None

    def get_response(self, user_input: str, top_k: int = 3) -> BotReply:
        user_input = user_input.strip()
        if not user_input:
            return BotReply("Please type a question.", is_fallback=True)

        talk = self._small_talk(user_input)
        if talk:
            return talk

        query = self.preprocessor.preprocess(user_input)
        if not query:
            return BotReply(FALLBACK, is_fallback=True)

        scores = cosine_similarity(self._vectorizer.transform([query]), self._matrix).ravel()
        ranked = scores.argsort()[::-1]
        best = int(ranked[0])

        if scores[best] < self.threshold:
            hints = [self.faqs[i]["question"] for i in ranked[:top_k] if scores[i] > 0.05]
            return BotReply(FALLBACK, float(scores[best]), suggestions=hints, is_fallback=True)

        others = [self.faqs[i]["question"] for i in ranked[1:top_k] if scores[i] > 0.1]
        return BotReply(
            answer=self.faqs[best]["answer"],
            score=float(scores[best]),
            matched_question=self.faqs[best]["question"],
            suggestions=others,
        )
