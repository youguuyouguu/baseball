import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client

from api.kbo_api import create_kbo_router
from api.schedule_api import create_schedule_router
from api.tour_api import create_tour_router
from api.user_api import create_user_router
from repository.User_repository import UserRepository
from repository.Tour_repository import TourRepository
from service.KBO_service import KBOService
from service.Schedule_service import ScheduleService
from service.Tour_service import TourService
from service.User_service import UserService


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
user_service = UserService(user_repository)
tour_service = TourService(tour_repository)
kbo_service = KBOService()
schedule_service = ScheduleService()

app.include_router(create_user_router(supabase))
app.include_router(create_kbo_router(kbo_service))
app.include_router(create_schedule_router(schedule_service))
app.include_router(create_tour_router(tour_service))
