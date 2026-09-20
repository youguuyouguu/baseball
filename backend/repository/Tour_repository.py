from datetime import time
from typing import Any, Dict, List, Optional

from supabase import Client


class TourRepository:
    TABLE_NAME = "Tour"

    def __init__(self, supabase: Client):
        self.supabase = supabase

    def create_tour(
        self,
        schedule_id: Optional[int],
        User_id: int,
        League_id: int,
        starting_time: time,
        end_time: time,
        people_num: int,
    ) -> Dict[str, Any]:
        data = {
            "User_id": User_id,
            "League_id": League_id,
            "starting_time": starting_time.isoformat(),
            "end_time": end_time.isoformat(),
            "people_num": people_num,
        }
        if schedule_id is not None:
            data["schedule_id"] = schedule_id

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

        return response.data if response.data else None

    def get_tours(self) -> List[Dict[str, Any]]:
        response = self.supabase.table(self.TABLE_NAME).select("*").execute()
        return response.data

    def get_tours_by_user(self, User_id: int) -> List[Dict[str, Any]]:
        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .select("*")
            .eq("User_id", User_id)
            .execute()
        )
        return response.data

    def get_tours_by_user(self, User_id: int) -> List[Dict[str, Any]]:
        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .select("*")
            .eq("User_id", User_id)
            .execute()
        )
        return response.data

    def update_tour(
        self,
        schedule_id: int,
        User_id: Optional[int] = None,
        League_id: Optional[int] = None,
        starting_time: Optional[time] = None,
        end_time: Optional[time] = None,
        people_num: Optional[int] = None,
    ) -> Optional[Dict[str, Any]]:
        update_data: Dict[str, Any] = {}

        if User_id is not None:
            update_data["User_id"] = User_id
        if League_id is not None:
            update_data["League_id"] = League_id
        if starting_time is not None:
            update_data["starting_time"] = starting_time.isoformat()
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

        return response.data if response.data else None

    def delete_tour(self, schedule_id: int) -> Optional[Dict[str, Any]]:
        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .delete()
            .eq("schedule_id", schedule_id)
            .execute()
        )

        return response.data[0] if response.data else None