from pathlib import Path

from markdownify import markdownify as md

from .config import *
from .utils import get_logger


class MarkdownBuilder:

    def __init__(self):

        self.logger = get_logger()

        self.sections = []

    # ----------------------------------------------------

    def metadata(self,
                 crop,
                 source):

        return f"""---
title: {crop.title()}
crop: {crop.title()}
source: {source}
category: Crop Production
language: English
---

"""

    # ----------------------------------------------------

    def soup_to_markdown(self, soup):

        markdown = md(

            str(soup),

            heading_style="ATX",

            bullets="-",

            strip=["span"]

        )

        return markdown

    # ----------------------------------------------------

    def clean(self,
              markdown):

        lines = []

        blank = False

        for line in markdown.splitlines():

            line = line.rstrip()

            if line == "":

                if blank:
                    continue

                blank = True

            else:

                blank = False

            lines.append(line)

        return "\n".join(lines)

    # ----------------------------------------------------

    def add_section(self,
                    soup):

        markdown = self.soup_to_markdown(soup)

        markdown = self.clean(markdown)

        if markdown.strip():

            self.sections.append(markdown)

    # ----------------------------------------------------

    def merge(self):

        return "\n\n---\n\n".join(self.sections)

    # ----------------------------------------------------
    def save(self, crop, content):

        folder = KNOWLEDGE_BASE_DIR / "crops"

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        filepath = folder / f"{crop}.md"

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(content)

        self.logger.info(
            f"Saved {filepath}"
        )

        return filepath