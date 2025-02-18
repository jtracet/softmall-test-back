from datetime import datetime
from typing import Any

from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.src.modules.auth import Token


class AuthDAL:
    async def create_token(self, db: AsyncSession, data: dict[str, Any]) -> None:
        new_token = Token(**data)
        db.add(new_token)
        await db.commit()

    async def get_token(self, db: AsyncSession, token: str) -> Token | None:
        query = select(Token).where(Token.token == token)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_valid_token_by_user(self, db: AsyncSession, user_id: int) -> Token | None:
        query = select(Token).where(and_(Token.user_id == user_id, Token.expires_at > datetime.utcnow()))
        result = await db.execute(query)
        return result.scalars().first()

    async def delete_token(self, db: AsyncSession, token: str) -> bool:
        query = delete(Token).where(Token.token == token)
        await db.execute(query)
        await db.commit()
        return True

    async def delete_tokens_by_user(self, db: AsyncSession, user_id: int) -> None:
        query = delete(Token).where(Token.user_id == user_id)
        await db.execute(query)
        await db.commit()


auth_dal = AuthDAL()
