import secrets
from typing import Any

import jwt

from application.users.schemas.tokens import AccessTokenPayload, RefreshTokenPayload
from config.fastapi import fastapi_settings


def create_access_token(access_token_payload: AccessTokenPayload) -> str:
    to_encode = access_token_payload.model_dump()
    to_encode['user_id'] = str(access_token_payload.user_id)
    encoded_jwt = jwt.encode(
        to_encode, fastapi_settings.SECURITY.SECRET_KEY, algorithm=fastapi_settings.SECURITY.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(refresh_token_payload: RefreshTokenPayload) -> str:
    to_encode = refresh_token_payload.model_dump()
    to_encode['jti'] = str(refresh_token_payload.jti)
    to_encode['user_id'] = str(refresh_token_payload.user_id)
    encoded_jwt = jwt.encode(
        to_encode, fastapi_settings.SECURITY.SECRET_KEY, algorithm=fastapi_settings.SECURITY.ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> Any:
    payload = jwt.decode(
        jwt=token, key=fastapi_settings.SECURITY.SECRET_KEY, algorithms=[fastapi_settings.SECURITY.ALGORITHM]
    )
    return payload


def decode_access_token(token: str) -> AccessTokenPayload:
    payload = decode_token(token)
    return AccessTokenPayload(**payload)


def decode_refresh_token(token: str) -> RefreshTokenPayload:
    payload = decode_token(token)
    return RefreshTokenPayload(**payload)


def generate_system_token(length: int = 64) -> str:
    return secrets.token_urlsafe(length)
