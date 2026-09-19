데이터베이스(DB) 스키마 설계


## 1. 개요

본 문서는 앱에서 사용하는 데이터베이스의 테이블 구조와 테이블 간 관계를 정의한다.

현재 데이터베이스는 다음과 같은 기능을 중심으로 설계되어 있다.

* 사용자 정보 관리
* KBO 경기 일정 관리
* 사용자가 생성한 여행/경기 관람 일정 관리
* 일정에 포함된 세부 장소 및 방문 시간 관리
* 관광지 및 장소 정보 관리
* 사용자가 작성한 장소 리뷰 관리

### 주요 테이블

| 테이블               | 설명                      |
| ----------------- | ----------------------- |
| `User`            | 사용자 계정 및 기본 정보          |
| `league`          | KBO 경기 일정 정보            |
| `Tour`            | 사용자가 생성한 전체 일정          |
| `schedule_detail` | 일정에 포함되는 세부 장소 및 방문 시간  |
| `Tour_Place`     | API를 통해 수집한 관광지 및 장소 정보 |
| `review`          | 사용자가 장소에 작성한 리뷰         |

---

# 2. 테이블 구조

## 2.1 User

사용자의 기본 정보를 저장하는 테이블이다.

2.1 User (사용자)
- user_id (PK): UUID 형식의 사용자 식별자
- email: 이메일
- nickname: 닉네임


### 역할

* 사용자를 식별한다.
* 사용자가 생성한 일정표(`Tour`)와 연결된다.
* 사용자가 작성한 리뷰( `review`)와 연결된다.

---

2.2 League (경기 일정)
- league_id (PK): UUID 형식의 경기 식별자
- game_date: 경기 날짜
- game_time: 시작 시간
- stadium_name: 경기장 이름
- address: 경기장 주소

### 역할

* KBO 경기 일정 정보를 관리한다.
* `Tour`에서 특정 경기를 선택할 수 있도록 한다.

---

2.3 Tour (전체 일정)
- schedule_id (PK): UUID 형식의 일정 식별자
- user_id (FK): UUID 형식의 사용자 (User)
- game_id (FK): UUID 형식의 경기 (League)
- start_time: 일정 시작 시간
- end_time: 일정 종료 시간
- people_num: 참여 인원

### 외래 키

* `user_id` → `User.User_id`
* `game_id` → `league.league_id`

### 역할

하나의 여행 또는 경기 관람 계획에 대한 전체적인 정보를 저장한다.

예를 들어 사용자가 특정 KBO 경기를 관람하기 위해

> 출발 → 관광지 방문 → 식사 → 경기 관람

과 같은 일정을 만들 경우, 해당 전체 일정이 `Tour`에 저장된다.

---

2.4 ScheduleDetail (세부 일정)
- detail_id (PK): UUID 형식의 세부 일정 식별자
- schedule_id (FK): UUID 형식의 전체 일정 (Tour)
- place_id (FK): UUID 형식의 장소 (Place, Nullable)
- custom_name: 직접 입력한 장소명 (Nullable)
- start_at: 방문 시작 시간
- end_at: 방문 종료 시간
- state: 상태 (대기/진행/종료)
### 외래 키

* `schedule_id` → `Tour.schedule_id`
* `place_id` → `Tour_Places.places_id`

### `state`

세부 일정의 현재 상태를 저장한다.

예상 값:

* `시작전`
* `진행중`
* `종료`

### 장소 정보 처리

`place_id`와 `place_name` 중 하나만 사용해야 하는 경우를 고려한다.

* API에서 제공되는 장소를 선택한 경우 → `place_id` 사용
* 사용자가 직접 입력한 장소인 경우 → `place_name` 사용

따라서 `place_id`와 `place_name` 중 하나는 `NULL`이 될 수 있다.

---

2.5 Place (장소)
- place_id (PK): UUID 형식의 장소 식별자
- content_id: 외부 API의 문자열 식별자
- place_type: 장소 타입
- name: 장소 이름
- address: 주소
- lat, lng: 위도, 경도


### 역할

* 관광지 정보를 저장한다.
* 외부 API에서 받아온 장소 데이터를 앱에서 재사용할 수 있도록 한다.
* `schedule_detail`에서 방문 장소를 참조한다.
* `review`에서 리뷰 대상 장소를 참조한다.

---

2.6 Review (리뷰)
- review_id (PK): UUID 형식의 리뷰 식별자
- user_id (FK): UUID 형식의 작성자 (User)
- place_id (FK): UUID 형식의 장소 (Place)
- content: 내용

### 외래 키

* `user_id` → `User.User_id`
* `place_id` → `Tour_Places.places_id`

### 역할

사용자가 특정 장소에 남긴 리뷰를 저장한다.

리뷰 조회 시 사용자 정보와 장소 정보를 각각 참조하여 작성자와 리뷰 대상 장소를 확인할 수 있다.

---

# 3. 테이블 관계

전체적인 데이터 관계는 다음과 같다.

```text
User
 ├── 1:N ── Tour
 │            │
 │            ├── N:1 ── league
 │            │
 │            └── 1:N ── schedule_detail
 │                           │
 │                           └── N:1 ── Tour_Places
 │
 └── 1:N ── review
                │
                └── N:1 ── Tour_Places
```

### 관계 상세

