# Search English Word By Pinyin

## Motivation

When looking up English words, one might encounter situations where only the pronunciation is known.

This tool provides the function of searching for words through Chinese Pinyin, which can search for English words when only the pronunciation is known.

## Usage

```
python pinyin2word.py
```

## Implementation

The [CMUdict](https://github.com/cmusphinx/cmudict) used by this tool contains over 134,000 words and their pronunciations in the ARPAbet phoneme set.

I summarized the Pinyin elements that are pronounced similarly to the phoneme in ARPAbet. Based on this, the tool could calculate the Levenshtein distance between the Pinyin input and the pronunciations in the dictionary to judge their similarity.