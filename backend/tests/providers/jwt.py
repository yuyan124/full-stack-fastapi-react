import pytest

from app.providers import jwt


def test_password_hash():
    email = "test@test.com"
    token = jwt.create_password_reset_token(email)
    r = jwt.verify_password_reset_token(token)

    assert email == r
