from app.services.user.models.user_models import User, UserRole
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.db.connection import get_db
from fastapi import Depends
from app.utils.password import hash_password
from sqlalchemy.orm import selectinload


class UserRepo:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_user_with_phone_email(self, email, phone):
        stmt = (
            select(User)
            .options(selectinload(User.roles).joinedload(UserRole.role))
            .where(
                or_(User.email == email, User.phone == phone)
            )
        )
        result = await self.db.execute(stmt)
        existing_user = result.scalar_one_or_none()
        return existing_user

    async def create_new_user(self, payload):
        new_user = User(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            phone=payload.phone,
            password_hash=hash_password(payload.password),
            dob=payload.dob,
            gender=payload.gender,
            company_id=payload.company_id,
            languages=",".join(payload.languages) if payload.languages else None,
            kyc_status="pending",
        )

        self.db.add(new_user)
        await self.db.flush()

        new_user_role = UserRole(
            user_id=new_user.id,
            role_id=payload.role
        )

        self.db.add(new_user_role)

        return new_user
