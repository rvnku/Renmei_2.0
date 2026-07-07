from typing import Dict
import json, re


VOWELS = 'аеёиоуыэюя'
CONSONANTS = 'бвгджзйклмнпрстфхцчшщ'
RARE_LETTERS = set('фщцэъё')
DISSONANT_CLUSTERS = ['вств', 'здр', 'рдц', 'лнц', 'стн', 'здн', 'сс', 'жж', 'чч', 'шш']


with open('assets/profanity.json', 'r') as file:
    profanity = json.load(file)


def count_consonant_clusters(word: str) -> int:
    clusters = re.findall(rf'[{CONSONANTS}]{{3,}}', word)
    return len(clusters)

def count_dissonant_transitions(word: str) -> int:
    count = 0
    for cluster in DISSONANT_CLUSTERS:
        count += word.count(cluster)
    return count

def count_rare_letters(word: str) -> int:
    return sum(1 for char in word if char in RARE_LETTERS)

def count_vowel_clusters(word: str) -> int:
    clusters = re.findall(rf'[{VOWELS}]{{2,}}', word)
    return len(clusters)

def count_long_vowel_clusters(word: str) -> int:
    clusters = re.findall(rf'[{VOWELS}]{{3,}}', word)
    return len(clusters)

def vowel_repetition_index(word: str) -> float:
    vowels_in_word = [c for c in word if c in VOWELS]
    if not vowels_in_word:
        return 0

    counts = {v: vowels_in_word.count(v) for v in set(vowels_in_word)}
    max_count = max(counts.values())
    return max_count / len(vowels_in_word)

def compact_word_penalty(word: str) -> float:
    if len(word) <= 7:
        return 0
    return (len(word) - 7) * 0.1

def analyze_word(word: str) -> Dict:
    return {
        'length': len(word),
        'NDT': count_consonant_clusters(word),
        'NDU': count_dissonant_transitions(word),
        'NIL': count_rare_letters(word),
        'VCT': count_vowel_clusters(word),
        'LVCT': count_long_vowel_clusters(word),
        'VRI': vowel_repetition_index(word),
        'length_penalty': compact_word_penalty(word),
    }

def get_euphopy(text: str) -> float:
    words = text.split()
    score = 0
    for word in words:
        if word in profanity:
            return 0.0

        data = analyze_word(word)

        alpha = 1.5   # согласные кластеры
        beta = 1.3    # проблемные сочетания
        gamma = 0.3   # редкие буквы
        delta = 1.1   # длина
        epsilon = 0.8 # 2+ гласных подряд
        zeta = 1.1    # 3+ гласных подряд
        eta = 0.3     # монотонность гласных

        penalty = (
            alpha * data['NDT'] +
            beta * data['NDU'] +
            gamma * data['NIL'] +
            delta * data['length_penalty'] +
            epsilon * data['VCT'] +
            zeta * data['LVCT'] +
            eta * data['VRI']
        )

        ei = 1 / (1 + penalty)
        score += ei

    return score / len(words)
