
# repository/Review_repository.py

from typing import Optional, List, Dict, Any

from supabase import Client


class ReviewRepository:
    """
    Review 테이블과 직접 상호작용하는 Repository 클래스.

    역할:
    - 리뷰 생성(Create)
    - 리뷰 조회(Read)
    - 전체 리뷰 조회(Read All)
    - 리뷰 수정(Update)
    - 리뷰 삭제(Delete)

    비즈니스 로직은 Service 계층에서 처리하고,
    이 클래스에서는 Supabase DB와의 상호작용만 담당한다.
    """

    # Supabase에서 사용할 실제 테이블 이름
    TABLE_NAME = "Review"

    def __init__(self, supabase: Client):
        """
        Supabase Client를 전달받아 Repository를 생성한다.

        Args:
            supabase: 생성된 Supabase Client
        """

        # 전달받은 Supabase Client를 저장한다.
        # 이후 모든 DB 작업에서 이 객체를 사용한다.
        self.supabase = supabase

    # ==================================================
    # CREATE
    # ==================================================

    def create_review(
        self,
        review_id: int,
        user_id: int,
        place_id: int,
        content: str
    ) -> Dict[str, Any]:
        """
        새로운 리뷰를 생성한다.

        Args:
            review_id: 리뷰 ID
            user_id: 리뷰 작성자의 사용자 ID
            place_id: 리뷰 대상 장소 ID
            content: 리뷰 내용

        Returns:
            생성된 리뷰 데이터
        """

        # Supabase Review 테이블에 저장할 데이터를 만든다.
        data = {
            "Review_id": review_id,
            "user_id": user_id,
            "place_id": place_id,
            "content": content
        }

        # Review 테이블에 데이터를 INSERT한다.
        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .insert(data)
            .execute()
        )

        # 생성된 리뷰 데이터를 반환한다.
        return response.data[0]

    # ==================================================
    # READ
    # ==================================================

    def get_review(
        self,
        review_id: int
    ) -> Optional[Dict[str, Any]]:
        """
        Review_id를 이용하여 특정 리뷰를 조회한다.

        Args:
            review_id: 조회할 리뷰 ID

        Returns:
            리뷰가 존재하면 리뷰 데이터,
            존재하지 않으면 None
        """

        # Review_id가 일치하는 리뷰를 조회한다.
        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .select("*")
            .eq("Review_id", review_id)
            .execute()
        )

        # 조회 결과가 없는 경우 None을 반환한다.
        if not response.data:
            return None

        # 첫 번째 리뷰 데이터를 반환한다.
        return response.data[0]

    # ==================================================
    # READ ALL
    # ==================================================

    def get_reviews(self) -> List[Dict[str, Any]]:
        """
        모든 리뷰를 조회한다.

        Returns:
            전체 리뷰 목록
        """

        # Review 테이블의 모든 데이터를 조회한다.
        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .select("*")
            .execute()
        )

        # 리뷰 목록을 반환한다.
        return response.data

    # ==================================================
    # UPDATE
    # ==================================================

    def update_review(
        self,
        review_id: int,
        content: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        특정 리뷰의 내용을 수정한다.

        Args:
            review_id: 수정할 리뷰 ID
            content: 수정할 리뷰 내용

        Returns:
            수정된 리뷰 데이터
            또는 수정 대상이 없으면 None
        """

        # 실제로 수정할 데이터를 저장할 딕셔너리
        update_data = {}

        # content가 전달된 경우에만 수정한다.
        if content is not None:
            update_data["content"] = content

        # 수정할 값이 없는 경우 None을 반환한다.
        if not update_data:
            return None

        # Review_id가 일치하는 리뷰를 수정한다.
        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .update(update_data)
            .eq("Review_id", review_id)
            .execute()
        )

        # 수정된 데이터가 없는 경우 None을 반환한다.
        if not response.data:
            return None

        # 수정된 리뷰 데이터를 반환한다.
        return response.data[0]

    # ==================================================
    # DELETE
    # ==================================================

    def delete_review(
        self,
        review_id: int
    ) -> Optional[Dict[str, Any]]:
        """
        특정 리뷰를 삭제한다.

        Args:
            review_id: 삭제할 리뷰 ID

        Returns:
            삭제된 리뷰 데이터
            또는 삭제 대상이 없으면 None
        """

        # Review_id가 일치하는 리뷰를 삭제한다.
        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .delete()
            .eq("Review_id", review_id)
            .execute()
        )

        # 삭제된 데이터가 없는 경우 None을 반환한다.
        if not response.data:
            return None

        # 삭제된 리뷰 데이터를 반환한다.
        return response.data[0]
