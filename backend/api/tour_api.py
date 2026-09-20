from datetime import time
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from service.Tour_service import TourService


class TourCreate(BaseModel):
    schedule_id: Optional[int] = None
    User_id: int
    League_id: int
    starting_time: time
    end_time: time
    people_num: int = Field(gt=0)


class TourUpdate(BaseModel):
    User_id: Optional[int] = None
    League_id: Optional[int] = None
    starting_time: Optional[time] = None
    end_time: Optional[time] = None
    people_num: Optional[int] = Field(default=None, gt=0)


def create_tour_router(tour_service: TourService):
    router = APIRouter(prefix="/tours", tags=["Tour"])

    def request_data(model: BaseModel, **kwargs):
        if hasattr(model, "model_dump"):
            return model.model_dump(**kwargs)
        return model.dict(**kwargs)

    @router.post("/")
    def create_tour(tour: TourCreate):
        try:
            result = tour_service.create_tour(**request_data(tour))
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error

        if result is None:
            raise HTTPException(status_code=500, detail="Tour 생성에 실패했습니다.")
        return result

    @router.get("/{schedule_id}")
    def get_tour(schedule_id: int):
        result = tour_service.get_tour(schedule_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Tour를 찾을 수 없습니다.")
        return result

    @router.get("/")
    def get_tours():
        return tour_service.get_tours()

    @router.put("/{schedule_id}")
    def update_tour(schedule_id: int, tour: TourUpdate):
        try:
            result = tour_service.update_tour(
                schedule_id=schedule_id,
                **request_data(tour, exclude_unset=True),
            )
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error

        if result is None:
            raise HTTPException(status_code=404, detail="수정할 Tour를 찾을 수 없습니다.")
        return result

    @router.delete("/{schedule_id}")
    def delete_tour(schedule_id: int):
        result = tour_service.delete_tour(schedule_id)
        if result is None:
            raise HTTPException(status_code=404, detail="삭제할 Tour를 찾을 수 없습니다.")
        return {"message": "Tour가 삭제되었습니다.", "schedule_id": schedule_id}

    return router