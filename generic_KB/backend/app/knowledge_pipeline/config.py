from pathlib import Path

# =====================================================
# Base Directories
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_HTML_DIR = BASE_DIR / "app" / "raw_html"

KNOWLEDGE_BASE_DIR = BASE_DIR / "app" / "knowledge_base"

LOG_DIR = BASE_DIR / "logs"

# =====================================================
# Crawl Settings
# =====================================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}

TIMEOUT = 20

MAX_RETRIES = 3

REQUEST_DELAY = 1

# =====================================================
# Supported Crops
# =====================================================

CROP_URLS = {

    "tomato":
    "https://agritech.tnau.ac.in/horticulture/horti_vegetables_tomato_index.html",

    "potato":
    "https://agritech.tnau.ac.in/horticulture/horti_vegetables_potato.html",

    "cotton":
    "https://agritech.tnau.ac.in/agriculture/agri_index.html",

    "rice":
    "https://agritech.tnau.ac.in/agriculture/agri_index.html"

}