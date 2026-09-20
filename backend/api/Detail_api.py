from datetime import time
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from service.Detail_service import DetailService


class DetailCreate(BaseModel):
    detail_id: Optional[int] = None
    schedule_id: int
    place_id: Optional[int] = None
    custom_name: Optional[str] = None
    start_at: time
    end_at: time
    state: str


class DetailUpdate(BaseModel):
    schedule_id: Optional[int] = None
    place_id: Optional[int] = None
    custom_name: Optional[str] = None
    start_at: Optional[time] = None
    end_at: Optional[time] = None
    state: Optional[str] = None


def create_detail_router(detail_service: DetailService):
    router = APIRouter(prefix="/schedule-details", tags=["ScheduleDetail"])

    def request_data(model: BaseModel, **kwargs):
        if hasattr(model, "model_dump"):
            return model.model_dump(**kwargs)
        return model.dict(**kwargs)

    @router.post("/")
    def create_detail(detail: DetailCreate):
        try:
            result = detail_service.create_detail(**request_data(detail))
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error
        if result is None:
            raise HTTPException(status_code=500, detail="ScheduleDetail 생성에 실패했습니다.")
        return result

    @router.get("/{detail_id}")
    def get_detail(detail_id: int):
        result = detail_service.get_detail(detail_id)
        if result is None:
            raise HTTPException(status_code=404, detail="ScheduleDetail을 찾을 수 없습니다.")
        return result

    @router.get("/")
    def get_details(schedule_id: Optional[int] = None):
        if schedule_id is not None:
            return detail_service.get_details_by_schedule(schedule_id)
        return detail_service.get_details()

    @router.put("/{detail_id}")
    def update_detail(detail_id: int, detail: DetailUpdate):
        try:
            result = detail_service.update_detail(detail_id=detail_id, **request_data(detail, exclude_unset=True))
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error
        if result is None:
            raise HTTPException(status_code=404, detail="수정할 ScheduleDetail을 찾을 수 없습니다.")
        return result

    @router.delete("/{detail_id}")
    def delete_detail(detail_id: int):
        result = detail_service.delete_detail(detail_id)
        if result is None:
            raise HTTPException(status_code=404, detail="삭제할 ScheduleDetail을 찾을 수 없습니다.")
        return {"message": "ScheduleDetail이 삭제되었습니다.", "detail_id": detail_id}

    return router