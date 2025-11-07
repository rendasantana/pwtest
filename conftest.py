import logging
import base64
from datetime import datetime
from pathlib import Path
import pytest

# === Setup awal ===
def pytest_configure(config):
    """Setup folder dan logger"""
    Path("reports/screenshots").mkdir(parents=True, exist_ok=True)
    Path("reports/videos").mkdir(parents=True, exist_ok=True)
    Path("reports/logs").mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("reports/logs/global_log.txt", mode="a", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )


@pytest.fixture(scope="function", autouse=True)
def per_test_logger(request):
    """Logger per test"""
    log_file = Path(f"reports/logs/{request.node.name}.log")
    handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger = logging.getLogger(request.node.name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    yield logger
    handler.close()
    logger.removeHandler(handler)


@pytest.fixture(scope="function")
def record_video(browser):
    """Fixture untuk merekam video"""
    videos_dir = Path("reports/videos")
    videos_dir.mkdir(parents=True, exist_ok=True)
    context = browser.new_context(record_video_dir=videos_dir)
    page = context.new_page()
    yield page
    context.close()


# === Hook report ===
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Tampilkan summary + konten detail (screenshot, video, log)"""
    outcome = yield
    rep = outcome.get_result()
    if rep.when != "call":
        return

    page = item.funcargs.get("page") or item.funcargs.get("record_video")
    pytest_html = item.config.pluginmanager.getplugin("html")
    if not pytest_html:
        return

    status_icon = "✅" if rep.passed else "❌"
    duration = f"{rep.duration:.2f}s"

    # Screenshot
    screenshot_path = Path("reports/screenshots") / f"{item.name}_{datetime.now():%Y%m%d_%H%M%S}.png"
    encoded_img = ""
    try:
        page.screenshot(path=screenshot_path, full_page=True)
        with open(screenshot_path, "rb") as f:
            encoded_img = base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        logging.warning(f"Gagal ambil screenshot: {e}")

    # Video
    encoded_video = ""
    videos_dir = Path("reports/videos")
    vids = sorted(videos_dir.glob("*.webm"), key=lambda x: x.stat().st_mtime, reverse=True)
    if vids:
        latest_video = vids[0]
        with open(latest_video, "rb") as v:
            encoded_video = base64.b64encode(v.read()).decode("utf-8")

    # Log
    log_file = Path(f"reports/logs/{item.name}.log")
    log_html = "Tidak ada log."
    if log_file.exists():
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            formatted = []
            for line in lines:
                color = "#ccc"
                if "ERROR" in line:
                    color = "#ff6b6b"
                elif "WARNING" in line:
                    color = "#ffd166"
                elif "INFO" in line:
                    color = "#06d6a0"
                formatted.append(f'<span style="color:{color};">{line.strip()}</span>')
            log_html = "<br>".join(formatted[-60:])

        # --- HTML lengkap ---
    html_block = f"""
    <style>
        .summary-box {{
            background:#222;
            border-left:6px solid {'#28a745' if rep.passed else '#dc3545'};
            color:#fff;
            padding:8px 12px;
            border-radius:8px;
            font-family:Segoe UI, sans-serif;
            margin-top:10px;
        }}
        .toggle-detail {{
            background:#0078d4;
            color:white;
            border:none;
            border-radius:6px;
            padding:4px 10px;
            cursor:pointer;
            font-size:12px;
        }}
        .detail-content {{
            display:none;
            margin-top:10px;
            border:1px solid #333;
            border-radius:8px;
            padding:10px;
            background:#111;
        }}
        .flex-container {{
            display:flex;
            flex-wrap:wrap;
            gap:15px;
            justify-content:space-between;
        }}
        .flex-item {{
            flex:1;
            min-width:250px;
            background:#1b1b1b;
            padding:8px;
            border-radius:8px;
            color:#dcdcdc;
        }}
    </style>

    <div class="summary-box">
        <b>{status_icon} {item.name}</b> &nbsp;&nbsp; ⏱ {duration}
        <button onclick="toggleDetail(this)">Lihat Detail</button>
    </div>

    <div id="detail-{item.name}" class="detail-content">
        <div class="flex-container">
            <div class="flex-item" style="text-align:center;">
                <b>📸 Screenshot:</b><br>
                <img src="data:image/png;base64,{encoded_img}" style="max-width:100%; border-radius:8px;">
            </div>

            <div class="flex-item" style="text-align:center;">
                <b>🎥 Video Test:</b><br>
                <video width="100%" controls style="border-radius:8px;">
                    <source src="data:video/webm;base64,{encoded_video}" type="video/webm">
                    Browser tidak mendukung video.
                </video>
            </div>

            <div class="flex-item">
                <b>🧾 Log:</b><br>
                <div style="font-family:monospace; max-height:200px; overflow:auto;">{log_html}</div>
            </div>
        </div>
    </div>

    <script>
        window.toggleDetail = function(name) {{
            const el = document.getElementById('detail-' + name);
            const btn = document.getElementById('btn-' + name);
            if (!el || !btn) return;

            if (el.style.display === 'none' || el.style.display === '') {{
                el.style.display = 'block';
                btn.innerHTML = 'Sembunyikan Detail ⬆️';
            }} else {{
                el.style.display = 'none';
                btn.innerHTML = 'Lihat Detail ⬇️';
            }}
        }};
    </script>
    """

    extras = getattr(rep, "extras", [])
    extras.append(pytest_html.extras.html(html_block))
    rep.extras = extras
