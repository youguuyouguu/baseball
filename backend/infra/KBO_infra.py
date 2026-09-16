from datetime import date as date_type
from enum import Enum
from typing import Optional

import requests

KBO_URL = "https://www.koreabaseball.com/ws/Main.asmx/GetKboGameList"


class GameStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    CANCELED = "CANCELED"


def _map_game_status(state_code: str) -> GameStatus:
    return {
        "1": GameStatus.SCHEDULED,
        "2": GameStatus.IN_PROGRESS,
        "3": GameStatus.FINISHED,
        "4": GameStatus.CANCELED,
    }.get(state_code, GameStatus.SCHEDULED)


def _parse_game(raw: dict) -> dict:
    """KBO 응답 필드 변환."""
    return {
        "id": raw["G_ID"],
        "date": raw["G_DT"],  
        "start_time": raw["G_TM"],
        "stadium": raw["S_NM"],
        "home_team": raw["HOME_NM"],
        "away_team": raw["AWAY_NM"],
        "status": _map_game_status(raw.get("GAME_STATE_SC", "")).value,
        # 필드 추가 가능
    }


def get_kbo_games_for_date(target_date: date_type) -> list[dict]:
    """지정한 날짜의 KBO 경기 목록을 가져오고 경기가 없으면 빈 리스트 반환."""

    formatted_date = target_date.strftime("%Y%m%d")

    payload = {
        "leId": 1,  # KBO 리그 ID
        "srId": "0,1,3,4,5,6,7,8,9",  # 전체 시리즈
        "date": formatted_date,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://www.koreabaseball.com",
        "Referer": "https://www.koreabaseball.com/",
    }

    try:
        response = requests.post(
            KBO_URL, data=payload, headers=headers, timeout=5
        )
        response.raise_for_status()
    except requests.RequestException as e:
        # 상위(API 라우터)에서 500으로 처리하거나, 캐시된 이전 데이터로 폴백하도록
        raise RuntimeError(f"KBO 일정 조회 실패: {e}") from e

    data = response.json()
    games = data.get("game", [])

    if not games:
        return []

    return [_parse_game(g) for g in games]