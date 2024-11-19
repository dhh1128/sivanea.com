import os
import re

comment_pat = re.compile(r'^(.*?)\s*\((20[0-9-: ]+)\)(.*)', re.DOTALL | re.MULTILINE)

class Comment:
    def __init__(self, m):
        self.author = m.group(1)
        self.date = m.group(2)
        self.rest = m.group(3).strip()


for file in os.listdir("."):
    if file.endswith(".md") and file != 'README.md':
        if os.path.isdir('./' + file): continue
        with open(file, 'r') as f:
            content = '\n' + f.read()
        sections = content.split('\n---\n')
        if not sections[0]: sections.pop(0)
        print(file)
        frontmatter = sections[0].strip()
        content = sections[1].strip()
        comments = [x.strip() for x in sections[2:]]
        if comments:
            clist = []
            for comment in comments:
                clist.append(Comment(comment_pat.match(comment)))
            clist.sort(key=lambda x: x.date)
            ctxt = 'comments:\n'
            for c in clist:
                if c.rest:
                    ctxt += '  - author: ' + c.author + '\n' + '    date: ' + c.date + '\n' + '    comment: |'
                    for line in c.rest.split('\n'):
                        ctxt += '\n      ' + line
                    ctxt += '\n'
            frontmatter += '\n' + ctxt
            with open(file, 'w') as f:
                f.write('---\n' + frontmatter + '---\n' + content + '\n')
