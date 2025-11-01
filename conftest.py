import logging
from pathlib import Path
import pytest
import base64

def pytest_configure(config):
    Path("reports/screenshots").mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("reports/test_log.txt", mode="a", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Tambahkan screenshot di kolom kanan sejajar dengan tombol expand (bukan di bawah log)"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        page = item.funcargs.get("page", None)
        if not page:
            return

        screenshot_path = Path("reports/screenshots") / f"{item.name}.png"
        try:
            page.screenshot(path=screenshot_path, full_page=True)
        except Exception as e:
            logging.warning(f"Gagal ambil screenshot: {e}")
            return

        pytest_html = item.config.pluginmanager.getplugin("html")
        if not pytest_html:
            return

        with open(screenshot_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")

        # Thumbnail sejajar dengan kolom expand [+]
        html_img = f"""
        <style>
            .screenshot-cell {{
                float: right;
                margin-left: 10px;
                margin-top: -5px;
            }}
            .screenshot-thumb {{
                height: 80px;
                border: 1px solid #ccc;
                border-radius: 5px;
                cursor: pointer;
                transition: 0.2s;
            }}
            .screenshot-thumb:hover {{
                opacity: 0.85;
            }}
            .modal {{
                display: none;
                position: fixed;
                z-index: 9999;
                padding-top: 60px;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                overflow: auto;
                background-color: rgba(0,0,0,0.9);
            }}
            .modal-content {{
                margin: auto;
                display: block;
                width: 80%;
                max-width: 900px;
                border-radius: 8px;
            }}
            .close {{
                position: absolute;
                top: 30px;
                right: 45px;
                color: #fff;
                font-size: 40px;
                font-weight: bold;
                cursor: pointer;
            }}
        </style>

        <div class="screenshot-cell">
            <img src="data:image/png;base64,{encoded}" class="screenshot-thumb" onclick="openModal_{item.name}()" alt="Screenshot">
        </div>

        <div id="modal_{item.name}" class="modal">
            <span class="close" onclick="closeModal_{item.name}()">&times;</span>
            <img class="modal-content" src="data:image/png;base64,{encoded}">
        </div>

        <script>
            function openModal_{item.name}() {{
                document.getElementById('modal_{item.name}').style.display = 'block';
            }}
            function closeModal_{item.name}() {{
                document.getElementById('modal_{item.name}').style.display = 'none';
            }}
        </script>
        """

        extras = getattr(rep, "extras", [])
        extras.append(pytest_html.extras.html(html_img))
        rep.extras = extras

