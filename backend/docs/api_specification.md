# 원정로드 API 명세서

## 1. API 개요

### 1.1 목적

본 문서는 원정로드 앱과 백엔드 서버 간의 데이터 통신을 위한 API 명세를 정의한다.

원정로드는 사용자가 KBO 경기 일정을 기준으로 원정 여행 일정을 생성하고, 경기장 주변의 관광지·식당·숙소 등의 장소를 조회하여 일정에 추가할 수 있도록 한다.

또한 한국관광공사 OpenAPI를 활용하여 장소 정보와 관광 데이터를 제공하고, 관광지 방문자 추이 예측 정보를 활용하여 일정에 포함된 장소의 혼잡 가능성을 안내한다.

---

# 2. 시스템 구성

기본적인 API 요청 흐름은 다음과 같다.

```text
Android App
    │
    │ HTTP Request
    ▼
API Server
    │
    ├── User / Tour / Review
    │       │
    │       ▼
    │      DB
    │
    └── 관광지 / 혼잡도 데이터
            │
            ▼
      한국관광공사 OpenAPI
```

앱에서 API Server로 요청을 보내면 서버는 요청에 따라 DB 또는 외부 API에서 데이터를 조회·가공한 후 앱에 응답한다.

---

# 3. API 기본 규칙

## 3.1 Base URL

```text
/api
```

> 실제 배포 서버 주소는 서버 구축 이후 결정한다.

## 3.2 통신 방식

* Protocol: HTTP/HTTPS
* Data Format: JSON
* Character Encoding: UTF-8

## 3.3 HTTP Method

| Method   | 용도     |
| -------- | ------ |
| `GET`    | 데이터 조회 |
| `POST`   | 데이터 생성 |
| `PUT`    | 데이터 수정 |
| `DELETE` | 데이터 삭제 |

---

# 4. API 목록

| 기능       | Method | Endpoint                                 | 설명               |
| -------- | ------ | ---------------------------------------- | ---------------- |
| 사용자 조회   | GET    | `/users/{userId}`                        | 사용자 정보 조회        |
| 사용자 생성   | POST   | `/users`                                 | 사용자 정보 생성        |
| 경기 목록 조회 | GET    | `/games`                                 | KBO 경기 일정 조회     |
| 경기 상세 조회 | GET    | `/games/{gameId}`                        | 특정 경기 정보 조회      |
| 일정 생성    | POST   | `/tours`                                 | 새로운 원정 일정 생성     |
| 일정 조회    | GET    | `/tours/{scheduleId}`                    | 일정 상세 조회         |
| 일정 목록 조회 | GET    | `/users/{userId}/tours`                  | 사용자의 일정 목록 조회    |
| 세부 일정 추가 | POST   | `/tours/{scheduleId}/details`            | 일정에 장소 추가        |
| 세부 일정 수정 | PUT    | `/tours/{scheduleId}/details/{detailId}` | 일정 시간 및 상태 수정    |
| 세부 일정 삭제 | DELETE | `/tours/{scheduleId}/details/{detailId}` | 일정에서 장소 삭제       |
| 장소 검색    | GET    | `/places`                                | 관광지·식당·숙소 검색     |
| 장소 상세 조회 | GET    | `/places/{placeId}`                      | 장소 상세 정보 조회      |
| 장소 추천    | GET    | `/places/recommend`                      | 원정 일정에 적합한 장소 추천 |
| 혼잡도 조회   | GET    | `/places/{placeId}/congestion`           | 장소의 혼잡 가능성 조회    |
| 리뷰 등록    | POST   | `/places/{placeId}/reviews`              | 장소 리뷰 등록         |
| 리뷰 조회    | GET    | `/places/{placeId}/reviews`              | 장소 리뷰 조회         |
| 리뷰 수정    | PUT    | `/reviews/{reviewId}`                    | 리뷰 수정            |
| 리뷰 삭제    | DELETE | `/reviews/{reviewId}`                    | 리뷰 삭제            |

---

# 5. 사용자 API

## 5.1 사용자 정보 조회

### Request

```http
GET /api/users/{userId}
```

### Path Parameter

| 이름       | 타입             | 설명      |
| -------- | -------------- | ------- |
| `userId` | Integer/String | 사용자 식별자 |

### Response

