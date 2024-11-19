import os
import re

url_pat = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

with open('README.md', 'r') as f:
    lines = f.readlines()


def capitalize(word):
    if word in ['of', 'from', 'in', 'and', 'at', 'on', 'to', 'with', 'the', 'a', 'an', 'by']: return word
    return word.capitalize()

lines = [line.strip().replace('[](','').replace(')','') for line in lines if line.strip()]
for line in lines:
    url = line
    title = url[url.rfind('/') + 1:]
    title = title[:title.rfind('.')]
    words = title.split('-')
    words = [words[0].capitalize()] + [capitalize(word) for word in words[1:]]
    title = ' '.join(words)
    print(f"[{title}]({url})")