| 부모 테이블        | 자식 테이블            | 관계  | 설명                            |
| ------------- | ----------------- | --- | ----------------------------- |
| `User`        | `Tour`            | 1:N | 한 사용자가 여러 일정을 생성할 수 있음        |
| `User`        | `review`          | 1:N | 한 사용자가 여러 리뷰를 작성할 수 있음        |
| `league`      | `Tour`            | 1:N | 하나의 경기를 여러 사용자의 일정에서 선택할 수 있음 |
| `Tour`        | `schedule_detail` | 1:N | 하나의 일정에 여러 세부 일정이 포함될 수 있음    |
| `Tour_Places` | `schedule_detail` | 1:N | 하나의 장소가 여러 일정에서 사용될 수 있음      |
| `Tour_Places` | `review`          | 1:N | 하나의 장소에 여러 리뷰가 작성될 수 있음       |

---

# 4. 데이터 흐름

## 일정 생성

1. 사용자가 `User`를 통해 로그인한다.
2. 사용자가 `league`에서 관람할 KBO 경기를 선택한다.
3. 선택한 사용자와 경기를 기준으로 `Tour`를 생성한다.
4. 관광지 또는 장소를 선택한다.
5. 선택한 장소를 `schedule_detail`에 추가한다.
6. 방문 시간과 일정 상태를 저장한다.

```text
User
 ↓
경기 선택
 ↓
league
 ↓
Tour 생성
 ↓
장소 선택
 ↓
schedule_detail
 ↓
Tour_Places
```

## 리뷰 작성

1. 사용자가 특정 장소를 선택한다.
2. `Tour_Places`에서 장소 정보를 확인한다.
3. 사용자가 리뷰를 작성한다.
4. `review`에 작성자와 장소의 FK를 저장한다.

```text
User
 ↓
장소 선택
 ↓
Tour_Places
 ↓
리뷰 작성
 ↓
review
```

---

# 5. 주요 제약 조건

### PK

각 테이블의 기본 키는 다음과 같다.

* `User.User_id`
* `league.league_id`
* `Tour.schedule_id`
* `schedule_detail.detail_id`
* `Tour_Places.places_id`
* `review.review_id`

각 PK는 해당 테이블의 데이터를 고유하게 식별한다.

### FK

외래 키 관계는 다음과 같다.

```text
Tour.user_id
    → User.User_id

Tour.game_id
    → league.league_id

schedule_detail.schedule_id
    → Tour.schedule_id

schedule_detail.place_id
    → Tour_Places.places_id

review.user_id
    → User.User_id

review.place_id
    → Tour_Places.places_id
```

---

# 6. 데이터 무결성

외래 키를 이용하여 존재하지 않는 사용자, 경기, 일정 또는 장소를 참조하는 데이터가 생성되지 않도록 한다.

예를 들어 `review.user_id`는 반드시 `User.User_id`에 존재하는 사용자를 참조해야 한다.

또한 일정 삭제 또는 장소 삭제 시 관련 데이터가 어떻게 처리될 것인지에 대한 정책을 별도로 정의해야 한다.

예:

* 사용자 삭제 → 해당 사용자의 일정 및 리뷰 삭제 여부 결정
* 일정 삭제 → 해당 일정의 `schedule_detail` 삭제
* 장소 삭제 → 해당 장소를 참조하는 일정 및 리뷰 처리 방식 결정

---

# 7. 설계 시 주의사항

## 7.1 장소 ID 명칭 통일

현재 ERD에서는 장소 테이블의 PK가 `places_id`이고, 이를 참조하는 컬럼은 `place_id`로 되어 있다.

```text
Tour_Places.places_id
        ↑
schedule_detail.place_id
review.place_id
```

실제 구현에서는 혼동을 줄이기 위해 다음과 같이 명칭을 통일하는 것을 권장한다.

```text
Tour_Places.place_id
schedule_detail.place_id
review.place_id
```

또는 현재 구조를 유지할 경우 FK가 정확히 `Tour_Places.places_id`를 참조하도록 명시한다.

## 7.2 날짜/시간 컬럼 명칭 통일

현재 `created_at`, `create_at`이 혼용되고 있다.

권장 형식:

```text
created_at
updated_at
```

따라서 `Tour_Places.create_at` 역시 `created_at`으로 통일하는 것을 권장한다.

## 7.3 `place_name` 중복 저장

`Tour_Places`에 이미 `place_name`이 존재하지만 `schedule_detail`에도 `place_name`이 존재한다.

장소 이름을 항상 `Tour_Places`에서 조회할 수 있다면 `schedule_detail.place_name`은 중복 데이터가 될 수 있다.

다만 사용자가 직접 입력한 장소를 지원하기 위한 목적이라면 다음과 같이 구분할 수 있다.

```text
place_id     → 등록된 장소/API 장소
place_name   → 사용자가 직접 입력한 장소
```

이 경우 둘 중 하나만 값이 존재하도록 제약 조건을 적용하는 것이 좋다.

---

# 8. 향후 확장 가능성

추후 앱 기능이 확장될 경우 다음과 같은 테이블을 추가할 수 있다.

* 사용자 선호 장소
* 장소 즐겨찾기
* 경기 팀 정보
* 경기 결과
* 관광지 카테고리
* 리뷰 이미지
* 일정 공유
* 일정 참가자
* 알림 정보

특히 하나의 `Tour`에 여러 사용자가 참여할 수 있도록 확장한다면 현재 `Tour.user_id` 구조만으로는 부족할 수 있으므로 별도의 일정 참가자 테이블을 추가하는 것을 고려한다.

예:

```text
Tour
  │
  └── Tour_User
          │
          └── User
```

이를 통해 하나의 여행 일정에 여러 사용자가 참여할 수 있도록 확장할 수 있다.
