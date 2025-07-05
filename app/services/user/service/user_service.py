from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_db
from fastapi import HTTPException, status, Depends
from app.services.user.repository.user_repo import UserRepo


class UserService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
        self.user_repo = UserRepo(db)

    async def create_user(self, payload):

        existing_user = await self.user_repo.get_user_with_phone_email(payload.email, payload.phone)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email or phone already exists."
            )

        new_user = await self.user_repo.create_new_user(payload)

        return new_user
