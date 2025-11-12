import pytest
from playwright.sync_api import expect

@pytest.mark.smoke
def test_handle_alerts(page):
    """Latihan 12: Menangani Alert, Confirm, dan Prompt Box"""

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Latihan 12: Handle Alerts</title>
        <style>
            body { font-family: Arial; margin: 30px; }
            button { margin: 10px; }
            #result { margin-top: 15px; color: green; font-weight: bold; }
        </style>
    </head>
    <body>
        <h2>Latihan Handle Alert, Confirm, Prompt</h2>

        <button id="alertBtn">Show Alert</button>
        <button id="confirmBtn">Show Confirm</button>
        <button id="promptBtn">Show Prompt</button>

        <p id="result"></p>

        <script>
            document.getElementById("alertBtn").onclick = function() {
                alert("Halo dari Alert Box!");
                document.getElementById("result").textContent = "Alert ditutup!";
            };

            document.getElementById("confirmBtn").onclick = function() {
                const result = confirm("Apakah kamu yakin?");
                document.getElementById("result").textContent = result ? "Kamu memilih OK!" : "Kamu memilih Cancel!";
            };

            document.getElementById("promptBtn").onclick = function() {
                const name = prompt("Masukkan nama kamu:", "Renda");
                if (name) {
                    document.getElementById("result").textContent = `Halo, ${name}!`;
                } else {
                    document.getElementById("result").textContent = "Prompt dibatalkan!";
                }
            };
        </script>
    </body>
    </html>
    """

    # 1️⃣ Set halaman HTML
    page.set_content(html_content)

    # 2️⃣ Tangani alert
    page.once("dialog", lambda dialog: dialog.accept())
    page.click("#alertBtn")
    expect(page.locator("#result")).to_have_text("Alert ditutup!")

    # 3️⃣ Tangani confirm → pilih Cancel
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.click("#confirmBtn")
    expect(page.locator("#result")).to_have_text("Kamu memilih Cancel!")

    # 4️⃣ Tangani confirm → pilih OK
    page.once("dialog", lambda dialog: dialog.accept())
    page.click("#confirmBtn")
    expect(page.locator("#result")).to_have_text("Kamu memilih OK!")

    # 5️⃣ Tangani prompt → isi nama custom
    page.once("dialog", lambda dialog: dialog.accept("Renda QA"))
    page.click("#promptBtn")
    expect(page.locator("#result")).to_have_text("Halo, Renda QA!")

    print("✅ Test berhasil: Semua alert, confirm, dan prompt berhasil ditangani!")
