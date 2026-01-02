#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from collections import defaultdict

# --- Configuration ---
MOOLA_FILE = 'gita.tex'
SPLIT_FILE = 'words/gita-words.tex'

OUTPUT_MOOLA_INDEX = 'index_moola.tex'
OUTPUT_WORD_INDEX = 'index_word.tex'

# Regex triggers
VERSE_COMMAND_PATTERN = re.compile(r'\\(twolineshloka|fourlineindentedshloka|onelineshloka|shloka)(\*)?')
CHAPTER_PATTERN = re.compile(r'\\chapt\{')

def clean_latex_text(text):
    """
    Removes outer braces, LaTeX macros, and punctuation.
    Returns clean Devanagari text.
    """
    if not text: return ""
    
    # Remove outer braces if present (we handle them in parsing, but safety check)
    text = text.strip()
    if text.startswith('{'): text = text[1:]
    if text.endswith('}'): text = text[:-1]

    # Remove standard LaTeX commands e.g. \textbf{...} -> ...
    text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', text) 
    
    # Remove punctuation (dandas, commas, etc.)
    text = re.sub(r'[|॥,;?!.]', '', text)
    
    return text.strip()

def get_group_char(text):
    """
    Returns the first character for grouping.
    Assumes Devanagari text.
    """
    if not text: return None
    # Just take the first unicode character
    return text[0]

def parse_file_strict(filepath, mode='moola'):
    """
    Parses the file with STRICT "Next Line" expectation.
    mode='moola': Captures only the first argument (first line after command).
    mode='split': Captures ALL arguments (all words in braces).
    """
    entries = [] 
    # For split mode, we might return list of words. For moola, list of phrases.
    
    chapter = 0
    verse = 0
    
    with open(filepath, 'r', encoding='utf-8') as f:
        # We use an iterator to allow "consuming" the next line explicitly
        lines = iter(f)
        
        for line in lines:
            line = line.strip()
            
            # 1. Chapter Check
            if CHAPTER_PATTERN.match(line):
                chapter += 1
                verse = 0
                continue
            
            # 2. Verse Trigger
            if VERSE_COMMAND_PATTERN.search(line):
                verse += 1
                link_id = f"track:split:{chapter}.{verse}"
                display_num = f"{chapter}.{verse}"
                
                # STRICT EXPECTATION: The content is on the NEXT line
                try:
                    content_line = next(lines).strip()
                except StopIteration:
                    break # End of file reached unexpectedly
                
                if not content_line.startswith('{'):
                    # This implies a formatting error in the source .tex or a comment line
                    # For now, we skip this verse to avoid crashing
                    print(f"Warning: Verse {display_num} triggered, but next line did not start with {{.")
                    continue

                # Parse based on mode
                if mode == 'moola':
                    # Capture strictly this first line/argument
                    clean_phrase = clean_latex_text(content_line)
                    if clean_phrase:
                        entries.append({
                            'text': clean_phrase,
                            'link_id': link_id,
                            'display_num': display_num
                        })
                        
                elif mode == 'split':
                    # For split, this line is words. 
                    # But does 'split' file also follow strict 1-arg per line? 
                    # If split file uses \twolineshloka, it likely has words spread over multiple lines too.
                    # Based on your prompt, we assume we process ALL lines starting with { until next command?
                    # actually, you said "The { is always on the next line". 
                    # Let's assume for Split, we capture words from that line, 
                    # AND potentially subsequent lines if they start with { (for 4-liners).
                    
                    # Capture first arg
                    entries.extend(process_words(content_line, link_id, display_num))
                    
                    # Peek ahead logic is tricky with simple iterators. 
                    # But usually, split files mirror moola files.
                    # If we need to capture lines 2,3,4 for words, we need a slightly looser loop here.
                    # Let's stick to the "Process any line starting with {" logic for SPLIT file specifically,
                    # as words can be anywhere.
                    pass 

    return entries

