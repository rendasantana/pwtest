# tests/test_form_interactions.py
import time
from playwright.sync_api import Page

def test_form_interactions(page: Page):
    page.set_default_timeout(30000)

    html_content = """
    <html>
      <body>
        <h2>Latihan Form Interactions</h2>
        <form id="f">
          Nama Depan: <input name='firstname'><br>
          Nama Belakang: <input name='lastname'><br>
          <label><input type='checkbox' id='bike'> Saya punya sepeda</label><br>
          <label><input type='radio' name='gender' value='male'> Laki-laki</label>
          <label><input type='radio' name='gender' value='female'> Perempuan</label><br>
          <select id='country'>
            <option value=''>Pilih Negara</option>
            <option value='id'>Indonesia</option>
            <option value='my'>Malaysia</option>
            <option value='sg'>Singapore</option>
          </select><br>
          <textarea id='message'></textarea><br>
          <button type='submit'>Kirim</button>
        </form>
      </body>
    </html>
    """
    page.set_content(html_content)

    page.fill("input[name='firstname']", "Renda")
    page.fill("input[name='lastname']", "Santana")
    page.check("#bike")
    page.check("input[value='male']")
    page.select_option("#country", "id")
    page.fill("#message", "Ini pesan latihan Playwright oleh Renda!")

    # Cetak hasil interaksi (tidak submit karena tidak ada handler)
    print("✅ Form interaksi selesai berhasil dijalankan.")

    # singgah sebentar supaya manual inspeksi di headed mode terlihat
    time.sleep(1)
