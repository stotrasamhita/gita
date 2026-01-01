#!/bin/bash
grep '^{' words/gita-words.tex | grep -v '॥' | sed 's/[{]//;s/\}.*//' | tr ' ' '\n' | sed 's/ं$/म्/' | sort | uniq > words/gita-wordlist.txt