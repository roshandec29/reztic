from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_db
from fastapi import HTTPException, status, Depends
from typing import Dict
from app.services.user.repository.user_repo import UserRepo
from app.utils.sms_utils import SMSUtils
from app.utils.token_utils import create_access_token, create_refresh_token


class AuthService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
        self.user_repo = UserRepo(db)

    async def user_otp_generate(self, data):
        user = await self.user_repo.get_user_with_phone_email('', data.phone)

        if not user:
            raise HTTPException(status_code=404, detail="User with this phone or email not found.")

        otp = await SMSUtils().generate_otp(self.db, phone_number=data.phone, otp_type='login')

        return otp

    async def verify_user_otp(self, data) -> Dict:
        user_data = await self.user_repo.get_user_with_phone_email('', data.phone)

        if not user_data:
            raise HTTPException(status_code=404, detail="User with this phone or email not found.")

        success = await SMSUtils().verify_otp(self.db, phone_number=data.phone, otp=data.otp)

        if success:
            access_token = create_access_token(user_data.to_dict())
            refresh_token = create_refresh_token(user_data.to_dict())

            return {"success": success, "access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

        return {"success": success}
