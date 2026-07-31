from pathlib import Path
from bs4 import BeautifulSoup
from markdownify import markdownify as md

from .config import *
from .utils import get_logger


class MarkdownBuilder:

    def __init__(self):

        self.logger = get_logger()

    # ---------------------------------------------------
    # Metadata
    # ---------------------------------------------------

    def build_metadata(self,
                       crop,
                       source,
                       url):

        metadata = f"""---
title: {crop.title()}
crop: {crop.title()}
source: {source}
source_url: {url}
category: Crop Production
language: English
---

"""

        return metadata

    # ---------------------------------------------------
    # HTML -> Markdown
    # ---------------------------------------------------

    def html_to_markdown(self,
                         soup: BeautifulSoup):

        markdown = md(

            str(soup),

            heading_style="ATX",

            bullets="-",

            strip=["span"]

        )

        return markdown

    # ---------------------------------------------------
    # Cleanup Markdown
    # ---------------------------------------------------

    def clean_markdown(self,
                       markdown):

        lines = []

        previous_blank = False

        for line in markdown.splitlines():

            line = line.rstrip()

            if line == "":

                if previous_blank:
                    continue

                previous_blank = True

            else:

                previous_blank = False

            lines.append(line)

        return "\n".join(lines)

    # ---------------------------------------------------
    # Save
    # ---------------------------------------------------

    def save_markdown(self,
                      crop,
                      markdown):

        output_dir = KNOWLEDGE_BASE_DIR / "crops"

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        filepath = output_dir / f"{crop}.md"

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(markdown)

        self.logger.info(
            f"Markdown saved -> {filepath}"
        )

    # ---------------------------------------------------
    # Build
    # ---------------------------------------------------

    def build(self,
              crop,
              soup,
              source,
              url):

        metadata = self.build_metadata(

            crop,
            source,
            url

        )

        markdown = self.html_to_markdown(soup)

        markdown = self.clean_markdown(markdown)

        final = metadata + markdown

        self.save_markdown(

            crop,

            final

        )

        return final