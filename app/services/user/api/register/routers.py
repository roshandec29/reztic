from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_db
from app.services.user.schemas.user_schemas import UserRegisterRequest
from app.services.user.service.user_service import UserService

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
