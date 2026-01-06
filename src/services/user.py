from datetime import datetime, timedelta, timezone
from uuid import uuid4, UUID
from typing import Optional, Any

from src.domain.entities import User, RefreshToken
from src.domain.exceptions import UserBannedException
from src.infrastructure.db.repositories.user import UserRepository
from src.infrastructure.db.repositories.refresh_token import RefreshTokenRepository
from src.infrastructure.security.password import verify_password, get_password_hash
from src.infrastructure.security.token import (
    create_access_token, create_refresh_token, decode_refresh_token
)
from src.config.security import SecurityConfig

class UserService:
    def __init__(
        self,
        user_repo: UserRepository,
        token_repo: RefreshTokenRepository,
        config: SecurityConfig,
    ) -> None:
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.config = config

    async def authenticate(self, tg_id_or_username: str | int, password_raw: str) -> User:
        if isinstance(tg_id_or_username, int):
            user = await self.user_repo.get_by_tg_id(tg_id_or_username)
        else:
            user = await self.user_repo.get_by_username(tg_id_or_username)
        
        if not user or not verify_password(password_raw, user.hashed_password):
            return None

        if user.is_banned:
            raise UserBannedException(f"User {user.username} is banned.")
            
        return user

    async def login(self, identifier: str | int, password_raw: str) -> Optional[dict[str, str]]:
        user = await self.authenticate(identifier, password_raw)
        if not user:
            return None
            
        return await self._create_session(user)

    async def refresh_tokens(self, refresh_token_str: str) -> Optional[dict[str, str]]:
        try:
            payload = decode_refresh_token(refresh_token_str)
        except Exception:
            return None

        db_token = await self.token_repo.get_by_token(refresh_token_str)
        if not db_token or db_token.expired_date < datetime.now(timezone.utc):
            return None

        user = await self.user_repo.get(db_token.user_id)
        if not user or user.is_banned:
            return None

        await self.token_repo.delete(db_token.id)
        return await self._create_session(user)

    async def create_user(self, **user_data: Any) -> User:
        """Принимает именованные аргументы, хеширует пароль и создает Entity."""
        if 'password' in user_data:
            password_raw = user_data.pop('password')
            user_data['hashed_password'] = get_password_hash(password_raw)

        new_user = User(**user_data)
        
        return await self.user_repo.add(new_user)

    async def update_user(self, user_id: int, **update_data: Any) -> Optional[User]:
        user = await self.user_repo.get(user_id)
        if not user:
            return None
            
        if 'password' in update_data:
            password_raw = update_data.pop('password')
            user.hashed_password = get_password_hash(password_raw)
            
        for field, value in update_data.items():
            if hasattr(user, field):
                setattr(user, field, value)
        
        return await self.user_repo.update(user)
    
    async def _create_session(self, user: User) -> dict[str, str]:
        access_exp = datetime.now(timezone.utc) + self.config.access_exp_delta
        access_token = create_access_token({
            "user_id": user.id, 
            "exp": int(access_exp.timestamp())
        })
        refresh_exp = datetime.now(timezone.utc) + self.config.refresh_exp_delta
        jti = uuid4()
        refresh_token_str = create_refresh_token({
            "user_id": user.id, 
            "jti": str(jti), 
            "exp": int(refresh_exp.timestamp())
        })
        token_entity = RefreshToken(
            id=jti,
            user_id=user.id,
            refresh_token=refresh_token_str,
            expired_date=refresh_exp
        )
        await self.token_repo.add(token_entity)
        
        return {
            "access_token": access_token, 
            "refresh_token": refresh_token_str
        }