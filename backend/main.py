import os
import threading
from datetime import date, timedelta

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client

from api.kbo_api import create_kbo_router
from api.schedule_api import create_schedule_router
from api.tour_api import create_tour_router
from api.user_api import create_user_router
from api.Detail_api import create_detail_router
from api.Place_api import create_place_router
from api.League_api import create_League_router
from repository.User_repository import UserRepository
from repository.Tour_repository import TourRepository
from repository.Detail_repository import DetailRepository
from repository.Place_repository import PlaceRepository
from repository.League_repository import LeagueRepository
from service.KBO_service import KBOService
from service.Schedule_service import ScheduleService
from service.Tour_service import TourService
from service.User_service import UserService
from service.Detail_service import DetailService
from service.Place_service import PlaceService
from service.League_service import LeagueService


app = FastAPI()
load_dotenv()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5174", "http://127.0.0.1:5174"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

supabase = create_client(
	os.environ["SUPABASE_URL"],
	os.environ["SUPABASE_KEY"],
)

user_repository = UserRepository(supabase)
tour_repository = TourRepository(supabase)
detail_repository = DetailRepository(supabase)
place_repository = PlaceRepository(supabase)
league_repository = LeagueRepository(supabase)
user_service = UserService(user_repository)
tour_service = TourService(tour_repository)
detail_service = DetailService(detail_repository)
place_service = PlaceService(place_repository)
league_service = LeagueService(league_repository)
kbo_service = KBOService()
schedule_service = ScheduleService()

app.include_router(create_user_router(supabase))
app.include_router(create_kbo_router(kbo_service))
app.include_router(create_schedule_router(schedule_service))
app.include_router(create_tour_router(tour_service))
app.include_router(create_detail_router(detail_service))
app.include_router(create_place_router(place_service))
app.include_router(create_League_router(league_service))


def sync_league_schedule() -> None:
	today = date.today()
	end_date = date(today.year, 10, 31)
	if today > end_date:
		return
	try:
		league_service.sync_regular_season(today, end_date)
	except Exception as error:
		print(f"League 일정 동기화 실패: {error}")


def weekly_league_sync() -> None:
	while True:
		sync_league_schedule()
		threading.Event().wait(timedelta(days=7).total_seconds())


@app.on_event("startup")
def start_league_sync() -> None:
	threading.Thread(target=weekly_league_sync, daemon=True).start()
