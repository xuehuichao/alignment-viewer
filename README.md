alignment-viewer
================

This script visualizes alignments between two sentences.

Machine translation, paraphrasing systems often need to use alignments. Examining the word level alignment between two sentences is helpful for tuning such systems. This script visualizes the alignment structure between two sentences.

Input
1. two sentences (e.g. one in French, and one in English)
2. the alignment between them (e.g. the first French word is aligned with the first English word)
Output
1. A PNG image visualizing the two sentences, and the alignments between them
![The alignment structure between English sentence "I like machine translation ." and Chinese sentence "我 喜欢 机器翻译 。"](demo.png)


Dependencies
------------
This script is written in Python. It depends on the following packages:

1. Google flags library -- [gflags](https://code.google.com/p/python-gflags/)
2. Python Image Library -- [PIL](http://www.pythonware.com/products/pil/)
