from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_db
from app.services.user.schemas.user_schemas import OTPRequest, VerifyOTPRequest
from app.services.user.service.auth_service import AuthService
from app.utils.errors import OTPError, OTPReadError

router = APIRouter(
    prefix="/api/v1",
    tags=["auth"]
)


@router.post("/auth/request-otp")
async def request_otp(data: OTPRequest, db: AsyncSession = Depends(get_db)):
    try:
        auth_service = AuthService(db)
        otp = await auth_service.user_otp_generate(data)

        await db.commit()
        if otp:
            return {"message": f"OTP sent successfully. {otp}"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"OTP not sent: {str(e)}"
        )


@router.post("/auth/verify-otp", status_code=status.HTTP_200_OK)
async def request_otp(data: VerifyOTPRequest, db: AsyncSession = Depends(get_db)):
    try:
        auth_service = AuthService(db)
        response = await auth_service.verify_user_otp(data)
        await db.commit()
        if response.get("success"):
            return {
                    "message": "OTP verified successfully.",
                    "access_token": response.get("access_token"),
                    "refresh_token": response.get("refresh_token"),
                    "token_type": response.get("token_type")
                    }

    except OTPReadError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=f"OTP not sent: {str(e.detail)}"
        )
    except OTPError as e:
        raise HTTPException(
            status_code=400,
            detail=f"OTP not sent: {str(e.detail)}"
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"OTP not sent: {str(e)}"
        )


