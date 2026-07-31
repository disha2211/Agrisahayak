from pathlib import Path

from knowledge_pipeline.parser import HTMLParser
from knowledge_pipeline.cleaner import HTMLCleaner
from knowledge_pipeline.markdown_builder import MarkdownBuilder

parser = HTMLParser()

cleaner = HTMLCleaner()

builder = MarkdownBuilder()

file = Path(
    "app/raw_html/tomato/horti_min_nutri_veg_tomato.html"
)

soup = parser.parse(file)

soup = cleaner.clean(soup)

builder.build(

    crop="tomato",

    soup=soup,

    source="TNAU",

    url="https://agritech.tnau.ac.in/horticulture/horti_vegetables_tomato_index.html"

)