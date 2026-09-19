from typing import Optional, List, Dict, Any
from uuid import UUID

from repository.User_repository import UserRepository


class UserService:
    """
    User와 관련된 비즈니스 로직을 담당하는 Service 클래스.

    Service 계층의 역할:
    - 사용자의 요청을 처리
    - 필요한 비즈니스 규칙을 적용
    - Repository를 호출하여 DB 작업 수행

    DB에 직접 접근하지 않고 UserRepository를 통해 접근한다.
    """

    def __init__(self, user_repository: UserRepository):
        # Repository 객체를 전달받아 Service에서 사용할 수 있도록 한다.
        self.user_repository = user_repository

    # =========================
    # CREATE
    # =========================

    def create_user(
        self,
        user_id: UUID,
        email: str,
        nickname: str
    ) -> Dict[str, Any]:
        """
        새로운 사용자를 생성한다.
        """

        # 이메일이 입력되었는지 확인한다.
        if not email:
            raise ValueError("이메일은 필수입니다.")

        # 닉네임이 입력되었는지 확인한다.
        if not nickname:
            raise ValueError("닉네임은 필수입니다.")

        # 동일한 User_id를 가진 사용자가 이미 존재하는지 확인한다.
        existing_user = self.user_repository.get_user(user_id)

        if existing_user is not None:
            raise ValueError("이미 존재하는 User_id입니다.")

        # 실제 DB 저장은 Repository에서 담당한다.
        return self.user_repository.create_user(
            user_id=user_id,
            email=email,
            nickname=nickname
        )

    # =========================
    # READ
    # =========================

    def get_user(
        self,
        user_id: UUID,
    ) -> Optional[Dict[str, Any]]:
        """
        User_id를 이용하여 사용자 한 명을 조회한다.
        """

        # DB 조회는 Repository에게 요청한다.
        return self.user_repository.get_user(user_id)

    def get_users(self) -> List[Dict[str, Any]]:
        """
        모든 사용자를 조회한다.
        """

        # 전체 사용자 조회를 Repository에게 요청한다.
        return self.user_repository.get_users()

    # =========================
    # UPDATE
    # =========================

    def update_user(
        self,
        user_id: UUID,
        email: Optional[str] = None,
        nickname: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        사용자 정보를 수정한다.
        """

        # 업데이트할 값이 하나도 없으면 예외를 던진다.
        if email is None and nickname is None:
            raise ValueError("수정할 값이 없습니다.")

        return self.user_repository.update_user(
            user_id=user_id,
            email=email,
            nickname=nickname
        )

    # =========================
    # DELETE
    # =========================

    def delete_user(self, user_id: UUID) -> Optional[Dict[str, Any]]:
        """
        User_id를 이용하여 사용자 한 명을 삭제한다.
        """

        return self.user_repository.delete_user(user_id)
