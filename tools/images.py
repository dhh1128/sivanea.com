import os
import re

html_imgurl_pat = re.compile(r'<img[^>]+?src="([^"]+)"')
md_imgurl_pat = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')

images = []
for file in os.listdir('assets'):
    if file.endswith('.jpeg') or file.endswith('.jpg') or file.endswith('.png'):
        images.append(file)

matches = {}

def check_match(images, match, fname):
    global matches
    url = match.group(1)
    valid = ('assets/' in url or url.startswith('https://')) and (url.endswith('.jpeg') or url.endswith('.jpg') or url.endswith('.png'))
    if valid:
        if not url.startswith('https://'):
            fragment = url[url.rfind('/') + 1:]
            if fragment not in images:
                valid = False
            else:
                matches[fragment] = 1
    if not valid:
        print(f"Invalid image URL {url} in {fname}")


for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".md") and file != 'README.md':
            fpath = os.path.join(root, file)
            with open(fpath, 'r') as f:
                content = f.read()
            #print(f"Checking {file}")
            for match in md_imgurl_pat.finditer(content):
                check_match(images, match, file)
            for match in html_imgurl_pat.finditer(content):
                check_match(images, match, file)

valid_count = len([x for x in images if x in matches])
print(f"{valid_count} images referenced validly.")

for unreferenced in [x for x in images if x not in matches]:
    print(f"Image {unreferenced} not referenced in any markdown file")

