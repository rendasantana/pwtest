from pathlib import Path

def fix_toggle_detail_function():
    report_path = Path("reports/report.html")
    if not report_path.exists():
        print("❌ File report.html tidak ditemukan di folder reports/")
        return

    html = report_path.read_text(encoding="utf-8")

    # Tambahkan definisi fungsi toggleDetail() di dalam <head> agar semua onclick bisa jalan
    if "function toggleDetail" in html:
        print("✅ Fungsi toggleDetail sudah ada.")
        return

    inject_code = """
<script>
function toggleDetail(button) {
  try {
    const tr = button.closest("tr");
    const detailRow = tr.nextElementSibling;
    if (!detailRow) return;

    const extra = detailRow.querySelector(".extra");
    if (!extra) return;

    const isHidden = extra.style.display === "none" || getComputedStyle(extra).display === "none";
    extra.style.display = isHidden ? "block" : "none";
    button.textContent = isHidden ? "▼ Sembunyikan Detail" : "▶ Lihat Detail";
  } catch (err) {
    console.error("Error toggleDetail:", err);
  }
}
</script>
"""

    if "</head>" in html:
        html = html.replace("</head>", inject_code + "\n</head>")
    else:
        html = inject_code + html

    report_path.write_text(html, encoding="utf-8")
    print("✅ Fungsi toggleDetail berhasil ditambahkan ke report.html")

if __name__ == "__main__":
    fix_toggle_detail_function()
