# api/User_api.py

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from service.User_service import UserService


# ==================================================
# 요청 데이터 모델
# ==================================================

class UserCreateRequest(BaseModel):
    """
    사용자 생성 요청 데이터

    클라이언트에서 다음과 같은 JSON을 보내면 된다.

    {
        "user_id": 1,
        "email": "test@test.com",
        "nickname": "테스트"
    }
    """

    user_id: int
    email: str
    nickname: str


class UserUpdateRequest(BaseModel):
    """
    사용자 정보 수정 요청 데이터

    수정하지 않는 값은 생략할 수 있다.
    """

    email: Optional[str] = None
    nickname: Optional[str] = None


# ==================================================
# User Router 생성 함수
# ==================================================

def create_user_router(user_service: UserService) -> APIRouter:
    """
    UserService를 전달받아 User API Router를 생성한다.

    main.py에서 생성한 UserService를 전달받기 때문에
    API 계층에서 직접 Repository나 Supabase에 접근하지 않는다.
    """

    router = APIRouter(
        prefix="/users",
        tags=["User"]
    )

    # ==================================================
    # CREATE
    # ==================================================

    @router.post("")
    def create_user(request: UserCreateRequest):
        """
        새로운 사용자를 생성한다.

        POST /users
        """

        try:
            # API → Service
            result = user_service.create_user(
                user_id=request.user_id,
                email=request.email,
                nickname=request.nickname
            )

            return {
                "message": "사용자가 생성되었습니다.",
                "data": result
            }

        except ValueError as e:
            # Service의 비즈니스 예외를
            # HTTP 400 오류로 변환한다.
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

    # ==================================================
    # READ - 단일 사용자
    # ==================================================

    @router.get("/{user_id}")
    def get_user(user_id: int):
        """
        특정 사용자를 조회한다.

        GET /users/{user_id}
        """

        # API → Service
        result = user_service.get_user(user_id)

        # 사용자가 존재하지 않는 경우
        if result is None:
            raise HTTPException(
                status_code=404,
                detail="사용자를 찾을 수 없습니다."
            )

        return {
            "data": result
        }

    # ==================================================
    # READ - 전체 사용자
    # ==================================================

    @router.get("")
    def get_users():
        """
        모든 사용자를 조회한다.

        GET /users
        """

        # API → Service
        result = user_service.get_users()

        return {
            "data": result
        }

    # ==================================================
    # UPDATE
    # ==================================================

    @router.put("/{user_id}")
    def update_user(
        user_id: int,
        request: UserUpdateRequest
    ):
        """
        사용자 정보를 수정한다.

        PUT /users/{user_id}
        """

        try:
            # API → Service
            result = user_service.update_user(
                user_id=user_id,
                email=request.email,
                nickname=request.nickname
            )

            # 수정할 사용자가 없는 경우
            if result is None:
                raise HTTPException(
                    status_code=404,
                    detail="사용자를 찾을 수 없습니다."
                )

            return {
                "message": "사용자 정보가 수정되었습니다.",
                "data": result
            }

        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

    # ==================================================
    # DELETE
    # ==================================================

    @router.delete("/{user_id}")
    def delete_user(user_id: int):
        """
        사용자를 삭제한다.

        DELETE /users/{user_id}
        """

        # API → Service
        result = user_service.delete_user(user_id)

        # 삭제할 사용자가 없는 경우
        if result is None:
            raise HTTPException(
                status_code=404,
                detail="사용자를 찾을 수 없습니다."
            )

        return {
            "message": "사용자가 삭제되었습니다.",
            "data": result
        }

    return router