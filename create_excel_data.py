from openpyxl import Workbook
import os

# Pastikan folder tests/data ada
os.makedirs("tests/data", exist_ok=True)

# Buat workbook dan worksheet
wb = Workbook()
ws = wb.active
ws.title = "Sheet1"

# Header kolom
ws.append(["username", "password", "expected_text"])

# Data test login
data_rows = [
    ["admin", "12345", "Login successful"],
    ["user", "wrongpass", "Invalid password"],
    ["", "12345", "Username required"],
    ["admin", "", "Password required"]
]

# Tambahkan baris data ke sheet
for row in data_rows:
    ws.append(row)

# Simpan file Excel
file_path = "tests/data/login_data.xlsx"
wb.save(file_path)

print(f"✅ File Excel test data berhasil dibuat di: {file_path}")
