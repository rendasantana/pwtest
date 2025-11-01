import logging
from pathlib import Path

def pytest_configure(config):
    Path("reports/screenshots").mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("reports/test_log.txt", mode="a", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
