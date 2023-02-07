import pytest
from app.providers.crypto import check_password, generate_password_hash


def test_password_hash():
    password = "123456"
    hashed_password = generate_password_hash(password)

    r = check_password(password, hashed_password)
    assert r == True

    r = check_password("12345", hashed_password)
    assert r == False