```json
{
  "userId": 1,
  "email": "user@example.com",
  "nickname": "원정팬",
  "createdAt": "2026-08-19T10:00:00"
}
```

---

# 6. 경기 API

## 6.1 경기 목록 조회

사용자가 원정 관람 경기를 선택할 수 있도록 KBO 경기 일정을 조회한다.

### Request

```http
GET /api/games
```

### Query Parameter

| 이름     | 타입      | 필수 | 설명     |
| ------ | ------- | -- | ------ |
| `date` | String  | X  | 경기 날짜  |
| `team` | String  | X  | 구단 검색  |
| `page` | Integer | X  | 페이지 번호 |

### Response

```json
{
  "games": [
    {
      "gameId": 101,
      "gameDate": "2026-08-25",
      "gameTime": "18:30",
      "stadiumName": "○○구장",
      "stadiumAddress": "○○시 ○○구"
    }
  ]
}
```

---

## 6.2 경기 상세 조회

### Request

```http
GET /api/games/{gameId}
```

### Response

```json
{
  "gameId": 101,
  "gameDate": "2026-08-25",
  "gameTime": "18:30",
  "stadiumName": "○○구장",
  "stadiumAddress": "○○시 ○○구"
}
```

---

# 7. 일정 API

원정로드의 핵심 기능으로, 선택한 경기를 기준으로 사용자의 원정 여행 일정을 관리한다.

## 7.1 일정 생성

### Request

```http
POST /api/tours
```

### Request Body

```json
{
  "userId": 1,
  "gameId": 101,
  "startingTime": "2026-08-25T09:00:00",
  "endTime": "2026-08-26T12:00:00",
  "startingPlace": "서울역",
  "peopleNum": 2
}
```

### Response

```json
{
  "scheduleId": 1001,
  "message": "일정이 생성되었습니다."
}
```

---

## 7.2 일정 조회

### Request

```http
GET /api/tours/{scheduleId}
```

### Response

```json
{
  "scheduleId": 1001,
  "userId": 1,
  "gameId": 101,
  "gameName": "○○ vs ○○",
  "startingTime": "2026-08-25T09:00:00",
  "endTime": "2026-08-26T12:00:00",
  "startingPlace": "서울역",
  "peopleNum": 2,
  "details": [
    {
      "detailId": 1,
      "placeId": 301,
      "placeName": "○○관광지",
      "startAt": "2026-08-25T11:00:00",
      "endAt": "2026-08-25T13:00:00",
      "state": "종료"
    }
  ]
}
```

---

# 8. 세부 일정 API

`Tour`에 포함되는 개별 방문 장소와 시간을 관리한다.

## 8.1 세부 일정 추가

### Request

```http
POST /api/tours/{scheduleId}/details
```

### Request Body

```json
{
  "placeId": 301,
  "placeName": "○○관광지",
  "startAt": "2026-08-25T11:00:00",
  "endAt": "2026-08-25T13:00:00"
}
```

### Response

```json
{
  "detailId": 1,
  "scheduleId": 1001,
  "placeId": 301,
  "message": "세부 일정이 추가되었습니다."
}
```

---

## 8.2 세부 일정 수정

사용자가 일정표를 수정하거나 혼잡도 정보를 확인한 후 방문 시간을 변경할 때 사용한다.

### Request

```http
PUT /api/tours/{scheduleId}/details/{detailId}
```

### Request Body

```json
{
  "startAt": "2026-08-25T12:00:00",
  "endAt": "2026-08-25T14:00:00",
  "state": "시작전"
}
```

---

## 8.3 세부 일정 삭제

### Request

```http
DELETE /api/tours/{scheduleId}/details/{detailId}
```

### Response

```json
{
  "message": "세부 일정이 삭제되었습니다."
}
```

---

# 9. 장소 API

한국관광공사 관광정보를 기반으로 관광지·식당·숙소 등의 장소 정보를 제공한다.

제안서에서는 지역의 관광지·식당·숙소 조회, 관광지 키워드 검색, 장소 상세 정보 조회를 주요 활용 방식으로 정의하고 있다.

## 9.1 장소 검색

### Request

```http
GET /api/places
```

### Query Parameter

