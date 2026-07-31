from pathlib import Path

from knowledge_pipeline.parser import HTMLParser

parser = HTMLParser()

file = Path(
    "app/raw_html/tomato/crop_prot_crop diseases_veg_tomato.html"
)

content = parser.parse(file)

print(content.get_text()[:1000])