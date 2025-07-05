from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from app.db.connection import db_connection

router = APIRouter(tags=["reztic_healthcheck"])


@router.get("/health", summary="Healthcheck for DB and service")
async def healthcheck():
    db_status, db_message = await check_database()

    overall_status = "Healthy" if db_status == "Healthy" else "Unhealthy"

    return {
        "status": overall_status,
        "components": {
            "database": {
                "status": db_status,
                "message": db_message,
            }
        }
    }


async def check_database():
    try:
        async with db_connection.get_session() as session:
            await session.execute(text("SELECT 1"))
        return "Healthy", "Database connection is healthy."
    except OperationalError as e:
        return "Unhealthy", f"Database connection failed: {str(e)}"
    except Exception as e:
        return "Unhealthy", f"Unexpected error: {str(e)}"
