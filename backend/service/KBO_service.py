from datetime import date

from infra.KBO_infra import get_kbo_games_for_date


class KBOService:
    """KBO 경기 조회 흐름과 외부 연동을 연결한다."""

    def get_games(self, target_date: date) -> list[dict]:
        return get_kbo_games_for_date(target_date)