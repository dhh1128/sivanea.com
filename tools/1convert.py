import os
import xml.etree.ElementTree as ET
import re
import html

STD_LINK_PATTERN = re.compile(r'https?://sivanea.com/(\d{4}/\d{2}/\d{2})/(.+)')
UPLOAD_LINK_PATTERN = re.compile(r'https?://sivanea.com/wp-content/uploads/(\d{4}/\d{2}(?:/\d{2})?)/(.+)')
DRAFT_LINK_PATTERN = re.compile(r'https?://sivanea.com/\?p=(\d+)')

NAMESPACES = {
    'dc': "https://purl.org/dc/elements/1.1/",
    'ns0': "https://wordpress.org/export/1.2/",
    'ns2': "https://purl.org/rss/1.0/modules/content/"
}

def get_child_text(parent, tag):
    child = parent.find(tag, NAMESPACES)
    return child.text if child is not None else None

class Comment:
    def __init__(self, comment):
        self.author = get_child_text(comment, "ns0:comment_author")
        self.date = get_child_text(comment, "ns0:comment_date")
        self.typ = get_child_text(comment, "ns0:comment_type")
        self.content = html.unescape(get_child_text(comment, "ns0:comment_content"))
        self.url = get_child_text(comment, "ns0:comment_author_url") if self.typ == 'pingback' else None

class Post:
    def __init__(self, item):
        self.item = item
        self.typ = get_child_text(item, "ns0:post_type")
        url_tag = "ns0:attachment_url" if self.typ == 'attachment' else "link"
        self.title = get_child_text(item, "title")
        url = get_child_text(item, url_tag)
        m = STD_LINK_PATTERN.match(url)
        if not m:
            m = UPLOAD_LINK_PATTERN.match(url)
        if m:
            self.date = m.group(1)
            self.slug = m.group(2)
            if self.slug.endswith('/'):
                self.slug = self.slug[:-1]
        else:
            self.date = 'unknown'
            self.slug = 'unknown'
            m = DRAFT_LINK_PATTERN.match(url)
            if m:
                print(f"Skipped draft {url}")
            else:
                print(f"Could not parse URL: {url}")
        self.url = self.date + '/' + self.slug
        self._body = get_child_text(item, "ns2:encoded")
        self._body_ready = False
        self.hashtags = []
        for cat in item.findall("category", NAMESPACES):
            self.hashtags.append(cat.text)
        self.comments = []
        for comment in item.findall("ns0:comment", NAMESPACES):
            self.comments.append(Comment(comment))

    def body(self):
        if not self._body_ready:
            self._body = html.unescape(self._body)
            self._body_ready = True
        return self._body
    
    def save(self):
        if not os.path.exists(self.date):
            os.makedirs(self.date)
        fname = os.path.join(self.date, self.slug + '.md')
        with open(fname, 'w') as f:
            f.write('---\n')
            f.write('title: ' + self.title + '\n')
            f.write('date: ' + self.date + '\n')
            f.write('slug: ' + self.slug + '\n')
            f.write('---\n\n')
            f.write(self.body())
            for c in self.comments:
                f.write('\n\n---\n\n')
                f.write(f"{c.author} ({c.date})\n\n")
                f.write(c.content)

def convert():
    # Parse the XML file into an ElementTree object
    tree = ET.parse('data.xml')
    root = tree.getroot()
    posts = []
    i = 0
    for channel in root.findall(".//channel", NAMESPACES):
        for item in channel.findall("item", NAMESPACES):
            p = Post(item)
            print(f"{i} - {p.url}")
            i += 1
            posts.append(p)
    for p in posts:
        if p.typ != 'attachment' and p.date != 'unknown':
            p.save()


if __name__ == '__main__':
    convert()