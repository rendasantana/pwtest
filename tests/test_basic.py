def test_open_w3schools(page):
    page.goto("https://w3schools.com")
    assert "W3Schools" in page.title()
