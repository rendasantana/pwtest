from playwright.sync_api import sync_playwright, expect

def test_wait_and_sync_example():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1️⃣ Buka halaman demo dengan delay
        page.goto("https://demo.playwright.dev/todomvc/")

        # 2️⃣ Tunggu elemen utama muncul (list input)
        page.wait_for_selector(".new-todo")

        # 3️⃣ Isi form setelah input siap
        page.fill(".new-todo", "Belajar Playwright Wait")
        page.press(".new-todo", "Enter")

        # 4️⃣ Tunggu item muncul di daftar
        page.wait_for_selector(".todo-list li")

        # 5️⃣ Verifikasi teksnya
        text = page.text_content(".todo-list li")
        assert "Belajar Playwright Wait" in text

        browser.close()
