import os
import re

relpat = re.compile(r'^date:\s*(20\d\d-\d\d-\d\d)\nslug:\s*(.*)$', re.M)

for file in os.listdir("."):
    if file.endswith(".md") and file != 'README.md':
        with open(file, 'r') as f:
            content = f.read()
        m = relpat.search(content)
        if m:
            date = m.group(1).replace('-', '/')
            slug = m.group(2)
            content = content[:m.end()] + f"\nredirect_from:\n  - /{date}/{slug}" + content[m.end():]
            with open(file, 'w') as f:
                f.write(content)
