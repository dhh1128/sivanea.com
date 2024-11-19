import os
import re

relpat = re.compile(r'---\n\n(.*\|\s[A-Za-z0-9].*$)\n\n\[(…|\.\.\.)\].*\[(…|\.\.\.)\]', re.M)

for file in os.listdir("."):
    if file.endswith("") and file != 'README':
        with open(file, 'r') as f:
            content = f.read()
        match = relpat.search(content)
        updated = False
        while match:
            updated = True
            content = content.replace(match.group(), '')
            match = relpat.search(content)
        if updated:
            with open(file, 'w') as f:
                f.write(content)