| 이름          | 타입      | 필수 | 설명     |
| ----------- | ------- | -- | ------ |
| `keyword`   | String  | X  | 검색어    |
| `area`      | String  | X  | 지역     |
| `type`      | String  | X  | 장소 유형  |
| `latitude`  | Double  | X  | 기준 위도  |
| `longitude` | Double  | X  | 기준 경도  |
| `page`      | Integer | X  | 페이지 번호 |

### `type` 예시

```text
TOURIST
RESTAURANT
ACCOMMODATION
```

### Response

```json
{
  "places": [
    {
      "placeId": 301,
      "contentId": "123456",
      "contentTypeId": "12",
      "placeName": "○○관광지",
      "address": "○○시 ○○구",
      "longitude": 127.123456,
      "latitude": 36.123456,
      "image": "image_url"
    }
  ]
}
```

---

# 10. 장소 추천 API

사용자의 경기 일정과 출발 위치 등을 기준으로 원정 경기 지역의 장소를 추천한다.

원정로드는 경기장과의 거리, 이동 시간 등을 고려하고, 누적된 원정 팬 방문 이력을 추천에 활용하는 것을 목표로 한다.

## 10.1 장소 추천

### Request

```http
GET /api/places/recommend
```

### Query Parameter

| 이름          | 타입       | 필수 | 설명       |
| ----------- | -------- | -- | -------- |
| `gameId`    | Integer  | O  | 관람 경기    |
| `latitude`  | Double   | O  | 기준 위치 위도 |
| `longitude` | Double   | O  | 기준 위치 경도 |
| `type`      | String   | X  | 장소 유형    |
| `peopleNum` | Integer  | X  | 방문 인원    |
| `startAt`   | DateTime | X  | 방문 예정 시간 |

### Response

```json
{
  "places": [
    {
      "placeId": 301,
      "placeName": "○○관광지",
      "type": "TOURIST",
      "distance": 1.2,
      "estimatedTravelTime": 15,
      "recommendScore": 0.91
    }
  ]
}
```

> `recommendScore`의 실제 계산 방식은 추천 알고리즘 구현 단계에서 정의한다.

---

# 11. 혼잡도 API

한국관광공사의 관광지 집중률 방문자 추이 예측 정보를 활용하여 특정 시간대에 혼잡할 가능성이 있는 장소를 안내한다.

제안서에서는 해당 데이터가 실시간 혼잡도가 아니라 과거 패턴 기반의 예측값이라는 점을 명시하고 있다. 따라서 API 응답 역시 실제 실시간 인원 수가 아닌 **혼잡 가능성**을 제공하는 형태로 설계한다.

## 11.1 혼잡도 조회

### Request

```http
GET /api/places/{placeId}/congestion
```

### Query Parameter

| 이름     | 타입   | 필수 | 설명       |
| ------ | ---- | -- | -------- |
| `date` | Date | O  | 방문 예정 날짜 |
| `time` | Time | O  | 방문 예정 시간 |

### Response

```json
{
  "placeId": 301,
  "date": "2026-08-25",
  "time": "13:00",
  "congestionLevel": "HIGH",
  "prediction": 0.82,
  "message": "혼잡할 가능성이 높습니다."
}
```

### 혼잡도 단계

| 값        | 의미         |
| -------- | ---------- |
| `LOW`    | 혼잡 가능성이 낮음 |
| `MEDIUM` | 혼잡 가능성이 보통 |
| `HIGH`   | 혼잡 가능성이 높음 |

---

# 12. 리뷰 API

사용자는 방문한 장소에 대해 인파, 소요 시간, 서비스 품질 등의 후기를 작성할 수 있다.

## 12.1 리뷰 등록

### Request

```http
POST /api/places/{placeId}/reviews
```

### Request Body

```json
{
  "userId": 1,
  "content": "경기 전에 방문하기 좋았습니다."
}
```

### Response

```json
{
  "reviewId": 5001,
  "placeId": 301,
  "userId": 1,
  "content": "경기 전에 방문하기 좋았습니다.",
  "createdAt": "2026-08-25T15:30:00"
}
```

---

## 12.2 리뷰 조회

### Request

```http
GET /api/places/{placeId}/reviews
```

### Response

```json
{
  "reviews": [
    {
      "reviewId": 5001,
      "userId": 1,
      "nickname": "원정팬",
      "content": "경기 전에 방문하기 좋았습니다.",
      "createdAt": "2026-08-25T15:30:00"
    }
  ]
}
```

