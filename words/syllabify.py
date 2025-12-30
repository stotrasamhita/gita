#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unicodedata
import json
from collections import defaultdict

# -----------------------------
# Unicode character categories
# -----------------------------

DEVANAGARI_START = 0x0900
DEVANAGARI_END   = 0x097F

VIRAMA = "\u094D"

INDEPENDENT_VOWELS = set(chr(c) for c in range(0x0904, 0x0915))
CONSONANTS = set(chr(c) for c in range(0x0915, 0x093A))
VOWEL_SIGNS = set(chr(c) for c in range(0x093E, 0x094D))
DIACRITICS = {"\u0902", "\u0903", "\u0901"}  # anusvara, visarga, chandrabindu

ZWJ = "\u200D"
ZWNJ = "\u200C"


# -----------------------------
# Normalization
# -----------------------------

def normalize_word(word: str) -> str:
    word = word.strip()
    word = unicodedata.normalize("NFC", word)
    word = word.replace(ZWJ, "").replace(ZWNJ, "")
    return word


# -----------------------------
# Akṣara segmentation
# -----------------------------

def split_into_aksharas(word: str) -> list[str]:
    aksharas = []
    i = 0
    n = len(word)

    while i < n:
        ch = word[i]

        # Independent vowel
        if ch in INDEPENDENT_VOWELS:
            ak = ch
            i += 1

            # absorb diacritics
            while i < n and word[i] in DIACRITICS:
                ak += word[i]
                i += 1

            aksharas.append(ak)
            continue

        # Consonant cluster
        if ch in CONSONANTS:
            ak = ch
            i += 1

            # absorb virama + consonant sequences
            while i + 1 < n and word[i] == VIRAMA and word[i + 1] in CONSONANTS:
                ak += word[i] + word[i + 1]
                i += 2

            # absorb terminal virama (e.g. म्)
            if i < n and word[i] == VIRAMA:
                ak += word[i]
                i += 1


            # absorb vowel sign (if any)
            if i < n and word[i] in VOWEL_SIGNS and word[i] != VIRAMA:
                ak += word[i]
                i += 1

            # absorb diacritics
            while i < n and word[i] in DIACRITICS:
                ak += word[i]
                i += 1

            aksharas.append(ak)
            continue

        # Fallback: unexpected character
        # Attach it as a standalone unit to avoid silent data loss
        aksharas.append(ch)
        i += 1

    return aksharas


# -----------------------------
# Main processing
# -----------------------------

def process_file(input_path):
    words = []

    input_basename = input_path.split('.')[0]
    count_output_path = input_basename + '-counts.txt'
    json_output_path = input_basename + '-syllables.json'

    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            w = normalize_word(line)
            if w:
                words.append(w)

    syllable_index = defaultdict(set)

    with open(count_output_path, "w", encoding="utf-8") as out:
        for word in words:
            syllables = split_into_aksharas(word)
            count = len(syllables)

            # Output 1: word,count
            out.write(f"{word},{count}\n")

            # Prepare syllabified form
            syllabified_word = " ".join(syllables)

            # Output 2: syllable → words
            for syl in syllables:
                syllable_index[syl].add(syllabified_word)

    # Convert sets to sorted lists
    syllable_index = {
        syl: sorted(words)
        for syl, words in syllable_index.items()
    }

    with open(json_output_path, "w", encoding="utf-8") as jf:
        json.dump(syllable_index, jf, ensure_ascii=False, indent=2)


# -----------------------------
# CLI entry point
# -----------------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python syllabify.py <input.txt>")
        sys.exit(1)

    process_file(sys.argv[1])
