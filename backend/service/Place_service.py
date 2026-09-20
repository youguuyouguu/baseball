from typing import Any, Dict, List, Optional

from repository.Place_repository import PlaceRepository


class PlaceService:
    def __init__(self, place_repository: PlaceRepository):
        self.place_repository = place_repository

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
        self._validate_place_data(place_type, name, address, lat, lng)
        if self.place_repository.get_place(place_id) is not None:
            raise ValueError("이미 존재하는 place_id입니다.")
        return self.place_repository.create_place(
            place_id=place_id,
            content_id=content_id,
            place_type=place_type,
            name=name,
            address=address,
            lat=lat,
            lng=lng,
        )

    def get_place(self, place_id: int) -> Optional[Dict[str, Any]]:
        return self.place_repository.get_place(place_id)

    def get_places(self) -> List[Dict[str, Any]]:
        return self.place_repository.get_places()

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
        if place_type is not None and not place_type.strip():
            raise ValueError("장소 타입은 필수입니다.")
        if name is not None and not name.strip():
            raise ValueError("장소 이름은 필수입니다.")
        if address is not None and not address.strip():
            raise ValueError("장소 주소는 필수입니다.")
        self._validate_coordinates(lat, lng)
        return self.place_repository.update_place(
            place_id=place_id,
            content_id=content_id,
            place_type=place_type,
            name=name,
            address=address,
            lat=lat,
            lng=lng,
        )

    def delete_place(self, place_id: int) -> Optional[Dict[str, Any]]:
        return self.place_repository.delete_place(place_id)

    @staticmethod
    def _validate_place_data(place_type: str, name: str, address: str, lat: float, lng: float) -> None:
        if not place_type.strip():
            raise ValueError("장소 타입은 필수입니다.")
        if not name.strip():
            raise ValueError("장소 이름은 필수입니다.")
        if not address.strip():
            raise ValueError("장소 주소는 필수입니다.")
        PlaceService._validate_coordinates(lat, lng)

    @staticmethod
    def _validate_coordinates(lat: Optional[float], lng: Optional[float]) -> None:
        if lat is not None and not -90 <= lat <= 90:
            raise ValueError("위도는 -90에서 90 사이여야 합니다.")
        if lng is not None and not -180 <= lng <= 180:
            raise ValueError("경도는 -180에서 180 사이여야 합니다.")