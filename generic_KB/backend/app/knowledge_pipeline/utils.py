import logging
from pathlib import Path

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import requests

from .config import *


# =======================================================
# Folder Creation
# =======================================================

def create_directories():

    directories = [

        RAW_HTML_DIR,
        KNOWLEDGE_BASE_DIR,
        LOG_DIR

    ]

    for directory in directories:

        Path(directory).mkdir(
            parents=True,
            exist_ok=True
        )


# =======================================================
# Logging
# =======================================================

def get_logger():

    logger = logging.getLogger("KnowledgePipeline")

    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(

        "%(asctime)s | %(levelname)s | %(message)s"

    )

    file_handler = logging.FileHandler(

        LOG_DIR / "pipeline.log",
        encoding="utf-8"

    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.addHandler(console_handler)

    return logger


# =======================================================
# HTTP Session
# =======================================================

def create_session():

    session = requests.Session()

    retries = Retry(

        total=MAX_RETRIES,

        backoff_factor=1,

        status_forcelist=[500, 502, 503, 504]

    )

    adapter = HTTPAdapter(max_retries=retries)

    session.mount("https://", adapter)

    session.mount("http://", adapter)

    session.headers.update(HEADERS)

    return session