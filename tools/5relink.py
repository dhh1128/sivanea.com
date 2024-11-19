import os
import re

relpat = re.compile(r'href="[^>]*?/20\d\d/\d\d/\d\d/([-a-z0-9]+)/"')

for file in os.listdir("."):
    if file.endswith(".md") and file != 'README.md':
        with open(file, 'r') as f:
            content = f.read()
        match = relpat.search(content)
        updated = False
        while match:
            updated = True
            content = content.replace(match.group(), f'href="{match.group(1)}"')
            match = relpat.search(content)
        if updated:
            with open(file, 'w') as f:
                f.write(content)
