import string
from collections import Counter
from typing import Dict

def word_frequency(filepath: str) -> Dict[str, int]:
    """Return a dict mapping each word to its frequency in the file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{filepath}' does not exist.")

    # Normalize words: lowercase and strip punctuation
    translator = str.maketrans('', '', string.punctuation)
    words = text.lower().translate(translator).split()

    # Count frequencies
    freq = Counter(words)

    # Sort by frequency descending
    sorted_freq = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

    return sorted_freq


if __name__ == '__main__':
    freq = word_frequency('sample.txt')
    top_5 = list(freq.items())[:5]
    for word, count in top_5:
        print(f'{word}: {count}')
