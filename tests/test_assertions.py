import pytest
import logging

@pytest.mark.parametrize("url, expected_text", [
    ("https://playwright.dev", "Playwright"),
    ("https://w3schools.com", "W3Schools"),
])
def test_page_title_and_content(page, url, expected_text):
    logging.info(f"Membuka halaman: {url}")
    page.goto(url, timeout=30000)

    # Assertion untuk title
    title = page.title()
    logging.info(f"Title halaman: {title}")
    assert expected_text.lower() in title.lower(), f"Expected '{expected_text}' in title, got '{title}'"

    # Assertion untuk elemen visible di halaman
    body_text = page.text_content("body")
    assert expected_text.lower() in body_text.lower(), f"Teks '{expected_text}' tidak ditemukan di halaman."

    logging.info(f"✅ {url} berisi teks '{expected_text}' seperti yang diharapkan.")
