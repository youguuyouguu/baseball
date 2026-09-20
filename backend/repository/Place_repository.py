from typing import Any, Dict, List, Optional

from supabase import Client


class PlaceRepository:
    TABLE_NAME = "Tour_Place"

    def __init__(self, supabase: Client):
        self.supabase = supabase

    def create_place(
        self,
        content_id: str,
        place_type: str,
        name: str,
        address: str,
        lat: float,
        lng: float,
        place_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        data = {
            "content_id": content_id,
            "place_type": place_type,
            "name": name,
            "address": address,
            "lat": lat,
            "lng": lng,
        }
        if place_id is not None:
            data["place_id"] = place_id
        response = self.supabase.table(self.TABLE_NAME).insert(data).execute()
        return response.data[0]

    def get_place(self, place_id: int) -> Optional[Dict[str, Any]]:
        response = self.supabase.table(self.TABLE_NAME).select("*").eq("place_id", place_id).execute()
        return response.data[0] if response.data else None

    def get_places(self) -> List[Dict[str, Any]]:
        response = self.supabase.table(self.TABLE_NAME).select("*").execute()
        return response.data

    def update_place(
        self,
        place_id: int,
        content_id: Optional[str] = None,
        place_type: Optional[str] = None,
        name: Optional[str] = None,
        address: Optional[str] = None,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
    ) -> Optional[Dict[str, Any]]:
        update_data: Dict[str, Any] = {}
        if content_id is not None:
            update_data["content_id"] = content_id
        if place_type is not None:
            update_data["place_type"] = place_type
        if name is not None:
            update_data["name"] = name
        if address is not None:
            update_data["address"] = address
        if lat is not None:
            update_data["lat"] = lat
        if lng is not None:
            update_data["lng"] = lng
        if not update_data:
            return None

        response = self.supabase.table(self.TABLE_NAME).update(update_data).eq("place_id", place_id).execute()
        return response.data[0] if response.data else None

    def delete_place(self, place_id: int) -> Optional[Dict[str, Any]]:
        response = self.supabase.table(self.TABLE_NAME).delete().eq("place_id", place_id).execute()
        return response.data[0] if response.data else None