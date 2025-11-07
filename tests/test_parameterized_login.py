import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.parametrize(
    "username,password,expected_text",
    [
        ("admin", "12345", "Login successful"),
        ("user", "wrongpass", "Invalid password"),
        ("", "12345", "Username required"),
        ("admin", "", "Password required"),
    ]
)
def test_login_parameterized(username, password, expected_text):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Halaman contoh (ganti dengan URL-mu jika ada)
        page.goto("https://www.demoblaze.com/")  # contoh, nanti bisa diganti halaman login buatanmu

        # Ini hanya simulasi: misalkan kita isi input manual (anggap form login)
        print(f"\nMenguji username={username}, password={password}")
        
        # Karena tidak ada form nyata, kita hanya akan "simulasi hasil"
        if username == "admin" and password == "12345":
            result = "Login successful"
        elif username == "":
            result = "Username required"
        elif password == "":
            result = "Password required"
        else:
            result = "Invalid password"

        assert result == expected_text, f"Dapat: {result}, tapi harapannya: {expected_text}"
        browser.close()
