from app.services.geolocation.repository.geolocation_repo import get_localities


class GeolocationService:
    def __init__(self, db):
        self.db = db

    async def get_localities(self, payload):
        response = await get_localities(filters=payload, db=self.db)
        return response

