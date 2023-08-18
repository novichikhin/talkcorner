import enum


class CredentialType(str, enum.Enum):
    JWT_PAYLOAD = "jwt_payload"
    USER_ID_NOT_UUID = "user_id_not_uuid"
    JWT_ERROR = "jwt_error"
    AUTHORIZATION_NOT_BEARER = "authorization_not_bearer"
