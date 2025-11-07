import csv
import pytest
from playwright.sync_api import sync_playwright

# Fungsi untuk membaca data CSV
def read_csv_data(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [(row['username'], row['password'], row['expected_text']) for row in reader]
    return data


@pytest.mark.parametrize(
    "username,password,expected_text",
    read_csv_data("tests/data/login_data.csv")
)
def test_login_from_csv(username, password, expected_text):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Simulasi proses login (belum ke web nyata)
        print(f"\nUji username={username}, password={password}")

        if username == "admin" and password == "12345":
            result = "Login successful"
        elif username == "":
            result = "Username required"
        elif password == "":
            result = "Password required"
        else:
            result = "Invalid password"

        assert result == expected_text, f"Dapat: {result}, harapan: {expected_text}"
        browser.close()
