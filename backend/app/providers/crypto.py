import hmac

import bcrypt


def safe_str_cmp(a, b):
    if isinstance(a, str):
        a = a.encode("utf-8")
    if isinstance(b, str):
        b = b.encode("utf-8")

    builtin_safe_str_cmp = getattr(hmac, "compare_digest", None)
    if builtin_safe_str_cmp is not None:
        return builtin_safe_str_cmp(a, b)

    if len(a) != len(b):
        return False

    rv = 0

    for x, y in zip(a, b):
        rv |= x ^ y

    return rv == 0


class Bcrypt(object):
    rounds = 10
    prefix = "2a"

    def unicode_to_bytes(self, unicode_string: str):
        return (
            bytes(unicode_string, "utf-8")
            if isinstance(unicode_string, str)
            else unicode_string
        )

    def generate_password_hash(
        self, password: str, rounds: int = None, prefix: bytes = None
    ):
        if not password:
            raise ValueError("Password must be non-empty")

        rounds = self.rounds if rounds is None else rounds
        prefix = self.prefix if prefix is None else prefix

        password = self.unicode_to_bytes(password)
        prefix = self.unicode_to_bytes(prefix)

        salt = bcrypt.gensalt(rounds=rounds, prefix=prefix)
        return bcrypt.hashpw(password, salt)

    def check_password_hash(self, password: str, password_hash: str):
        password_hash = self.unicode_to_bytes(password_hash)
        password = self.unicode_to_bytes(password)
        return safe_str_cmp(bcrypt.hashpw(password, password_hash), password_hash)


def generate_password_hash(password: str, rounds: int = None):
    return Bcrypt().generate_password_hash(password, rounds)


def check_password_hash(password: str, password_hash: str):
    return Bcrypt().check_password_hash(password_hash, password)
