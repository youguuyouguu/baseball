# service/League_service.py

from typing import Optional, List, Dict, Any

from repository.League_repository import LeagueRepository


class LeagueService:
    """
    League와 관련된 비즈니스 로직을 담당하는 Service 클래스.

    Service 계층의 역할:
    - 경기 일정 요청 처리
    - 필수 데이터 검증
    - 중복 경기 확인
    - LeagueRepository를 호출하여 DB 작업 수행

    DB에 직접 접근하지 않고 LeagueRepository를 통해 접근한다.
    """

    def __init__(self, League_repository: LeagueRepository):
        """
        LeagueRepository를 전달받아 Service를 생성한다.
        """

        self.League_repository = League_repository

    # ==================================================
    # CREATE
    # ==================================================

    def create_League(
        self,
        League_id: int,
        game_date: str,
        game_time: str,
        game_name: str,
        stadium_name: str,
        stadium_address: str
    ) -> Dict[str, Any]:
        """
        새로운 경기 일정을 생성한다.
        """

        # 필수 값 확인
        if not game_date:
            raise ValueError("경기 날짜는 필수입니다.")

        if not game_time:
            raise ValueError("경기 시간은 필수입니다.")

        if not game_name:
            raise ValueError("경기 이름은 필수입니다.")

        if not stadium_name:
            raise ValueError("경기장 이름은 필수입니다.")

        if not stadium_address:
            raise ValueError("경기장 주소는 필수입니다.")

        # 같은 League_id를 가진 경기가 이미 존재하는지 확인
        existing_League = self.League_repository.get_League(League_id)

        if existing_League is not None:
            raise ValueError("이미 존재하는 League_id입니다.")

        # Repository를 통해 DB에 저장
        return self.League_repository.create_League(
            League_id=League_id,
            game_date=game_date,
            game_time=game_time,
            game_name=game_name,
            stadium_name=stadium_name,
            stadium_address=stadium_address
        )

    # ==================================================
    # READ
    # ==================================================

    def get_League(
        self,
        League_id: int
    ) -> Optional[Dict[str, Any]]:
        """
        특정 경기 일정을 조회한다.
        """

        return self.League_repository.get_League(League_id)

    # ==================================================
    # READ ALL
    # ==================================================

    def get_Leagues(self) -> List[Dict[str, Any]]:
        """
        모든 경기 일정을 조회한다.
        """

        return self.League_repository.get_Leagues()

    # ==================================================
    # UPDATE
    # ==================================================

    def update_League(
        self,
        League_id: int,
        game_date: Optional[str] = None,
        game_time: Optional[str] = None,
        game_name: Optional[str] = None,
        stadium_name: Optional[str] = None,
        stadium_address: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        경기 일정을 수정한다.

        전달된 값만 수정한다.
        """

        # 수정할 값이 하나도 없는 경우
        if (
            game_date is None
            and game_time is None
            and game_name is None
            and stadium_name is None
            and stadium_address is None
        ):
            raise ValueError("수정할 값이 없습니다.")

        # Repository를 통해 수정
        return self.League_repository.update_League(
            League_id=League_id,
            game_date=game_date,
            game_time=game_time,
            game_name=game_name,
            stadium_name=stadium_name,
            stadium_address=stadium_address
        )

    # ==================================================
    # DELETE
    # ==================================================

    def delete_League(
        self,
        League_id: int
    ) -> Optional[Dict[str, Any]]:
        """
        특정 경기 일정을 삭제한다.
        """

        return self.League_repository.delete_League(League_id)