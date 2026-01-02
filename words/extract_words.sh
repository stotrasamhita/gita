#!/bin/bash
grep '^{' gita-words.tex | grep -v '॥' | sed 's/[{]//;s/\}.*//' | tr ' ' '\n' | sed 's/ं$/म्/' | sort | uniq > gita-wordlist.txt
grep item index_word.tex | awk '{print $1}' | sed 's@\\item\[@@g;s@]$@@g' > words.txt
