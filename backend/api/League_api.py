# api/League_api.py

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from service.League_service import LeagueService


# ==================================================
# 요청 데이터 모델
# ==================================================

class LeagueCreateRequest(BaseModel):
    """
    경기 일정 생성 요청 데이터.

    클라이언트에서 다음과 같은 JSON을 보내면 된다.

    {
        "League_id": 1001,
        "game_date": "2026-09-20",
        "game_time": "18:30:00",
        "game_name": "LG 트윈스 vs 두산 베어스",
        "stadium_name": "잠실야구장",
        "stadium_address": "서울특별시 송파구 올림픽로 25"
    }
    """

    League_id: int
    game_date: str
    game_time: str
    game_name: str
    stadium_name: str
    stadium_address: str


class LeagueUpdateRequest(BaseModel):
    """
    경기 일정 수정 요청 데이터.

    수정하지 않는 값은 생략할 수 있다.
    """

    game_date: Optional[str] = None
    game_time: Optional[str] = None
    game_name: Optional[str] = None
    stadium_name: Optional[str] = None
    stadium_address: Optional[str] = None


# ==================================================
# League Router 생성
# ==================================================

def create_League_router(
    League_service: LeagueService
) -> APIRouter:
    """
    LeagueService를 전달받아 League API Router를 생성한다.
    """

    router = APIRouter(
        prefix="/leagues",
        tags=["League"]
    )

    # ==================================================
    # CREATE
    # ==================================================

    @router.post("")
    def create_League(request: LeagueCreateRequest):
        """
        새로운 경기 일정을 생성한다.
        """

        try:
            result = League_service.create_League(
                League_id=request.League_id,
                game_date=request.game_date,
                game_time=request.game_time,
                game_name=request.game_name,
                stadium_name=request.stadium_name,
                stadium_address=request.stadium_address
            )

            return {
                "message": "경기 일정이 생성되었습니다.",
                "data": result
            }

        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

    # ==================================================
    # READ
    # ==================================================

    @router.get("/{League_id}")
    def get_League(League_id: int):
        """
        특정 경기 일정을 조회한다.
        """

        result = League_service.get_League(League_id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="경기 일정을 찾을 수 없습니다."
            )

        return {
            "data": result
        }

    # ==================================================
    # READ ALL
    # ==================================================

    @router.get("")
    def get_Leagues():
        """
        모든 경기 일정을 조회한다.
        """

        result = League_service.get_Leagues()

        return {
            "data": result
        }

    # ==================================================
    # UPDATE
    # ==================================================

    @router.put("/{League_id}")
    def update_League(
        League_id: int,
        request: LeagueUpdateRequest
    ):
        """
        경기 일정을 수정한다.
        """

        try:
            result = League_service.update_League(
                League_id=League_id,
                game_date=request.game_date,
                game_time=request.game_time,
                game_name=request.game_name,
                stadium_name=request.stadium_name,
                stadium_address=request.stadium_address
            )

            if result is None:
                raise HTTPException(
                    status_code=404,
                    detail="경기 일정을 찾을 수 없습니다."
                )

            return {
                "message": "경기 일정이 수정되었습니다.",
                "data": result
            }

        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

    # ==================================================
    # DELETE
    # ==================================================

    @router.delete("/{League_id}")
    def delete_League(League_id: int):
        """
        특정 경기 일정을 삭제한다.
        """

        result = League_service.delete_League(League_id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="경기 일정을 찾을 수 없습니다."
            )

        return {
            "message": "경기 일정이 삭제되었습니다.",
            "data": result
        }

    return router