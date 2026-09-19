from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from supabase import Client


class DetailRepository:
    TABLE_NAME = "schedule_detail"

    def __init__(self, supabase: Client):
        self.supabase = supabase

    def create_detail(self, detail_id: UUID, schedule_id: UUID, place_id: Optional[UUID], custom_name: Optional[str], start_at: datetime, end_at: datetime, state: str) -> Dict[str, Any]:
        data = {
            "detail_id": str(detail_id),
            "schedule_id": str(schedule_id),
            "place_id": str(place_id) if place_id else None,
            "custom_name": custom_name,
            "start_at": start_at.isoformat(),
            "end_at": end_at.isoformat(),
            "state": state,
        }
        response = self.supabase.table(self.TABLE_NAME).insert(data).execute()
        return response.data[0]

    def get_detail(self, detail_id: UUID) -> Optional[Dict[str, Any]]:
        response = self.supabase.table(self.TABLE_NAME).select("*").eq("detail_id", str(detail_id)).execute()
        return response.data[0] if response.data else None

    def get_details(self) -> List[Dict[str, Any]]:
        response = self.supabase.table(self.TABLE_NAME).select("*").execute()
        return response.data

    def get_details_by_schedule(self, schedule_id: UUID) -> List[Dict[str, Any]]:
        response = self.supabase.table(self.TABLE_NAME).select("*").eq("schedule_id", str(schedule_id)).execute()
        return response.data

    def update_detail(self, detail_id: UUID, schedule_id: Optional[UUID] = None, place_id: Optional[UUID] = None, custom_name: Optional[str] = None, start_at: Optional[datetime] = None, end_at: Optional[datetime] = None, state: Optional[str] = None) -> Optional[Dict[str, Any]]:
        update_data: Dict[str, Any] = {}
        if schedule_id is not None:
            update_data["schedule_id"] = str(schedule_id)
        if place_id is not None:
            update_data["place_id"] = str(place_id)
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

        response = self.supabase.table(self.TABLE_NAME).update(update_data).eq("detail_id", str(detail_id)).execute()
        return response.data[0] if response.data else None

    def delete_detail(self, detail_id: UUID) -> Optional[Dict[str, Any]]:
        response = self.supabase.table(self.TABLE_NAME).delete().eq("detail_id", str(detail_id)).execute()
        return response.data[0] if response.data else None