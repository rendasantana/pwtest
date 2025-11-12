import pytest
from datetime import datetime
from pathlib import Path
from playwright.sync_api import expect

@pytest.mark.smoke
def test_form_multi_browser(page, browser_name):
    """Latihan Bonus 16: Jalankan di banyak browser"""

    html = """
    <html>
    <body>
        <h2>Form Multi Browser</h2>
        <form>
            <input id="name" placeholder="Nama"><br><br>
            <input id="email" placeholder="Email"><br><br>
            <button id="submit">Kirim</button>
        </form>
        <p id="result"></p>

        <script>
            document.querySelector("#submit").addEventListener("click", e => {
                e.preventDefault();
                const name = document.querySelector("#name").value;
                const email = document.querySelector("#email").value;
                const result = document.querySelector("#result");
                if(name && email.includes("@")){
                    result.textContent = "✅ Form sukses dikirim!";
                } else {
                    result.textContent = "❌ Form gagal!";
                }
            });
        </script>
    </body>
    </html>
    """

    page.set_content(html)

    # Isi form
    page.fill("#name", "Renda Arya Santana")
    page.fill("#email", "renda@example.com")
    page.click("#submit")

    # Validasi
    expect(page.locator("#result")).to_have_text("✅ Form sukses dikirim!")

    # Screenshot
    reports = Path("reports/multi_browser")
    reports.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    page.screenshot(path=reports / f"{browser_name}_{ts}.png")

    print(f"🧭 {browser_name}: test sukses & screenshot tersimpan.")
