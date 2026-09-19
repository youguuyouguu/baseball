from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from service.Tour_service import TourService


class TourCreate(BaseModel):
    schedule_id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    game_id: UUID
    start_time: datetime
    end_time: datetime
    people_num: int = Field(gt=0)


class TourUpdate(BaseModel):
    user_id: Optional[UUID] = None
    game_id: Optional[UUID] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
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
    def get_tour(schedule_id: UUID):
        result = tour_service.get_tour(schedule_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Tour를 찾을 수 없습니다.")
        return result

    @router.get("/")
    def get_tours():
        return tour_service.get_tours()

    @router.put("/{schedule_id}")
    def update_tour(schedule_id: UUID, tour: TourUpdate):
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
    def delete_tour(schedule_id: UUID):
        result = tour_service.delete_tour(schedule_id)
        if result is None:
            raise HTTPException(status_code=404, detail="삭제할 Tour를 찾을 수 없습니다.")
        return {"message": "Tour가 삭제되었습니다.", "schedule_id": schedule_id}

    return router