import requests, random
from typing import Literal, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from app.services.user.models.otp_models import OTP
from sqlalchemy import delete, select
from .errors import OTPReadError, OTPError
from fastapi import status
from app.config import config

class SMSUtils:
    @staticmethod
    def send_sms(
            phone_number: str,
            message: str,
            provider: Literal["fast2sms", "smshorizon", "textlocal", "exotel"],
            api_key: str = None,
            sender_id: Optional[str] = None,
            sid: Optional[str] = None,
            token: Optional[str] = None,
    ) -> dict:
        """
        Sends an SMS using the specified provider.

        :param phone_number: Recipient's phone number (Indian number without +91)
        :param message: SMS content
        :param provider: SMS provider name ("fast2sms", "smshorizon", "textlocal", "exotel")
        :param api_key: API key for authentication
        :param sender_id: Sender ID (Required for some providers)
        :param sid: SID (Only for Exotel)
        :param token: Auth Token (Only for Exotel)
        :return: Response JSON or text
        """

        if provider == "fast2sms":
            url = "https://www.fast2sms.com/dev/bulkV2"
            payload = {
                "message": message,
                "language": "english",
                "route": "q",
                "numbers": phone_number,
            }
            headers = {
                "authorization": "td7Ywhi2FgMokNjxRA0IPzKVZC3fen4Uv8SuL9brEXslQmq1WBSLJqpsWnD4eNvGclI0UyFXgwu98zQh",
                "cache-control": "no-cache"
            }

            response = requests.post(url, data=payload, headers=headers)
            print(response.json())
            return response.json()

        elif provider == "smshorizon":
            url = f"https://www.smshorizon.in/api/sendsms.php?user=your_username&apikey={api_key}&mobile={phone_number}&message={message}&senderid={sender_id}&type=txt"
            response = requests.get(url)
            return response.text

        elif provider == "textlocal":
            url = "https://api.textlocal.in/send/"
            payload = {
                "apikey": api_key,
                "numbers": phone_number,
                "message": message,
                "sender": sender_id or "TXTLCL",
            }
            response = requests.post(url, data=payload)
            return response.json()

        elif provider == "exotel":
            if not (sid and token):
                raise ValueError("Exotel requires 'sid' and 'token'.")
            url = f"https://api.exotel.com/v1/Accounts/{sid}/Sms/send"
            payload = {
                "From": sender_id,
                "To": phone_number,
                "Body": message,
            }
            response = requests.post(url, data=payload, auth=(sid, token))
            return response.json()

        else:
            raise ValueError("Invalid provider. Choose from 'fast2sms', 'smshorizon', 'textlocal', 'exotel'.")

    async def generate_otp(self, db: AsyncSession, phone_number: str, otp_type: str) -> str:
        otp = str(random.randint(100000, 999999))

        # delete old OTP
        await db.execute(
            delete(OTP).where(OTP.phone_number == phone_number)
        )

        expires_at = datetime.now() + timedelta(minutes=config.OTP_EXPIRE_MINUTES)

        otp_entry = OTP(
            phone_number=phone_number,
            otp_hash=otp,
            otp_type=otp_type,
            expires_at=expires_at,
            is_used=False
        )

        db.add(otp_entry)

        # optionally trigger SMS here
        # self.send_sms(phone_number=phone_number, message=f"Your OTP is {otp}", provider="fast2sms")

        return otp

    @staticmethod
    async def verify_otp(db: AsyncSession, phone_number: str, otp: str) -> bool:
        """
        Verifies OTP from the database.
        """
        now = datetime.now(timezone.utc)

        stmt = select(OTP).where(
            OTP.phone_number == phone_number
        ).order_by(OTP.created_at.desc())

        result = await db.execute(stmt)
        otp_entry = result.scalar_one_or_none()

        if not otp_entry:
            raise OTPError(detail="No OTP found for this phone number.")

        # if otp_entry.is_used:
        #     raise OTPReadError(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP already used.")

        if now > otp_entry.expires_at:
            await db.delete(otp_entry)
            raise OTPReadError(status_code=status.HTTP_401_UNAUTHORIZED, detail="OTP expired.")

        if otp_entry.otp_hash != otp:
            raise OTPReadError(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid OTP.")

        # otp_entry.is_used = True

        return True
