# main.py

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from supabase import Client, create_client

# ==================================================
# Repository
# ==================================================

from repository.User_repository import UserRepository
from repository.League_repository import LeagueRepository

# ==================================================
# Service
# ==================================================

from service.User_service import UserService
from service.League_service import LeagueService

# ==================================================
# API
# ==================================================

from api.User_api import create_user_router
from api.League_api import create_League_router


# ==================================================
# 환경 변수 설정
# ==================================================

load_dotenv()


# ==================================================
# Supabase 설정
# ==================================================

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "SUPABASE_URL 또는 SUPABASE_KEY가 설정되어 있지 않습니다."
    )


# ==================================================
# Supabase Client 생성
# ==================================================

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# ==================================================
# User Repository 생성
# ==================================================

user_repository = UserRepository(supabase)


# ==================================================
# User Service 생성
# ==================================================

user_service = UserService(user_repository)


# ==================================================
# League Repository 생성
# ==================================================

League_repository = LeagueRepository(supabase)


# ==================================================
# League Service 생성
# ==================================================

League_service = LeagueService(League_repository)


# ==================================================
# FastAPI 애플리케이션 생성
# ==================================================

app = FastAPI(
    title="Baseball Travel API",
    description="야구 원정 팬을 위한 여행 일정 설계 서비스 API",
    version="1.0.0"
)


# ==================================================
# User API Router 생성
# ==================================================

user_router = create_user_router(user_service)


# ==================================================
# League API Router 생성
# ==================================================

League_router = create_League_router(League_service)


# ==================================================
# Router 등록
# ==================================================

app.include_router(user_router)
app.include_router(League_router)


# ==================================================
# 서버 상태 확인
# ==================================================

@app.get("/")
def root():
    return {
        "message": "Baseball Travel API 서버가 정상적으로 실행 중입니다."
    }