---

## 12.3 리뷰 수정

### Request

```http
PUT /api/reviews/{reviewId}
```

### Request Body

```json
{
  "content": "경기 전에 방문하기 좋았고 이동하기도 편했습니다."
}
```

---

## 12.4 리뷰 삭제

### Request

```http
DELETE /api/reviews/{reviewId}
```

### Response

```json
{
  "message": "리뷰가 삭제되었습니다."
}
```

---

# 13. 공통 응답 형식

성공 및 실패 응답의 형식을 통일하여 클라이언트에서 처리하기 쉽도록 한다.

## 성공

```json
{
  "success": true,
  "data": {}
}
```

## 실패

```json
{
  "success": false,
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "필수 파라미터가 누락되었습니다."
  }
}
```

---

# 14. HTTP 상태 코드

| 상태 코드                       | 의미           |
| --------------------------- | ------------ |
| `200 OK`                    | 요청 성공        |
| `201 Created`               | 데이터 생성 성공    |
| `204 No Content`            | 삭제 또는 수정 성공  |
| `400 Bad Request`           | 잘못된 요청       |
| `401 Unauthorized`          | 인증 필요        |
| `403 Forbidden`             | 권한 없음        |
| `404 Not Found`             | 요청한 데이터 없음   |
| `500 Internal Server Error` | 서버 내부 오류     |
| `502 Bad Gateway`           | 외부 API 통신 오류 |

---

# 15. API와 DB 테이블 관계

API에서 사용하는 주요 데이터는 다음 DB 테이블과 연결된다.

| API 기능    | 관련 DB                             |
| --------- | --------------------------------- |
| 사용자 API   | `User`                            |
| 경기 API    | `league`                          |
| 일정 API    | `Tour`                            |
| 세부 일정 API | `schedule_detail`                 |
| 장소 API    | `Tour_Places`                     |
| 리뷰 API    | `review`                          |
| 혼잡도 API   | `Tour_Places` + 외부 관광 데이터         |
| 장소 추천 API | `Tour_Places` + `review` + 일정 데이터 |

전체적인 관계는 다음과 같다.

```text
User
 │
 ├── Tour ─────────────── league
 │     │
 │     └── schedule_detail ─── Tour_Places
 │                                  │
 └── review ───────────────────────┘
```

---

# 16. 외부 API 연동

원정로드의 서버는 필요한 관광 데이터를 한국관광공사 OpenAPI에서 가져온 후 앱에서 사용하기 적합한 형태로 가공한다.

```text
Android App
     │
     ▼
API Server
     │
     ├──────────────► 내부 DB
     │
     └──────────────► 한국관광공사 OpenAPI
                           │
                           ├─ 관광지 정보
                           ├─ 식당 정보
                           ├─ 숙소 정보
                           └─ 관광지 방문자 추이 예측
```

한국관광공사 API는 지역의 관광지·식당·숙소 조회와 관광지 검색 및 장소 상세 정보 제공에 활용하며, 관광지 집중률 방문자 추이 예측 정보는 일정 계획 및 수정 과정에서 혼잡 가능성을 안내하는 데 활용한다.

---

# 17. 추후 확정이 필요한 항목

현재 문서는 기능 구조와 DB 스키마를 기반으로 작성한 **1차 API 명세 초안**이다.

실제 구현 전에 다음 항목을 확정해야 한다.

* [ ] 실제 Base URL
* [ ] 인증 방식 및 토큰 구조
* [ ] `userId`, `gameId` 등의 실제 데이터 타입
* [ ] KBO 경기 데이터의 실제 수집 방법
* [ ] 한국관광공사 OpenAPI의 실제 Endpoint
* [ ] 외부 API 요청 파라미터
* [ ] 추천 알고리즘의 입력값 및 점수 계산 방식
* [ ] 혼잡도 데이터의 실제 응답 형식
* [ ] 페이징 방식
* [ ] 에러 코드 목록
* [ ] CORS 및 보안 정책
* [ ] API 버전 관리 방식 (`/api/v1` 등)

> 특히 **한국관광공사 OpenAPI의 실제 Endpoint와 응답 JSON은 현재 제공된 자료만으로 확정할 수 없으므로**, 실제 API를 연결할 때 해당 API 문서를 기준으로 별도 작성해야 한다.
