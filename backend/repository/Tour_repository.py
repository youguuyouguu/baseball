from datetime import datetime
from typing import Any, Dict, List, Optional

from supabase import Client


class TourRepository:
    TABLE_NAME = "Tour"

    def __init__(self, supabase: Client):
        self.supabase = supabase

    def create_tour(
        self,
        schedule_id: int,
        user_id: int,
        game_id: int,
        start_time: datetime,
        end_time: datetime,
        people_num: int,
    ) -> Dict[str, Any]:
        data = {
            "schedule_id": schedule_id,
            "user_id": user_id,
            "game_id": game_id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "people_num": people_num,
        }

        response = self.supabase.table(self.TABLE_NAME).insert(data).execute()
        return response.data[0]

    def get_tour(self, schedule_id: int) -> Optional[Dict[str, Any]]:
        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .select("*")
            .eq("schedule_id", schedule_id)
            .execute()
        )

        return response.data[0] if response.data else None

    def get_tours(self) -> List[Dict[str, Any]]:
        response = self.supabase.table(self.TABLE_NAME).select("*").execute()
        return response.data

    def update_tour(
        self,
        schedule_id: int,
        user_id: Optional[int] = None,
        game_id: Optional[int] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        people_num: Optional[int] = None,
    ) -> Optional[Dict[str, Any]]:
        update_data: Dict[str, Any] = {}

        if user_id is not None:
            update_data["user_id"] = user_id
        if game_id is not None:
            update_data["game_id"] = game_id
        if start_time is not None:
            update_data["start_time"] = start_time.isoformat()
        if end_time is not None:
            update_data["end_time"] = end_time.isoformat()
        if people_num is not None:
            update_data["people_num"] = people_num

        if not update_data:
            return None

        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .update(update_data)
            .eq("schedule_id", schedule_id)
            .execute()
        )

        return response.data[0] if response.data else None

    def delete_tour(self, schedule_id: int) -> Optional[Dict[str, Any]]:
        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .delete()
            .eq("schedule_id", schedule_id)
            .execute()
        )

        return response.data[0] if response.data else None