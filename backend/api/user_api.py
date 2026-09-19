from typing import Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from supabase import Client

from repository.User_repository import UserRepository


# ============================================================
# 요청 데이터 형식
# ============================================================

class UserCreate(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    email: str
    nickname: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    nickname: Optional[str] = None


# ============================================================
# Router 생성
# ============================================================

def create_user_router(supabase: Client):

    # User 관련 API를 묶는 Router
    router = APIRouter(
        prefix="/users",
        tags=["User"]
    )

    user_repository = UserRepository(supabase)


    # ========================================================
    # CREATE
    # ========================================================

    @router.post("/")
    def create_user(user: UserCreate):

        result = user_repository.create_user(
            user_id=user.user_id,
            email=user.email,
            nickname=user.nickname
        )

        if result is None:
            raise HTTPException(
                status_code=500,
                detail="User 생성에 실패했습니다."
            )

        return result


    # ========================================================
    # READ - 특정 사용자
    # ========================================================

    @router.get("/{user_id}")
    def get_user(user_id: UUID):

        result = user_repository.get_user(user_id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="User를 찾을 수 없습니다."
            )

        return result


    # ========================================================
    # READ - 이메일
    # ========================================================

    @router.get("/email/{email}")
    def get_user_by_email(email: str):

        result = user_repository.get_user_by_email(email)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="User를 찾을 수 없습니다."
            )

        return result


    # ========================================================
    # READ - 전체 사용자
    # ========================================================

    @router.get("/")
    def get_all_users():

        return user_repository.get_users()


    # ========================================================
    # UPDATE
    # ========================================================

    @router.put("/{user_id}")
    def update_user(
        user_id: UUID,
        user: UserUpdate
    ):

        result = user_repository.update_user(
            user_id=user_id,
            email=user.email,
            nickname=user.nickname
        )

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="수정할 User를 찾을 수 없습니다."
            )

        return result


    # ========================================================
    # DELETE
    # ========================================================

    @router.delete("/{user_id}")
    def delete_user(user_id: UUID):

        result = user_repository.delete_user(user_id)

        if not result:
            raise HTTPException(
                status_code=404,
                detail="삭제할 User를 찾을 수 없습니다."
            )

        return {
            "message": "User가 삭제되었습니다.",
            "user_id": user_id
        }


    return router
