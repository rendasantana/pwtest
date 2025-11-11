from pathlib import Path

def inject_expand_script():
    report_path = Path("reports/report.html")
    if not report_path.exists():
        print("❌ File report.html tidak ditemukan di folder reports/")
        return

    html = report_path.read_text(encoding="utf-8")

    # Cegah duplikasi
    if "Error saat toggle detail" in html:
        print("✅ Script sudah pernah diinject sebelumnya.")
        return

    # Script dan CSS untuk expand
    inject_code = """
<!-- Injected Expand Fix -->
<style>
.expand {
  background: none;
  border: none;
  font-size: 13px;
  color: #0078d4;
  cursor: pointer;
}
.expand:hover {
  text-decoration: underline;
}
</style>
<script>
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".expand").forEach(button => {
    button.addEventListener("click", function () {
      try {
        const tr = this.closest("tr");
        const detailRow = tr.nextElementSibling;
        if (!detailRow) return;

        const extra = detailRow.querySelector(".extra");
        if (!extra) return;

        const isHidden = extra.style.display === "none" || getComputedStyle(extra).display === "none";
        extra.style.display = isHidden ? "block" : "none";

        this.textContent = isHidden ? "▼ Sembunyikan Detail" : "▶ Lihat Detail";
        this.style.cursor = "pointer";
      } catch (err) {
        console.error("Error saat toggle detail:", err);
      }
    });
  });
});
</script>
<!-- End Expand Fix -->
"""

    # Sisipkan sebelum </body>
    if "</body>" in html:
        html = html.replace("</body>", inject_code + "\n</body>")
        report_path.write_text(html, encoding="utf-8")
        print("✅ Script expand fix berhasil disisipkan ke report.html")
    else:
        print("⚠️ Tidak ditemukan tag </body> — gagal inject script.")


if __name__ == "__main__":
    inject_expand_script()
