import re
from bs4 import BeautifulSoup, NavigableString, Comment

from .utils import get_logger


class HTMLCleaner:

    def __init__(self):

        self.logger = get_logger()

        self.blacklisted_words = {

            "home",
            "contact",
            "photo bank",
            "copyright",
            "all rights reserved",
            "tnau 2008",
            "tnau 2009",
            "tnau 2010",
            "tnau 2011",
            "tnau 2012",
            "tnau 2013",
            "tnau 2014",
            "tnau 2015",
            "tnau 2016",
            "tnau 2017",
            "tnau 2018",
            "tnau 2019",
            "tnau 2020",
            "tnau 2021",
            "tnau 2022",
            "tnau 2023",
            "tnau 2024",
            "tnau 2025",
            "site map",
            "feedback"

        }

    # --------------------------------------------------

    def remove_comments(self, soup):

        comments = soup.find_all(
            string=lambda text: isinstance(text, Comment)
        )

        for comment in comments:
            comment.extract()

        return soup

    # --------------------------------------------------

    def remove_empty_tags(self, soup):

        for tag in soup.find_all():

            if tag.name in ["img", "br", "hr"]:
                continue

            if not tag.get_text(strip=True):

                tag.decompose()

        return soup

    # --------------------------------------------------

    def remove_navigation_blocks(self, soup):

        selectors = [

            "nav",
            "header",
            "footer",
            ".navbar",
            ".navigation",
            ".menu",
            ".footer",
            ".breadcrumb",
            ".breadcrumbs"

        ]

        for selector in selectors:

            try:

                for node in soup.select(selector):

                    node.decompose()

            except Exception:
                pass

        return soup

    # --------------------------------------------------

    def remove_duplicate_links(self, soup):

        seen = set()

        for link in soup.find_all("a"):

            text = link.get_text(" ", strip=True)

            if text in seen:

                link.decompose()

            else:

                seen.add(text)

        return soup

    # --------------------------------------------------

    def remove_blacklisted_text(self, soup):

        for node in soup.find_all(text=True):

            if isinstance(node, NavigableString):

                text = node.strip().lower()

                if text in self.blacklisted_words:

                    node.extract()

        return soup

    # --------------------------------------------------

    def normalize_whitespace(self, soup):

        text = str(soup)

        text = re.sub(r"\n+", "\n", text)

        text = re.sub(r"\t+", "", text)

        text = re.sub(r" +", " ", text)

        return BeautifulSoup(text, "lxml")

    # --------------------------------------------------

    def clean(self, soup):

        soup = self.remove_comments(soup)

        soup = self.remove_navigation_blocks(soup)

        soup = self.remove_duplicate_links(soup)

        soup = self.remove_blacklisted_text(soup)

        soup = self.remove_empty_tags(soup)

        soup = self.normalize_whitespace(soup)

        return soup