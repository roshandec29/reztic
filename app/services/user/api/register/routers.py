from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_db
from app.services.user.schemas.user_schemas import UserRegisterRequest, OTPRequest, VerifyOTPRequest
from app.services.user.service.user_service import UserService
from app.services.user.service.auth_service import AuthService
from app.utils.errors import OTPError, OTPReadError

router = APIRouter(
    prefix="/api/v1",
    tags=["users"]
)


@router.post(
    "/users/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Creates a new user with the provided details after verifying no duplicate email/phone exists."
)
async def register_user(
    payload: UserRegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    new_user = await user_service.create_user(payload)

    try:
        await db.commit()
        await db.refresh(new_user)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"User registration failed: {str(e)}"
        )

    return {
        "message": "User registered successfully",
        "user_id": str(new_user.id)
    }


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

    auth_service = AuthService(db)
    response = await auth_service.verify_user_otp(data)
    try:
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


