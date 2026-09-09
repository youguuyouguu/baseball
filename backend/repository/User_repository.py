from typing import Optional, List, Dict, Any

from supabase import Client


class UserRepository:
    """
    User 테이블과 직접 상호작용하는 Repository 클래스.

    역할:
    - User 데이터 생성(Create)
    - User 데이터 조회(Read)
    - User 데이터 수정(Update)
    - User 데이터 삭제(Delete)

    비즈니스 로직은 Service 계층에서 처리하고,
    이 클래스에서는 DB와의 상호작용만 담당한다.
    """

    # Supabase에서 사용할 테이블 이름
    TABLE_NAME = "User"

    def __init__(self, supabase: Client):
        """
        Supabase 클라이언트를 전달받아 Repository를 생성한다.

        Args:
            supabase: 생성된 Supabase Client
        """
        self.supabase = supabase

    # --------------------------------------------------
    # CREATE
    # --------------------------------------------------

    def create_user(
        self,
        user_id: int,
        email: str,
        nickname: str
    ) -> Dict[str, Any]:
        """
        새로운 사용자를 생성한다.

        Args:
            user_id: 사용자 ID
            email: 사용자 이메일
            nickname: 사용자 닉네임

        Returns:
            생성된 사용자 데이터
        """

        data = {
            "User_id": user_id,
            "email": email,
            "nickname": nickname
        }

        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .insert(data)
            .execute()
        )

        return response.data[0]

    # --------------------------------------------------
    # READ
    # --------------------------------------------------

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        User_id를 이용해 특정 사용자를 조회한다.

        Args:
            user_id: 조회할 사용자 ID

        Returns:
            사용자가 존재하면 사용자 데이터,
            존재하지 않으면 None
        """

        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .select("*")
            .eq("User_id", user_id)
            .execute()
        )

        if not response.data:
            return None

        return response.data[0]

    # --------------------------------------------------
    # READ ALL
    # --------------------------------------------------

    def get_users(self) -> List[Dict[str, Any]]:
        """
        모든 사용자를 조회한다.

        Returns:
            사용자 목록
        """

        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .select("*")
            .execute()
        )

        return response.data

    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------

    def update_user(
        self,
        user_id: int,
        email: Optional[str] = None,
        nickname: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        사용자의 이메일 또는 닉네임을 수정한다.

        전달된 값만 수정한다.

        Args:
            user_id: 수정할 사용자 ID
            email: 수정할 이메일
            nickname: 수정할 닉네임

        Returns:
            수정된 사용자 데이터
        """

        update_data = {}

        if email is not None:
            update_data["email"] = email

        if nickname is not None:
            update_data["nickname"] = nickname

        # 수정할 값이 하나도 없는 경우
        if not update_data:
            return None

        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .update(update_data)
            .eq("User_id", user_id)
            .execute()
        )

        if not response.data:
            return None

        return response.data[0]

    # --------------------------------------------------
    # DELETE
    # --------------------------------------------------

    def delete_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        특정 사용자를 삭제한다.

        Args:
            user_id: 삭제할 사용자 ID

        Returns:
            삭제된 사용자 데이터
        """

        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .delete()
            .eq("User_id", user_id)
            .execute()
        )

        if not response.data:
            return None

        return response.data[0]