#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from collections import defaultdict

# --- Configuration ---
MOOLA_FILE = '../gita.tex'
SPLIT_FILE = 'gita-words.tex'

OUTPUT_MOOLA_INDEX = 'index_moola.tex'
OUTPUT_WORD_INDEX = 'index_word.tex'

# Regex triggers
VERSE_COMMAND_PATTERN = re.compile(r'^\\(twolineshloka|fourlineindentedshloka|onelineshloka|shloka)(\*)?')
CHAPTER_PATTERN = re.compile(r'\\chapt\{')

def normalize_anusvara(word):
    """
    Standardizes Sanskrit words for indexing.
    Specifically: Ends with Anusvara (ं) -> Halanta Ma (म्)
    """
    if word.endswith('ं'): # Unicode \u0902
        return word[:-1] + 'म्' # Replaces with \u092e + \u094d
    return word

def clean_latex_text(text):
    """
    1. Removes TeX comments (%).
    2. Trims content outside the last closing brace '}'.
    3. Removes braces and TeX macros.
    4. Removes punctuation.
    """
    if not text: return ""
    
    # 1. Strip TeX comments immediately
    text = text.split('%')[0].strip()
    
    # 2. Safety: Only keep content up to the last '}'
    # This prevents capturing "garbage" or counters that exist after the brace
    last_brace_index = text.rfind('}')
    if last_brace_index != -1:
        text = text[:last_brace_index+1]

    # 3. Remove outer braces
    text = text.strip()
    if text.startswith('{'): text = text[1:]
    if text.endswith('}'): text = text[:-1]

    # 4. Remove standard LaTeX commands e.g. \textbf{...} -> ...
    text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', text) 
    
    # 5. Remove punctuation (dandas, commas, etc.)
    text = re.sub(r'[|॥,;?!.]', '', text)
    
    return text.strip()

def get_group_char(text):
    """Returns the first character for grouping."""
    if not text: return None
    return text[0]

def parse_file_strict(filepath, mode='moola'):
    """
    Parses gita.tex for Moola.
    Strictly captures only the content of the FIRST argument (next line).
    """
    entries = [] 
    chapter = 0
    verse = 0
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = iter(f)
        for line in lines:
            line = line.strip()
            
            if CHAPTER_PATTERN.match(line):
                chapter += 1
                verse = 0
                continue
            
            if VERSE_COMMAND_PATTERN.search(line):
                if not ('onelineshloka' in line and '*' not in line):
                    verse += 1
                link_id = f"track:moola:{chapter}.{verse}"
                display_num = f"{chapter}-{verse}"
                
                # STRICT EXPECTATION: The content is on the NEXT line
                try:
                    content_line = next(lines).strip()
                except StopIteration:
                    break 
                
                if not content_line.startswith('{'):
                    print(f"Warning: Verse {display_num} skipped. Expected '{{' on next line, got: {content_line[:20]}...")
                    verse -= 1
                    continue

                if mode == 'moola':
                    clean_phrase = clean_latex_text(content_line)
                    if clean_phrase:
                        entries.append({
                            'text': clean_phrase,
                            'link_id': link_id,
                            'display_num': display_num
                        })
    return entries

def parse_split_file_general(filepath):
    """
    Parses gita-words.tex for Words.
    Captures words from ANY line starting with {.
    """
    word_entries = [] 
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
                if not ('onelineshloka' in line and '*' not in line):
                    verse += 1
                continue
            
            # Capture words from any line starting with { (except double danda)
            if line.startswith('{') and not line.startswith('{॥'):
                clean_line = clean_latex_text(line)
                words = clean_line.split()
                
                link_id = f"track:moola:{chapter}.{verse}"
                display_num = f"{chapter}-{verse}"
                
                for w in words:
                    # NORMALIZE: Handle Anusvara -> 'm'
                    w = normalize_anusvara(w)
                    
                    word_entries.append((w, link_id, display_num))
                        
    return word_entries

def generate_grouped_tex(entries, output_file, mode='list'):
    """
    Generates LaTeX output grouped by First Character.
    """
    # 1. Group by First Char
    groups = defaultdict(list)
    
    for e in entries:
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
        if mode == 'dict':
            f.write(r"\begin{multicols}{2}" + "\n")
        for char in sorted_chars:
            # 1. Add Anchor (for proper linking)
            # 2. Add to TOC (as a chapter)
            # 3. Print Visual Header
            header = (
                f"\n\\phantomsection"
                f"\\addcontentsline{{toc}}{{chapter}}{{{char}}}" 
                f"\n\\vspace{{1em}} \\centerline{{\\Huge \\textbf{{{char}}}}} \\nopagebreak \\vspace{{0.5em}}\n"
            )
            f.write(header)            
            
            items = groups[char]
            items.sort(key=lambda x: x[0])
            
            if mode == 'list':
                f.write(r"\begin{itemize}" + "\n")
                # f.write(r"\addtolength{\itemsep}{-1ex}" + "\n")
                for text, link, disp in items:
                    line = f"\\item {text} \\dotfill \\hyperref[{link}]{{{disp}}}\n"
                    f.write(line)
                f.write(r"\end{itemize}" + "\n")
                
            elif mode == 'dict':
                f.write(r"\begin{description}" + "\n")
                
                # Consolidate duplicates
                unique_words = defaultdict(list)
                for text, link, disp in items:
                    if (link, disp) not in unique_words[text]:
                        unique_words[text].append((link, disp))
                
                # Sort words within the group
                for word in sorted(unique_words.keys()):
                    refs = unique_words[word]
                    links_str = ", ".join([f"\\hyperref[{uid}]{{{did}}}" for uid, did in refs])
                    f.write(f"\\item[{word}] {links_str}\n")
                    
                f.write(r"\end{description}" + "\n")

        if mode == 'dict':
            f.write(r"\end{multicols}" + "\n")
            
    print(f"Generated {output_file}")

def main():
    print("Processing Moola (Verse Index)...")
    moola_entries = parse_file_strict(MOOLA_FILE, mode='moola')
    generate_grouped_tex(moola_entries, OUTPUT_MOOLA_INDEX, mode='list')
    
    print("Processing Split (Word Index)...")
    word_entries = parse_split_file_general(SPLIT_FILE)
    generate_grouped_tex(word_entries, OUTPUT_WORD_INDEX, mode='dict')

if __name__ == "__main__":
    main()