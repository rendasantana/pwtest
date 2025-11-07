def test_video_fail(record_video):
    record_video.goto("https://playwright.dev/python/")
    title = record_video.title()
    print(f"Judul halaman: {title}")

    # Test gagal sengaja dibuat
    assert "Selenium" in title, "Judul tidak mengandung kata 'Selenium'"
