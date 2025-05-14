import re
from tag_extractor.tag_mapper import TAG_MAP

def extract_tags_from_text(text):
    tags = set()
    text_lower=text.lower()
    for keyword, tag in TAG_MAP.items():
        if re.search(rf"\b{re.escape(keyword)}\b", text_lower):
            tags.add(tag)
    return sorted(tags)