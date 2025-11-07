"""Download required NLTK data for sentiment analysis."""

import nltk

try:
    nltk.data.find("vader_lexicon")
    print("✅ VADER lexicon already downloaded")
except LookupError:
    print("Downloading VADER lexicon...")
    nltk.download("vader_lexicon", quiet=True)
    print("✅ VADER lexicon downloaded successfully")

