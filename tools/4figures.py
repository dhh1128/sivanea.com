import os
import re

cap_pat = re.compile(r'\[caption id="".*?(<a href=".*?">)?(<img .*?/>)(?:</a>)?\s*(.*?)\[/caption\]', re.DOTALL | re.MULTILINE)

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.md'):
            file_path = os.path.join(root, file)
            print(file_path)
            with open(file_path, 'r') as f:
                content = f.read()
            updated = False
            match = cap_pat.search(content)
            while match:
                updated = True
                anchor_tag = match.group(1)
                img_tag = match.group(2)
                caption = match.group(3)
                new_tag = f'<figure>{img_tag}<figcaption>{caption}</figcaption></figure>'
                content = content[:match.start()] + new_tag + content[match.end():]
                match = cap_pat.search(content)
            if updated:
                with open(file_path, 'w') as f:
                    f.write(content)
                print(f'Updated {file_path}')
