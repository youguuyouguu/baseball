from datetime import datetime
from typing import Any, Dict, List, Optional

from repository.Tour_repository import TourRepository


class TourService:
    """Tour 생성 및 수정 규칙을 처리하는 Service 클래스."""

    def __init__(self, tour_repository: TourRepository):
        self.tour_repository = tour_repository

    def create_tour(
        self,
        schedule_id: int,
        user_id: int,
        game_id: int,
        start_time: datetime,
        end_time: datetime,
        people_num: int,
    ) -> Dict[str, Any]:
        self._validate_times(start_time, end_time)
        self._validate_people(people_num)
        return self.tour_repository.create_tour(
            schedule_id=schedule_id,
            user_id=user_id,
            game_id=game_id,
            start_time=start_time,
            end_time=end_time,
            people_num=people_num,
        )

    def get_tour(self, schedule_id: int) -> Optional[Dict[str, Any]]:
        return self.tour_repository.get_tour(schedule_id)

    def get_tours(self) -> List[Dict[str, Any]]:
        return self.tour_repository.get_tours()

    def update_tour(
        self,
        schedule_id: int,
        user_id: Optional[int] = None,
        game_id: Optional[int] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        people_num: Optional[int] = None,
    ) -> Optional[Dict[str, Any]]:
        if start_time is not None and end_time is not None:
            self._validate_times(start_time, end_time)
        if people_num is not None:
            self._validate_people(people_num)
        return self.tour_repository.update_tour(
            schedule_id=schedule_id,
            user_id=user_id,
            game_id=game_id,
            start_time=start_time,
            end_time=end_time,
            people_num=people_num,
        )

    def delete_tour(self, schedule_id: int) -> Optional[Dict[str, Any]]:
        return self.tour_repository.delete_tour(schedule_id)

    @staticmethod
    def _validate_times(start_time: datetime, end_time: datetime) -> None:
        if start_time >= end_time:
            raise ValueError("일정 시작시간은 종료시간보다 빨라야 합니다.")

    @staticmethod
    def _validate_people(people_num: int) -> None:
        if people_num <= 0:
            raise ValueError("참여 인원은 1명 이상이어야 합니다.")