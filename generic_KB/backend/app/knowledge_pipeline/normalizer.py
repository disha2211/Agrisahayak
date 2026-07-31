import re
from collections import OrderedDict

from .utils import get_logger


class MarkdownNormalizer:

    def __init__(self):

        self.logger = get_logger()

    # ----------------------------------------------------
    # Remove duplicate blank lines
    # ----------------------------------------------------

    def normalize_blank_lines(self, text):

        text = re.sub(r"\n{3,}", "\n\n", text)

        return text

    # ----------------------------------------------------
    # Remove duplicate paragraphs
    # ----------------------------------------------------

    def remove_duplicate_paragraphs(self, text):

        seen = OrderedDict()

        paragraphs = text.split("\n\n")

        for para in paragraphs:

            clean = para.strip()

            if clean:

                seen[clean] = True

        return "\n\n".join(seen.keys())

    # ----------------------------------------------------
    # Remove duplicate headings
    # ----------------------------------------------------

    def remove_duplicate_headings(self, text):

        lines = []

        headings = set()

        for line in text.splitlines():

            if line.startswith("#"):

                heading = line.strip()

                if heading in headings:

                    continue

                headings.add(heading)

            lines.append(line)

        return "\n".join(lines)

    # ----------------------------------------------------
    # Remove repeated separators
    # ----------------------------------------------------

    def clean_separators(self, text):

        text = re.sub(r"(-{3,}\n){2,}", "---\n", text)

        return text

    # ----------------------------------------------------
    # Normalize heading hierarchy
    # ----------------------------------------------------

    def normalize_headings(self, text):

        lines = []

        first_heading = True

        for line in text.splitlines():

            if line.startswith("#"):

                heading = line.lstrip("#").strip()

                if first_heading:

                    lines.append(f"# {heading}")

                    first_heading = False

                else:

                    lines.append(f"## {heading}")

            else:

                lines.append(line)

        return "\n".join(lines)

    # ----------------------------------------------------

    def remove_short_lines(self, text):

        lines = []

        blacklist = {

            "home",
            "contact",
            "feedback",
            "next",
            "previous",
            "top"

        }

        for line in text.splitlines():

            clean = line.strip().lower()

            if clean in blacklist:

                continue

            lines.append(line)

        return "\n".join(lines)

    # ----------------------------------------------------

    def normalize(self, markdown):

        markdown = self.normalize_blank_lines(markdown)

        markdown = self.remove_duplicate_paragraphs(markdown)

        markdown = self.remove_duplicate_headings(markdown)

        markdown = self.clean_separators(markdown)

        markdown = self.normalize_headings(markdown)

        markdown = self.remove_short_lines(markdown)

        self.logger.info("Markdown normalized.")

        return markdown