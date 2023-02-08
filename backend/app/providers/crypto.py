import bcrypt


class Bcrypt(object):
    rounds = 10
    prefix = "2a"

    def __init__(self, rounds: int = 10, prefix: str = "2a") -> None:
        self.rounds = rounds
        self.prefix = prefix.encode()

    def unicode_to_bytes(self, unicode_string: str):
        return (
            bytes(unicode_string, "utf-8")
            if isinstance(unicode_string, str)
            else unicode_string
        )

    def generate_password_hash(self, password: str) -> str:
        if not password:
            raise ValueError("Password must be non-empty")

        salt = bcrypt.gensalt(self.rounds, self.prefix)
        return bcrypt.hashpw(password.encode(), salt).decode()

    def check_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())


def generate_password_hash(password: str) -> str:
    return Bcrypt().generate_password_hash(password)


def check_password(password: str, hashed_password: str) -> bool:
    return Bcrypt().check_password(password, hashed_password)
