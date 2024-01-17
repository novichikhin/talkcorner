from passlib.context import CryptContext


def get_password_hash(crypt_context: CryptContext, password: str) -> str:
    return crypt_context.hash(password)


def verify_password(
    crypt_context: CryptContext,
    plain_password: str,
    hashed_password: str
) -> bool:
    return crypt_context.verify(plain_password, hashed_password)
