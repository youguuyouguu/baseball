from datetime import time
from typing import Any, Dict, List, Optional

from repository.Tour_repository import TourRepository


class TourService:
    """Tour 생성 및 수정 규칙을 처리하는 Service 클래스."""

    def __init__(self, tour_repository: TourRepository):
        self.tour_repository = tour_repository

    def create_tour(
        self,
        schedule_id: Optional[int],
        User_id: int,
        League_id: int,
        starting_time: time,
        end_time: time,
        people_num: int,
    ) -> Dict[str, Any]:
        self._validate_times(starting_time, end_time)
        self._validate_people(people_num)
        return self.tour_repository.create_tour(
            schedule_id=schedule_id,
            User_id=User_id,
            League_id=League_id,
            starting_time=starting_time,
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
        User_id: Optional[int] = None,
        League_id: Optional[int] = None,
        starting_time: Optional[time] = None,
        end_time: Optional[time] = None,
        people_num: Optional[int] = None,
    ) -> Optional[Dict[str, Any]]:
        if starting_time is not None and end_time is not None:
            self._validate_times(starting_time, end_time)
        if people_num is not None:
            self._validate_people(people_num)
        return self.tour_repository.update_tour(
            schedule_id=schedule_id,
            User_id=User_id,
            League_id=League_id,
            starting_time=starting_time,
            end_time=end_time,
            people_num=people_num,
        )

    def delete_tour(self, schedule_id: int) -> Optional[Dict[str, Any]]:
        return self.tour_repository.delete_tour(schedule_id)

    @staticmethod
    def _validate_times(start_time: time, end_time: time) -> None:
        if start_time >= end_time:
            raise ValueError("일정 시작시간은 종료시간보다 빨라야 합니다.")

    @staticmethod
    def _validate_people(people_num: int) -> None:
        if people_num <= 0:
            raise ValueError("참여 인원은 1명 이상이어야 합니다.")