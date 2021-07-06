# 用拼音搜索英文单词

## 功能

在查英语单词时有时会遇到只知道单词发音，不知道单词拼写的情况。本工具提供了用拼音搜索单词的功能，可以在只知道单词发音的情况下查找单词。

## 运行

```
python pinyin2word.py
```

## 原理

本工具使用的[CMUdict](https://github.com/cmusphinx/cmudict)包含超过134,000个单词和它们的发音，发音用[ARPAbet](https://en.wikipedia.org/wiki/ARPABET)表示。

我总结了和ARPAbet中的音素发音相近的拼音元素，并以此为依据，计算用户输入的拼音和词典中单词ARPAbet的[Levenshtein距离](https://en.wikipedia.org/wiki/Levenshtein_distance)，从而判断用户输入拼音和词典中单词发音的相似程度。