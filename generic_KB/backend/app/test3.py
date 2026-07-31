from pathlib import Path

from knowledge_pipeline.parser import HTMLParser
from knowledge_pipeline.cleaner import HTMLCleaner

parser = HTMLParser()
cleaner = HTMLCleaner()

file = Path(
    "app/raw_html/tomato/horti_min_nutri_veg_tomato.html"
)

soup = parser.parse(file)

clean = cleaner.clean(soup)

print(clean.get_text("\n"))