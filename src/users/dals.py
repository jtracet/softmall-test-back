from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dal import BaseDAL
from src.models.src.modules.user import User


class UserDAL(BaseDAL[User]):
    async def get_user_by_username(self, db: AsyncSession, username: str) -> User | None:
        query = select(User).where(User.username == username)
        result = await db.execute(query)
        return result.scalars().first()


user_dal = UserDAL(User)

from src.models.src.modules.user import UserRole


class UsersRolesDAL(BaseDAL[UserRole]):
    pass


users_roles_dal = UsersRolesDAL(UserRole)
