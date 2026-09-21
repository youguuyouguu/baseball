from datetime import datetime, time
from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from service.Schedule_service import ScheduleService
from service.congestion_service import build_congestion_cache


class Location(BaseModel):
    id: str
    name: str
    address: Optional[str] = None


class GameAnchor(BaseModel):
    stadium: Location
    start_time: datetime


class StartPoint(BaseModel):
    location: Location
    arrival_time: datetime


class ReturnTransport(BaseModel):
    location: Location
    departure_time: datetime


class EndPoint(BaseModel):
    accommodation: Optional[Location] = None
    accommodation_deadline: Optional[datetime] = None
    return_transport: Optional[ReturnTransport] = None


class Place(BaseModel):
    id: str
    name: str
    location: Location
    address: Optional[str] = None
    category: Optional[str] = None
    visit_minutes: int = Field(gt=0)
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None


class ScheduleRequest(BaseModel):
    participant_count: int = Field(gt=0)
    game: GameAnchor
    start_point: StartPoint
    end_point: EndPoint
    places: list[Place] = Field(default_factory=list)
    travel_times: dict[str, dict[str, int]]
    congestion_cache: dict[str, Optional[dict[str, Any]]] = Field(default_factory=dict)



def create_schedule_router(schedule_service: ScheduleService):
    router = APIRouter(prefix="/schedules", tags=["Schedule"])

    @router.post("/generate")
    def generate_schedule(request: ScheduleRequest):
        try:
            payload = request.model_dump() if hasattr(request, "model_dump") else request.dict()

            target_date = datetime.fromisoformat(
                str(payload["game"]["start_time"])
            ).date()

            try:
                payload["congestion_cache"] = build_congestion_cache(
                    places=payload["places"],
                    target_date=target_date,
                )
            except Exception:
                payload["congestion_cache"] = {}

            return schedule_service.build_schedule(payload)

        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    return router

