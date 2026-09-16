from datetime import date
from fastapi import APIRouter, HTTPException, Query

from service.KBO_service import KBOService

def create_kbo_router(kbo_service: KBOService):
    router = APIRouter(prefix="/kbo", tags=["KBO"])


    @router.get("/games")
    def get_games(
        target_date: date = Query(default_factory=date.today, alias="date")
    ):
        try:
            games = kbo_service.get_games(target_date)
        except RuntimeError as e:
            raise HTTPException(status_code=502, detail=str(e))

        if not games:
            return {"games": [], "message": "해당 날짜에 경기가 없습니다."}

        return {"games": games}

    return router