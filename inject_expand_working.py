from pathlib import Path

def inject_working_toggle():
    report_path = Path("reports/report.html")
    if not report_path.exists():
        print("❌ File report.html tidak ditemukan.")
        return

    html = report_path.read_text(encoding="utf-8")

    # Hapus versi toggleDetail lama kalau ada
    html = html.replace("onclick=\"toggleDetail", "class=\"expandable\" data-target")

    # Tambahkan JavaScript baru di akhir file (atau sebelum </body>)
    script = """
<script>
document.addEventListener("DOMContentLoaded", function() {
  console.log("✅ Toggle script aktif");
  document.querySelectorAll('button.toggle-detail').forEach(btn => {
    btn.addEventListener('click', () => {
      const name = btn.getAttribute('data-name');
      const detail = document.getElementById('detail-' + name);
      if (!detail) return;
      const visible = detail.style.display === 'block';
      detail.style.display = visible ? 'none' : 'block';
      btn.textContent = visible ? 'Lihat Detail ⬇️' : 'Sembunyikan Detail ⬆️';
    });
  });

  // Tambahan kompatibilitas untuk pytest-html default rows
  document.querySelectorAll('button[onclick]').forEach(btn => {
    btn.addEventListener('click', e => {
      e.preventDefault();
      const tr = btn.closest('tr');
      if (!tr) return;
      const next = tr.nextElementSibling;
      if (!next) return;
      next.style.display = next.style.display === 'none' ? '' : 'none';
    });
  });
});
</script>
"""

    # Sisipkan sebelum </body>
    if "</body>" in html:
        html = html.replace("</body>", script + "\n</body>")
    else:
        html += script

    report_path.write_text(html, encoding="utf-8")
    print("✅ Script toggle interaktif berhasil disuntik ke report.html")

if __name__ == "__main__":
    inject_working_toggle()
