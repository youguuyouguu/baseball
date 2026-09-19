from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from service.Place_service import PlaceService


class PlaceCreate(BaseModel):
    place_id: int
    content_id: int
    place_type: str
    name: str
    address: str
    lat: float
    lng: float


class PlaceUpdate(BaseModel):
    content_id: Optional[int] = None
    place_type: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


def create_place_router(place_service: PlaceService):
    router = APIRouter(prefix="/places", tags=["Place"])

    def request_data(model: BaseModel, **kwargs):
        if hasattr(model, "model_dump"):
            return model.model_dump(**kwargs)
        return model.dict(**kwargs)

    @router.post("/")
    def create_place(place: PlaceCreate):
        try:
            result = place_service.create_place(**request_data(place))
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error
        if result is None:
            raise HTTPException(status_code=500, detail="Place 생성에 실패했습니다.")
        return result

    @router.get("/{place_id}")
    def get_place(place_id: int):
        result = place_service.get_place(place_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Place를 찾을 수 없습니다.")
        return result

    @router.get("/")
    def get_places():
        return place_service.get_places()

    @router.put("/{place_id}")
    def update_place(place_id: int, place: PlaceUpdate):
        try:
            result = place_service.update_place(
                place_id=place_id,
                **request_data(place, exclude_unset=True),
            )
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error
        if result is None:
            raise HTTPException(status_code=404, detail="수정할 Place를 찾을 수 없습니다.")
        return result

    @router.delete("/{place_id}")
    def delete_place(place_id: int):
        result = place_service.delete_place(place_id)
        if result is None:
            raise HTTPException(status_code=404, detail="삭제할 Place를 찾을 수 없습니다.")
        return {"message": "Place가 삭제되었습니다.", "place_id": place_id}

    return router