from playwright.sync_api import Page, expect

def test_add_product_to_cart(page: Page):
    # 1️⃣ Buka situs
    page.goto("https://www.demoblaze.com")

    # 2️⃣ Klik produk Samsung galaxy s6
    page.click("text=Samsung galaxy s6")

    # 3️⃣ Pastikan detail produk muncul
    expect(page.locator("h2.name")).to_have_text("Samsung galaxy s6")

    # 4️⃣ Tangani alert popup
    def handle_dialog(dialog):
        print(f"Alert muncul: {dialog.message}")
        assert "Product added" in dialog.message, "Pesan alert tidak sesuai!"
        dialog.accept()

    page.on("dialog", handle_dialog)

    # 5️⃣ Klik Add to cart
    page.click("text=Add to cart")

    # 6️⃣ Tunggu sebentar agar popup sempat muncul
    page.wait_for_timeout(2000)
