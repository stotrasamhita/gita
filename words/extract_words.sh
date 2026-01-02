#!/bin/bash
grep '^{' gita-words.tex | grep -v '॥' | sed 's/[{]//;s/\}.*//' | tr ' ' '\n' | sed 's/ं$/म्/' | sort | uniq > gita-wordlist.txt
