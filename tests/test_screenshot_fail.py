def test_example_fail(page):
    page.goto("https://playwright.dev/python/")
    page.screenshot(path="tests/screenshots/before_fail.png")
    title = page.title()

    print(f"Title halaman: {title}")
    # Test ini sengaja dibuat gagal agar fitur screenshot otomatis aktif
    assert "Selenium" in title, "Judul tidak mengandung kata 'Selenium'"
