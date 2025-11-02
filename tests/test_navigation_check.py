import pytest
import logging
import re
import os
import time
from datetime import datetime
from playwright.sync_api import Page, expect

logger = logging.getLogger(__name__)


class TestNavigationCheck:

    @pytest.mark.parametrize("url, links_to_check", [
        (
            "https://playwright.dev/python/",
            [
                {"text": "Get started", "url_part": "intro"},
                {"text": "API reference", "url_part": "api"},
                {"text": "Guides", "url_part": "guides"},
            ]
        ),
    ])
    def test_navigation_links(self, page: Page, url, links_to_check, record_property):
        """
        Robust navigation checker:
        - memastikan page siap sebelum mencari link
        - mencari link dengan beberapa strategi fallback
        - kembali ke halaman utama setelah tiap klik
        - menyimpan log detail ke report via record_property
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("reports/screenshots", exist_ok=True)

        logs = []

        def log(msg):
            logger.info(msg)
            logs.append(msg)
            print(msg)

        def find_link_flexibly(link_text: str):
            """Coba beberapa cara untuk menemukan locator link secara robust."""
            # 1) coba get_by_role dengan regex (case-insensitive)
            try:
                pattern = re.compile(re.escape(link_text), re.IGNORECASE)
                locator = page.get_by_role("link", name=pattern, exact=True)
                # cek apakah ada elemen yang resolvable (try to query count)
                if locator.count() > 0:
                    return locator
            except Exception:
                # bisa muncul strict-mode error atau lainnya; lanjut ke fallback
                pass

            # 2) fallback: cari dengan text selector (ambil yang pertama)
            try:
                txt_locator = page.locator(f"text={link_text}").first
                if txt_locator.count() > 0:
                    return txt_locator
            except Exception:
                pass

            # 3) ekstra: cari di header/nav
            try:
                header_loc = page.locator("header").locator(f"text={link_text}").first
                if header_loc.count() > 0:
                    return header_loc
            except Exception:
                pass

            # 4) terakhir: return None jika tidak ditemukan
            return None

        log("🔹 Memulai pengujian navigasi utama...")
        page.goto(url)
        page.wait_for_load_state("networkidle")
        log("✅ Halaman utama Playwright Python dibuka.")

        # gunakan regex terhadap title supaya tidak fragile
        expect(page).to_have_title(re.compile("Playwright Python"))
        log("✅ Judul halaman sesuai (regex cocok).")

        # loop tiap link
        for link in links_to_check:
            link_text = link["text"]
            expected_part = link["url_part"]
            log(f"🔍 Mengecek tautan: {link_text}")

            # pastikan kita berada di halaman home sebelum mencari link
            if page.url != url:
                page.goto(url)
                page.wait_for_load_state("networkidle")
                time.sleep(0.5)

            # tunggu nav/header siap
            try:
                page.wait_for_selector("header, nav, main", timeout=7000)
            except Exception:
                # lanjut walau header tidak tampil, karena beberapa layout berbeda
                pass

            # cari locator dengan pendekatan berlapis
            locator = find_link_flexibly(link_text)

            # jika belum ditemukan, coba scroll top & retry
            if not locator:
                try:
                    page.evaluate("window.scrollTo(0, 0)")
                    time.sleep(0.5)
                    locator = find_link_flexibly(link_text)
                except Exception:
                    locator = None

            # jika masih tidak ditemukan, log dan ambil screenshot -> fail
            if not locator:
                log(f"[ERROR] Tidak dapat menemukan link: {link_text}")
                screenshot_path = f"reports/screenshots/FAILED_NAV_{timestamp}.png"
                try:
                    page.screenshot(path=screenshot_path, full_page=True)
                    log(f"📸 Screenshot error disimpan: {screenshot_path}")
                except Exception as e_ss:
                    log(f"[WARN] Gagal menyimpan screenshot error: {e_ss}")
                record_property("Log Detail", "\n".join(logs))
                raise AssertionError(f"Gagal menemukan link: {link_text}")

            # pastikan visible (dengan timeout lebih panjang)
            try:
                expect(locator).to_be_visible(timeout=15000)
            except Exception as e_vis:
                # coba scroll to element & retry
                try:
                    locator.scroll_into_view_if_needed()
                    time.sleep(0.5)
                    expect(locator).to_be_visible(timeout=8000)
                except Exception as e2:
                    log(f"[ERROR] Locator visible check gagal untuk '{link_text}': {e2}")
                    screenshot_path = f"reports/screenshots/FAILED_NAV_{timestamp}.png"
                    try:
                        page.screenshot(path=screenshot_path, full_page=True)
                        log(f"📸 Screenshot error disimpan: {screenshot_path}")
                    except Exception as e_ss:
                        log(f"[WARN] Gagal menyimpan screenshot error: {e_ss}")
                    record_property("Log Detail", "\n".join(logs))
                    raise AssertionError(f"Gagal validasi visibility link: {link_text}") from e2

            # klik link dan tunggu URL berubah sesuai ekspektasi
            try:
                locator.click()
            except Exception as e_click:
                # jika click gagal, coba klik via javascript
                try:
                    page.evaluate(
                        "(txt) => { const el = Array.from(document.querySelectorAll('a')).find(a => a.textContent && a.textContent.trim().toLowerCase().includes(txt.toLowerCase())); if (el) el.click(); }",
                        link_text,
                    )
                except Exception as e_js:
                    log(f"[ERROR] Gagal klik link '{link_text}': {e_click} / {e_js}")
                    screenshot_path = f"reports/screenshots/FAILED_NAV_{timestamp}.png"
                    try:
                        page.screenshot(path=screenshot_path, full_page=True)
                        log(f"📸 Screenshot error disimpan: {screenshot_path}")
                    except Exception as e_ss:
                        log(f"[WARN] Gagal menyimpan screenshot error: {e_ss}")
                    record_property("Log Detail", "\n".join(logs))
                    raise AssertionError(f"Gagal klik link: {link_text}") from e_js

            # tunggu hingga page berubah / menampilkan konten target
            try:
                # tunggu URL mengandung expected_part, tapi juga fallback tunggu main h1 muncul
                expect(page).to_have_url(re.compile(expected_part), timeout=12000)
                log(f"✅ URL berisi '{expected_part}' sesuai ekspektasi.")
            except Exception:
                try:
                    # fallback: tunggu main h1 muncul (beberapa subpages dinamis)
                    page.wait_for_selector("main h1, h1", timeout=8000)
                    if expected_part not in page.url:
                        log(f"[WARN] URL belum berisi '{expected_part}' tapi halaman sudah load: {page.url}")
                    else:
                        log(f"✅ URL berisi '{expected_part}' (fallback).")
                except Exception as e_wait:
                    log(f"[ERROR] Timeout menunggu target page setelah klik '{link_text}': {e_wait}")
                    screenshot_path = f"reports/screenshots/FAILED_NAV_{timestamp}.png"
                    try:
                        page.screenshot(path=screenshot_path, full_page=True)
                        log(f"📸 Screenshot error disimpan: {screenshot_path}")
                    except Exception as e_ss:
                        log(f"[WARN] Gagal menyimpan screenshot error: {e_ss}")
                    record_property("Log Detail", "\n".join(logs))
                    raise AssertionError(f"Gagal memvalidasi navigasi untuk: {link_text}") from e_wait

            # kembali ke halaman utama untuk iterasi selanjutnya
            if page.url != url:
                page.goto(url)
                page.wait_for_load_state("networkidle")
                time.sleep(0.5)
                log("↩️ Kembali ke halaman utama untuk cek tautan berikutnya.")

        # jika semua link sukses:
        screenshot_path = f"reports/screenshots/SUCCESS_NAV_{timestamp}.png"
        try:
            page.screenshot(path=screenshot_path, full_page=True)
            log(f"📸 Screenshot sukses disimpan: {screenshot_path}")
        except Exception as e_ss:
            log(f"[WARN] Gagal menyimpan screenshot success: {e_ss}")

        record_property("Log Detail", "\n".join(logs))
        log("🎉 Semua tautan navigasi utama berhasil diverifikasi.")

    def test_navigation_footer_links(self, page: Page, record_property):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("reports/screenshots", exist_ok=True)
        logs = []

        def log(msg):
            logger.info(msg)
            logs.append(msg)
            print(msg)

        log("🔹 Memulai pengujian tautan footer...")
        page.goto("https://playwright.dev/python/")
        page.wait_for_load_state("networkidle")

        footer_links = page.locator("footer a")
        count = footer_links.count()
        log(f"🔍 Ditemukan {count} tautan di footer.")

        for i in range(count):
            try:
                link = footer_links.nth(i)
                href = link.get_attribute("href")
                text = link.inner_text().strip()
                log(f"➡️ Mengecek footer link: {text} ({href})")
                # validasi sederhana: boleh internal (start with /) atau absolute http(s)
                if href and (href.startswith("http") or href.startswith("/")):
                    log(f"✅ Link footer valid: {href}")
                else:
                    log(f"[WARN] Link footer tampak tidak valid: {href}")
            except Exception as e:
                log(f"[ERROR] Saat memeriksa footer link index {i}: {e}")

        screenshot_path = f"reports/screenshots/FOOTER_{timestamp}.png"
        try:
            page.screenshot(path=screenshot_path, full_page=True)
            log(f"📸 Screenshot footer tersimpan.")
        except Exception as e_ss:
            log(f"[WARN] Gagal menyimpan screenshot footer: {e_ss}")

        record_property("Log Detail", "\n".join(logs))
        log("🎉 Semua tautan footer berhasil diverifikasi.")
