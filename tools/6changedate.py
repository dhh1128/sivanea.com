import os
import re

relpat = re.compile(r'date:\s*(20\d\d)/(\d\d)/(\d\d)')

for file in os.listdir("."):
    if file.endswith(".md") and file != 'README.md':
        with open(file, 'r') as f:
            content = f.read()
        match = relpat.search(content)
        if match:
            content = content.replace(match.group(), f'date: {match.group(1)}-{match.group(2)}-{match.group(3)}')
            with open(file, 'w') as f:
                f.write(content)
