from datetime import datetime
from typing import Any, Dict, List, Optional

from repository.Detail_repository import DetailRepository


class DetailService:
    ALLOWED_STATES = {"대기", "진행", "종료"}

    def __init__(self, detail_repository: DetailRepository):
        self.detail_repository = detail_repository

    def create_detail(self, detail_id: int, schedule_id: int, place_id: Optional[int], custom_name: Optional[str], start_at: datetime, end_at: datetime, state: str) -> Dict[str, Any]:
        self._validate_times(start_at, end_at)
        self._validate_state(state)
        self._validate_place(place_id, custom_name)
        if self.detail_repository.get_detail(detail_id) is not None:
            raise ValueError("이미 존재하는 detail_id입니다.")
        return self.detail_repository.create_detail(detail_id, schedule_id, place_id, custom_name, start_at, end_at, state)

    def get_detail(self, detail_id: int) -> Optional[Dict[str, Any]]:
        return self.detail_repository.get_detail(detail_id)

    def get_details(self) -> List[Dict[str, Any]]:
        return self.detail_repository.get_details()

    def get_details_by_schedule(self, schedule_id: int) -> List[Dict[str, Any]]:
        return self.detail_repository.get_details_by_schedule(schedule_id)

    def update_detail(self, detail_id: int, schedule_id: Optional[int] = None, place_id: Optional[int] = None, custom_name: Optional[str] = None, start_at: Optional[datetime] = None, end_at: Optional[datetime] = None, state: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if start_at is not None and end_at is not None:
            self._validate_times(start_at, end_at)
        if state is not None:
            self._validate_state(state)
        if place_id is not None or custom_name is not None:
            self._validate_place(place_id, custom_name)
        return self.detail_repository.update_detail(detail_id, schedule_id, place_id, custom_name, start_at, end_at, state)

    def delete_detail(self, detail_id: int) -> Optional[Dict[str, Any]]:
        return self.detail_repository.delete_detail(detail_id)

    @staticmethod
    def _validate_times(start_at: datetime, end_at: datetime) -> None:
        if start_at >= end_at:
            raise ValueError("방문 시작시간은 종료시간보다 빨라야 합니다.")

    @classmethod
    def _validate_state(cls, state: str) -> None:
        if state not in cls.ALLOWED_STATES:
            raise ValueError("상태는 대기, 진행, 종료 중 하나여야 합니다.")

    @staticmethod
    def _validate_place(place_id: Optional[int], custom_name: Optional[str]) -> None:
        if place_id is not None and custom_name is not None:
            raise ValueError("place_id와 custom_name을 동시에 입력할 수 없습니다.")