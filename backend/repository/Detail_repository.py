from datetime import time
from typing import Any, Dict, List, Optional

from supabase import Client


class DetailRepository:
    TABLE_NAME = "Schdule_detail"

    def __init__(self, supabase: Client):
        self.supabase = supabase

    def create_detail(self, detail_id: Optional[int], schedule_id: int, place_id: Optional[int], custom_name: Optional[str], start_at: time, end_at: time, state: str) -> Dict[str, Any]:
        data = {
            "schedule_id": schedule_id,
            "place_id": place_id,
            "custom_name": custom_name,
            "start_at": start_at.isoformat(),
            "end_at": end_at.isoformat(),
            "state": state,
        }
        if detail_id is not None:
            data["detail_id"] = detail_id
        response = self.supabase.table(self.TABLE_NAME).insert(data).execute()
        return response.data[0]

    def get_detail(self, detail_id: int) -> Optional[Dict[str, Any]]:
        response = self.supabase.table(self.TABLE_NAME).select("*").eq("detail_id", detail_id).execute()
        return response.data[0] if response.data else None

    def get_details(self) -> List[Dict[str, Any]]:
        response = self.supabase.table(self.TABLE_NAME).select("*").execute()
        return response.data

    def get_details_by_schedule(self, schedule_id: int) -> List[Dict[str, Any]]:
        response = self.supabase.table(self.TABLE_NAME).select("*").eq("schedule_id", schedule_id).execute()
        return response.data

    def update_detail(self, detail_id: int, schedule_id: Optional[int] = None, place_id: Optional[int] = None, custom_name: Optional[str] = None, start_at: Optional[time] = None, end_at: Optional[time] = None, state: Optional[str] = None) -> Optional[Dict[str, Any]]:
        update_data: Dict[str, Any] = {}
        if schedule_id is not None:
            update_data["schedule_id"] = schedule_id
        if place_id is not None:
            update_data["place_id"] = place_id
        if custom_name is not None:
            update_data["custom_name"] = custom_name
        if start_at is not None:
            update_data["start_at"] = start_at.isoformat()
        if end_at is not None:
            update_data["end_at"] = end_at.isoformat()
        if state is not None:
            update_data["state"] = state
        if not update_data:
            return None

        response = self.supabase.table(self.TABLE_NAME).update(update_data).eq("detail_id", detail_id).execute()
        return response.data[0] if response.data else None

    def delete_detail(self, detail_id: int) -> Optional[Dict[str, Any]]:
        response = self.supabase.table(self.TABLE_NAME).delete().eq("detail_id", detail_id).execute()
        return response.data[0] if response.data else None