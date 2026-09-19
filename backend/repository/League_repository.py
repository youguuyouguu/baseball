# repository/League_repository.py

from typing import Optional, List, Dict, Any
from uuid import UUID

from supabase import Client


class LeagueRepository:
    """
    League 테이블과 직접 상호작용하는 Repository 클래스.

    역할:
    - 경기 일정 생성(Create)
    - 경기 일정 조회(Read)
    - 경기 일정 수정(Update)
    - 경기 일정 삭제(Delete)

    DB와의 상호작용만 담당한다.
    """

    # Supabase의 실제 테이블 이름
    TABLE_NAME = "League"

    def __init__(self, supabase: Client):
        self.supabase = supabase

    # ==================================================
    # CREATE
    # ==================================================

    def create_League(
        self,
        League_id: UUID,
        game_date: str,
        game_time: str,
        game_name: str,
        stadium_name: str,
        stadium_address: str,
        external_game_id: Optional[str] = None,
    ) -> Dict[str, Any]:

        # Supabase에 저장할 데이터
        data = {
            "League_id": str(League_id),
            "game_date": game_date,
            "game_time": game_time,
            "game_name": game_name,
            "stadium_name": stadium_name,
            "stadium_address": stadium_address
        }

        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .insert(data)
            .execute()
        )

        return response.data[0]

    # ==================================================
    # READ
    # ==================================================

    def get_League(
        self,
        League_id: UUID
    ) -> Optional[Dict[str, Any]]:

        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .select("*")
            .eq("League_id", str(League_id))
            .execute()
        )

        if not response.data:
            return None

        return response.data[0]

    # ==================================================
    # READ ALL
    # ==================================================

    def get_Leagues(self) -> List[Dict[str, Any]]:

        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .select("*")
            .execute()
        )

        return response.data

    def upsert_Leagues(self, leagues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not leagues:
            return []

        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .upsert(leagues, on_conflict="League_id")
            .execute()
        )

        return response.data

    # ==================================================
    # UPDATE
    # ==================================================

    def update_League(
        self,
        League_id: UUID,
        game_date: Optional[str] = None,
        game_time: Optional[str] = None,
        game_name: Optional[str] = None,
        stadium_name: Optional[str] = None,
        stadium_address: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:

        update_data = {}

        if game_date is not None:
            update_data["game_date"] = game_date

        if game_time is not None:
            update_data["game_time"] = game_time

        if game_name is not None:
            update_data["game_name"] = game_name

        if stadium_name is not None:
            update_data["stadium_name"] = stadium_name

        if stadium_address is not None:
            update_data["stadium_address"] = stadium_address

        # 수정할 값이 없으면 종료
        if not update_data:
            return None

        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .update(update_data)
            .eq("League_id", str(League_id))
            .execute()
        )

        if not response.data:
            return None

        return response.data[0]

    # ==================================================
    # DELETE
    # ==================================================

    def delete_League(
        self,
        League_id: UUID
    ) -> Optional[Dict[str, Any]]:

        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .delete()
            .eq("League_id", str(League_id))
            .execute()
        )

        if not response.data:
            return None

        return response.data[0]