from tqdm import tqdm
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

    def discover_links(self, crop: str, index_url: str):

        html = self.fetch_html(index_url)

        soup = BeautifulSoup(html, "lxml")

        base = "{0.scheme}://{0.netloc}".format(
            urlparse(index_url)
        )

        discovered = set()

        crop = crop.lower()

        blacklist = {

            "home",
            "contact",
            "photo bank",
            "feedback",
            "copyright",
            "nursery techniques",
            "deficiencies & disorders"

        }

        for tag in soup.find_all("a", href=True):

            text = tag.get_text(
                " ",
                strip=True
            ).lower()

            href = tag["href"].strip()

            if text in blacklist:
                continue

            if href.startswith("#"):
                continue

            if href.startswith("mailto"):
                continue

            full = urljoin(base, href)

            if "agritech.tnau.ac.in" not in full:
                continue

            if crop not in full.lower() and crop not in text:
                continue

            discovered.add(full)

        self.logger.info(
            f"Discovered {len(discovered)} crop pages."
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

        if filepath.exists():

            self.logger.info(
                f"Skipped existing : {filepath.name}"
            )

            return

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

        links = self.discover_links(
                crop,
                index_url
            )

        self.logger.info(
            f"Downloading {len(links)} pages..."
        )

        for url in tqdm(
                links,
                desc=f"Crawling {crop}"
            ):

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

                self.logger.exception(e)

        self.logger.info(
            "Crawling Complete."
        )

