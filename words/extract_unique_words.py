#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import sys

def extract_unique_words_from_csv(input_filename, output_filename):
    # Read the CSV, skipping the first 2 rows. 
    # header=None ensures we treat the 3rd line as data, not a header.
    try:
        df = pd.read_csv(input_filename, skiprows=2, header=None)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Select columns from the 4th onwards (index 3)
    # iloc uses 0-based indexing, so 3 is the 4th column.
    data_subset = df.iloc[:, 3:]

    # Flatten the dataframe to a 1D array of values
    all_values = data_subset.values.flatten()

    unique_words = set()
    
    for word in all_values:
        # Skip NaN/empty values
        if pd.isna(word):
            continue
        
        # Convert to string and strip whitespace
        word = str(word).strip()
        
        # Skip empty strings and specific punctuation
        if not word or word in ['।', '॥']:
            continue
        
        # Replace 'ं' at the end of the word with 'म्'
        if word.endswith('ं'):
            word = word[:-1] + 'म्'
            
        unique_words.add(word)

    # Sort the unique words
    sorted_words = sorted(list(unique_words))

    # Write to output file
    with open(output_filename, 'w', encoding='utf-8') as f:
        for w in sorted_words:
            f.write(w + '\n')
            
    print(f"Successfully processed {len(sorted_words)} unique words.")
    print(f"Output saved to {output_filename}")

if __name__ == "__main__":
    # Usage example
    if len(sys.argv) != 3:
        print("Usage: python extract_unique_words.py <input_csv_file> <output_txt_file>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        extract_unique_words_from_csv(input_file, output_file)