def parse_split_file_general(filepath):
    """
    Special parser for Split file:
    Tracks verses, but captures words from ANY line starting with {
    """
    word_entries = [] # List of (Word, LinkID, DisplayNum)
    chapter = 0
    verse = 0
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            if CHAPTER_PATTERN.match(line):
                chapter += 1
                verse = 0
                continue
                
            if VERSE_COMMAND_PATTERN.search(line):
                verse += 1
                continue
            
            # Capture words from any line starting with { (except double danda)
            if line.startswith('{') and not line.startswith('{॥'):
                clean_line = clean_latex_text(line)
                words = clean_line.split()
                
                link_id = f"track:split:{chapter}.{verse}"
                display_num = f"{chapter}.{verse}"
                
                for w in words:
                    if len(w) > 1: # Skip noise
                        word_entries.append((w, link_id, display_num))
                        
    return word_entries

def process_words(raw_line, link_id, display_num):
    # Helper to extract words from a line
    clean = clean_latex_text(raw_line)
    words = clean.split()
    res = []
    for w in words:
        if len(w) > 1:
            res.append({'text': w, 'link_id': link_id, 'display_num': display_num})
    return res

def generate_grouped_tex(entries, output_file, title, mode='list'):
    """
    Generates the LaTeX file with 'Huge Char' grouping.
    mode='list' -> Itemize (for Verses)
    mode='dict' -> Multicols Description (for Words)
    """
    # 1. Group by First Char
    groups = defaultdict(list)
    
    for e in entries:
        # e is either dict (moola) or tuple (word)
        if isinstance(e, dict):
            text = e['text']
            link = e['link_id']
            disp = e['display_num']
        else:
            text = e[0]
            link = e[1]
            disp = e[2]
            
        char = get_group_char(text)
        if char:
            groups[char].append((text, link, disp))
            
    # 2. Sort Groups (Aksharas)
    sorted_chars = sorted(groups.keys())
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Header
        f.write(f"\\section*{{{title}}}\n")
        if mode == 'dict':
            f.write(r"\begin{multicols}{2}" + "\n")
            
        for char in sorted_chars:
            # -- The Huge Character Header --
            # \nopagebreak tries to keep header with at least one item
            header = f"\n\\vspace{{1em}} {{\\Huge \\textbf{{{char}}}}} \\nopagebreak \\vspace{{0.5em}}\n"
            f.write(header)
            
            # -- The Items --
            items = groups[char]
            # Sort items alphabetically within the group
            items.sort(key=lambda x: x[0])
            
            if mode == 'list':
                f.write(r"\begin{itemize}" + "\n")
                for text, link, disp in items:
                    line = f"\\item {{{text}}} \\dotfill \\hyperref[{link}]{{{disp}}}\n"
                    f.write(line)
                f.write(r"\end{itemize}" + "\n")
                
            elif mode == 'dict':
                f.write(r"\begin{description}" + "\n")
                
                # Consolidate duplicates for Word Index
                # (Word -> [List of Links])
                unique_words = defaultdict(list)
                for text, link, disp in items:
                    # Store as tuple to avoid adding same link twice
                    if (link, disp) not in unique_words[text]:
                        unique_words[text].append((link, disp))
                
                # Sort words again (keys of unique_words)
                for word in sorted(unique_words.keys()):
                    refs = unique_words[word]
                    links_str = ", ".join([f"\\hyperref[{uid}]{{{did}}}" for uid, did in refs])
                    f.write(f"\\item[{{{word}}}] {links_str}\n")
                    
                f.write(r"\end{description}" + "\n")

        if mode == 'dict':
            f.write(r"\end{multicols}" + "\n")
            
    print(f"Generated {output_file}")

def main():
    print("Processing Moola (Verse Index)...")
    moola_entries = parse_file_strict(MOOLA_FILE, mode='moola')
    generate_grouped_tex(moola_entries, OUTPUT_MOOLA_INDEX, "Verse Index (Shloka-anukramani)", mode='list')
    
    print("Processing Split (Word Index)...")
    # For Word index, we use the general parser to catch all words in all lines
    word_entries = parse_split_file_general(SPLIT_FILE)
    generate_grouped_tex(word_entries, OUTPUT_WORD_INDEX, "Word Index (Pada-anukramani)", mode='dict')

if __name__ == "__main__":
    main()