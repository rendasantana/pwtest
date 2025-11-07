import pytest

@pytest.mark.parametrize(
    "username,password,expected_text",
    [
        ("admin", "12345", "Login successful"),
        ("user", "wrongpass", "Invalid password"),
        ("", "12345", "Username required"),
        ("admin", "", "Password required"),
    ]
)
def test_login_with_fixture(page, username, password, expected_text):
    print(f"\nMenguji username={username}, password={password}")

    # Simulasi hasil login
    if username == "admin" and password == "12345":
        result = "Login successful"
    elif username == "":
        result = "Username required"
    elif password == "":
        result = "Password required"
    else:
        result = "Invalid password"

    # Validasi hasil
    assert result == expected_text, f"Dapat: {result}, harapan: {expected_text}"
