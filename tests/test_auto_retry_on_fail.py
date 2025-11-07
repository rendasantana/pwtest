import pytest
from playwright.sync_api import sync_playwright

# Latihan 42: Auto Retry Test on Failure
@pytest.mark.retry
@pytest.mark.flaky(reruns=2, reruns_delay=2)
def test_auto_retry_on_fail():
    """Test ini akan otomatis diulang 2x jika gagal"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")

        # Simulasi hasil gagal kadang-kadang
        import random
        value = random.choice([True, False])
        print(f"Simulasi hasil test: {'PASS' if value else 'FAIL'}")

        assert value, "Test gagal secara acak (ini untuk menguji retry)"

        browser.close()
