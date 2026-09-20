from datetime import date as date_type, timedelta
from enum import Enum
import hashlib

import requests

KBO_URL = "https://www.koreabaseball.com/ws/Main.asmx/GetKboGameList"

STADIUM_ADDRESSES = {
    "잠실": "서울특별시 송파구 올림픽로 25",
    "문학": "인천광역시 미추홀구 매소홀로 618",
    "사직": "부산광역시 동래구 사직로 45",
    "수원": "경기도 수원시 장안구 경수대로 893",
    "대구": "대구광역시 수성구 야구전설로 1",
    "광주": "광주광역시 북구 서림로 10",
    "대전": "대전광역시 중구 대종로 373",
    "고척": "서울특별시 구로구 경인로 430",
    "창원": "경상남도 창원시 마산회원구 삼호로 63",
    "울산": "울산광역시 남구 문수로 44",
}


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
    """KBO 응답을 League 테이블 필드로 변환한다."""
    stadium_name = raw.get("S_NM", "")
    address = next(
        (value for key, value in STADIUM_ADDRESSES.items() if key in stadium_name),
        "",
    )
    external_game_id = str(raw["G_ID"])
    return {
        "League_id": _stable_game_id(external_game_id),
        "game_date": _format_game_date(raw.get("G_DT", "")),
        "game_time": raw.get("G_TM", ""),
        "game_name": "KBO 정규시즌",
        "stadium_name": stadium_name,
        "stadium_address": address,
        "status": _map_game_status(raw.get("GAME_STATE_SC", "")).value,
    }


def _stable_game_id(external_game_id: str) -> int:
    """KBO의 영숫자 경기 ID를 기존 bigint PK에 맞춘다."""
    digest = hashlib.sha256(external_game_id.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") & 0x1FFFFFFFFFFFFF


def _format_game_date(value: str) -> str:
    if len(value) == 8 and value.isdigit():
        return f"{value[:4]}-{value[4:6]}-{value[6:]}"
    return value


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


def get_regular_season_games(start_date: date_type, end_date: date_type) -> list[dict]:
    """시작일부터 종료일까지 정규 시즌 경기 일정을 수집한다."""
    games = []
    current_date = start_date

    while current_date <= end_date:
        games.extend(get_kbo_games_for_date(current_date))
        current_date += timedelta(days=1)

    return games