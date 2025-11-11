import pytest
from playwright.sync_api import expect

@pytest.mark.smoke
def test_dynamic_dropdown_checkbox(page):
    """Latihan 7: Dropdown memunculkan checkbox dinamis + validasi"""

    try:
        # 1️⃣ Buat halaman HTML lokal
        html_content = """
        <!DOCTYPE html>
        <html>
        <body>
            <h2>Latihan 7: Dropdown + Checkbox Dinamis</h2>

            <label for="country">Pilih Negara:</label>
            <select id="country">
                <option value="">--Pilih--</option>
                <option value="indonesia">Indonesia</option>
                <option value="japan">Japan</option>
            </select>

            <div id="hobby-section" style="display:none; margin-top:15px;">
                <label>Pilih Hobi:</label><br>
                <input type="checkbox" id="cycling" name="hobby" value="cycling"> <label for="cycling">Cycling</label><br>
                <input type="checkbox" id="reading" name="hobby" value="reading"> <label for="reading">Reading</label><br>
            </div>

            <button id="submitBtn">Kirim</button>
            <p id="result" style="font-weight:bold; color:green;"></p>

            <script>
                const countrySelect = document.getElementById("country");
                const hobbySection = document.getElementById("hobby-section");
                const result = document.getElementById("result");
                const submitBtn = document.getElementById("submitBtn");

                countrySelect.addEventListener("change", () => {
                    if (countrySelect.value === "indonesia") {
                        hobbySection.style.display = "block";
                    } else {
                        hobbySection.style.display = "none";
                    }
                });

                submitBtn.addEventListener("click", () => {
                    const selectedCountry = countrySelect.value;
                    if (!selectedCountry) {
                        result.textContent = "❌ Harap pilih negara!";
                        result.style.color = "red";
                        return;
                    }

                    if (selectedCountry === "indonesia") {
                        const checked = document.querySelectorAll("input[name='hobby']:checked");
                        if (checked.length === 0) {
                            result.textContent = "⚠️ Harap pilih setidaknya satu hobi!";
                            result.style.color = "orange";
                        } else {
                            result.textContent = "✅ Data berhasil dikirim!";
                            result.style.color = "green";
                        }
                    } else {
                        result.textContent = "✅ Data berhasil dikirim!";
                        result.style.color = "green";
                    }
                });
            </script>
        </body>
        </html>
        """
        page.set_content(html_content)

        # 2️⃣ Pilih negara Indonesia → hobby section muncul
        page.select_option("#country", "indonesia")
        expect(page.locator("#hobby-section")).to_be_visible()

        # 3️⃣ Klik submit tanpa memilih hobby
        page.click("#submitBtn")
        expect(page.locator("#result")).to_have_text("⚠️ Harap pilih setidaknya satu hobi!")

        # 4️⃣ Centang salah satu hobby dan submit ulang
        page.check("#cycling")
        page.click("#submitBtn")
        expect(page.locator("#result")).to_have_text("✅ Data berhasil dikirim!")

        print("✅ Test berhasil: Dropdown dan checkbox dinamis bekerja sesuai logika!")

    except Exception as e:
        pytest.fail(f"Terjadi error di Latihan 7: {e}")
