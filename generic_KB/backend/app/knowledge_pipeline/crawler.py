from pathlib import Path
from urllib.parse import urljoin, urlparse
import time

from bs4 import BeautifulSoup

from .config import *
from .utils import create_session, get_logger


class TNAUCrawler:

    def __init__(self):

        self.session = create_session()
        self.logger = get_logger()

    # ---------------------------------------------------
    # Download HTML
    # ---------------------------------------------------

    def fetch_html(self, url: str):

        self.logger.info(f"Downloading : {url}")

        response = self.session.get(
            url,
            timeout=TIMEOUT
        )

        response.raise_for_status()

        return response.text

    # ---------------------------------------------------
    # Discover Links
    # ---------------------------------------------------

    def discover_links(self, index_url: str):

        html = self.fetch_html(index_url)

        soup = BeautifulSoup(html, "lxml")

        discovered = set()

        base = "{0.scheme}://{0.netloc}".format(
            urlparse(index_url)
        )

        for tag in soup.find_all("a", href=True):

            href = tag["href"].strip()

            if href.startswith("#"):
                continue

            if href.startswith("mailto:"):
                continue

            full_url = urljoin(base, href)

            if "agritech.tnau.ac.in" not in full_url:
                continue

            discovered.add(full_url)

        self.logger.info(
            f"Found {len(discovered)} links."
        )

        return sorted(discovered)

    # ---------------------------------------------------
    # Save HTML
    # ---------------------------------------------------

    def save_html(
        self,
        crop: str,
        url: str,
        html: str
    ):

        crop_dir = RAW_HTML_DIR / crop

        crop_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        filename = (
            url.split("/")[-1]
            .replace(".html", "")
            .replace(".htm", "")
        )

        if filename == "":
            filename = "index"

        filepath = crop_dir / f"{filename}.html"

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(html)

        self.logger.info(
            f"Saved -> {filepath}"
        )

    # ---------------------------------------------------
    # Crawl Entire Crop
    # ---------------------------------------------------

    def crawl_crop(self, crop: str):

        if crop not in CROP_URLS:

            raise ValueError(
                f"{crop} not configured."
            )

        index_url = CROP_URLS[crop]

        links = self.discover_links(index_url)

        self.logger.info(
            f"Downloading {len(links)} pages..."
        )

        for url in links:

            try:

                html = self.fetch_html(url)

                self.save_html(
                    crop,
                    url,
                    html
                )

                time.sleep(REQUEST_DELAY)

            except Exception as e:

                self.logger.warning(
                    f"Skipped {url}"
                )

                self.logger.warning(e)

        self.logger.info(
            "Crawling Complete."
        )