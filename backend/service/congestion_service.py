"""관광공사 관광지 집중률(혼잡도 예측) API 연동.

주의사항 (실제 API 특성):
- 관광지(tAtsNm) 카테고리만 데이터가 존재함. 음식점/숙박은 항상 매칭 실패 → None.
  따라서 places를 순회할 때 카테고리가 관광명소가 아니면 API 호출 자체를 생략한다.
- 응답에 장소 ID가 없고 이름 문자열(tAtsNm)로만 식별 가능 → 이름 매칭이 필요하고,
  매칭 실패 시 절대 억지로 추정하지 않는다 (다른 장소의 혼잡도를 잘못 붙이는 게 더 위험함).
- 응답은 baseYmd(날짜) 단위이며 시간대 구분이 없다. 즉 "하루 단위" 혼잡도 예측값이다.
"""

import os
from datetime import date as date_type
from typing import Optional
from dotenv import load_dotenv

load_dotenv()  # .env 파일에서 환경 변수 로드

import requests

TOUR_CONGESTION_URL = "https://apis.data.go.kr/B551011/TatsCnctrRateService/tatsCnctrRatedList"
SERVICE_KEY = os.environ["TOUR_API_SERVICE_KEY"]

# data.go.kr 참고문서의 '관광지_시군구_코드정보' 파일을 내려받아
# {"부산광역시 해운대구": {"areaCd": "6", "signguCd": "601"}, ...} 형태로 준비해두세요.
from infra.sigungu import SIGNGU_CODE_MAP


def _match_signgu_code(address: str) -> Optional[tuple[str, str]]:
    """장소 주소(카카오 로컬 API 응답의 address_name)에서 시군구를 찾아 지역코드로 변환."""
    for signgu_name, codes in SIGNGU_CODE_MAP.items():
        if signgu_name in address:
            return codes["areaCd"], codes["signguCd"]
    return None  # 코드표에 없는 지역 (매칭 실패)


def get_place_congestion(
    place_name: str, address: str, target_date: date_type
) -> Optional[dict]:
    """선택한 장소 하나의 특정 날짜 혼잡도를 조회.

    반환값: {"rate": 62.3, "level": "MEDIUM"} 또는 매칭 실패 시 None.
    None은 에러가 아니라 "이 장소는 혼잡도 데이터가 없음"을 의미함.
    """
    codes = _match_signgu_code(address or "")
    if codes is None:
        return None

    area_cd, signgu_cd = codes

    params = {
        "serviceKey": SERVICE_KEY,
        "pageNo": 1,
        "numOfRows": 30,  # 최대 약 30일치 예측이 한 번에 나옴
        "MobileOS": "ETC",
        "MobileApp": "AwayGameApp",
        "areaCd": area_cd,
        "signguCd": signgu_cd,
        "tAtsNm": place_name,
        "_type": "json",
    }

    try:
        response = requests.get(TOUR_CONGESTION_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        return None  # 외부 API 실패가 스케줄링 전체를 죽이면 안 됨

    body = data.get("response", {}).get("body", {})
    items = body.get("items", {})
    item_list = items.get("item", []) if items else []

    if not item_list:
        return None  # 관광지명 매칭 실패 (음식점/숙박이거나, 데이터셋에 없는 장소)

    target_str = target_date.strftime("%Y%m%d")
    matched = next((i for i in item_list if i["baseYmd"] == target_str), None)
    if matched is None:
        return None  # 해당 날짜가 예측 범위(약 30일) 밖임

    rate = float(matched["cnctrRate"])
    return {"rate": rate, "level": _classify_level(rate)}


def _classify_level(rate: float) -> str:
    """0~100 집중률을 사용자에게 보여줄 3단계로 분류."""
    if rate >= 80:
        return "HIGH"
    if rate >= 50:
        return "MEDIUM"
    return "LOW"


def build_congestion_cache(places: list[dict], target_date: date_type) -> dict[str, Optional[dict]]:
    """schedule_service.build_schedule에 넘길 congestion_cache를 미리 구성.

    places: [{"id": ..., "name": ..., "address": ..., "category": ...}, ...]
    반환: {place_id: {"rate": ..., "level": ...} | None}
    """
    cache: dict[str, Optional[dict]] = {}

    for place in places:
        if place.get("category") not in {"관광", "관광명소"}:
            # 음식점/숙박은 데이터셋에 없는 게 확인됐으므로 호출 자체를 생략 (불필요한 API 소모 방지)
            cache[place["id"]] = None
            continue

        cache[place["id"]] = get_place_congestion(
            place["name"], place["address"], target_date
        )

    return cache