from pathlib import Path

from bs4 import BeautifulSoup

from .config import *
from .utils import get_logger


class HTMLParser:

    def __init__(self):

        self.logger = get_logger()

    # --------------------------------------------------
    # Read HTML
    # --------------------------------------------------

    def load_html(self, filepath: Path):

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()

    # --------------------------------------------------
    # Remove unwanted tags
    # --------------------------------------------------

    def remove_noise(self, soup):

        unwanted_tags = [

            "script",
            "style",
            "noscript",
            "iframe",
            "svg",
            "footer",
            "nav",
            "header"

        ]

        for tag in unwanted_tags:

            for item in soup.find_all(tag):

                item.decompose()

        return soup

    # --------------------------------------------------
    # Find Main Content
    # --------------------------------------------------

    def find_main_content(self, soup):

        candidates = [

            "article",

            "main",

            "section",

            "div"

        ]

        largest = None

        largest_length = 0

        for tag in candidates:

            for node in soup.find_all(tag):

                text = node.get_text(
                    " ",
                    strip=True
                )

                if len(text) > largest_length:

                    largest_length = len(text)

                    largest = node

        if largest:

            return largest

        return soup

    # --------------------------------------------------
    # Clean Text
    # --------------------------------------------------

    def clean_text(self, text):

        lines = []

        for line in text.splitlines():

            line = line.strip()

            if line:

                lines.append(line)

        return "\n".join(lines)

    # --------------------------------------------------
    # Parse HTML
    # --------------------------------------------------

    def parse(self, filepath):

        html = self.load_html(filepath)

        soup = BeautifulSoup(

            html,

            "lxml"

        )

        soup = self.remove_noise(soup)

        main = self.find_main_content(soup)

        return main