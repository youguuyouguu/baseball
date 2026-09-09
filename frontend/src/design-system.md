# 디자인 시스템

**테마**: 오렌지(포인트) + 화이트(배경) + 그레이(보조/텍스트) 기반의 깔끔한 모바일 앱 스타일
**모드**: 라이트모드만 지원
**폰트**: 시스템 기본 폰트 (별도 웹폰트 로딩 없음)

---

## 1. 색상 (Colors)

### Primary — Orange
눈에 자극적이지 않도록 채도를 낮춘 오렌지입니다. 배너·포인트 이미지처럼 강한 원색이 아니라, 버튼·아이콘·강조 텍스트에 써도 부담 없는 톤입니다.

| 토큰 | HEX | 용도 |
|---|---|---|
| orange-50 | `#FFF4EC` | 연한 배경 (강조 영역 배경 등) |
| orange-100 | `#FFE4D1` | 배지/태그 배경 |
| orange-200 | `#FFC9A8` | 비활성 강조 요소 |
| orange-300 | `#FFAB7A` | 보조 강조 |
| orange-400 | `#FF9257` | hover 전 단계 |
| **orange-500** | **`#FF7A45`** | **Primary — 버튼, 활성 탭, 강조 텍스트** |
| orange-600 | `#F2622A` | 버튼 pressed/hover |
| orange-700 | `#CC4E1A` | 진한 강조 (텍스트용) |

### Neutral — Gray & White
| 토큰 | HEX | 용도 |
|---|---|---|
| white | `#FFFFFF` | 기본 배경 |
| gray-50 | `#FAFAFA` | 섹션 구분 배경 |
| gray-100 | `#F5F5F5` | 카드/입력창 배경 |
| gray-200 | `#EEEEEE` | 구분선(divider) |
| gray-300 | `#E0E0E0` | 테두리(border) |
| gray-400 | `#BDBDBD` | placeholder, 비활성 아이콘 |
| gray-500 | `#9E9E9E` | 보조 텍스트, 비활성 탭 |
| gray-600 | `#757575` | 부제목 텍스트 |
| gray-700 | `#616161` | 본문 텍스트(보조) |
| gray-900 | `#1A1A1A` | 본문 텍스트(기본, 순검정 대신 사용) |

### Semantic
| 토큰 | HEX | 용도 |
|---|---|---|
| success | `#2FB170` | 성공, 완료 상태 |
| warning | `#FFB800` | 주의 |
| error | `#F04452` | 오류, 필수 입력 경고 |
| info | `#3B82F6` | 안내 |

---

## 2. 타이포그래피

시스템 폰트 스택:
```
-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
"Apple SD Gothic Neo", "Malgun Gothic", sans-serif
```

| 스타일 | 크기/행간 | 굵기 | 용도 |
|---|---|---|---|
| Display | 28px / 36px | 700 | 랜딩·인트로 카피 |
| Title1 | 22px / 30px | 700 | 화면 타이틀, "김한화님," 같은 인사말 |
| Title2 | 18px / 26px | 600 | 섹션 제목 |
| Body1 | 16px / 24px | 400~500 | 본문, 리스트 주요 텍스트 |
| Body2 | 14px / 20px | 400 | 보조 설명, 탭 라벨 |
| Caption | 12px / 16px | 400 | 날짜, 부가정보 |
| Button | 16px / 24px | 600 | 버튼 텍스트 |

텍스트 색상은 기본 `gray-900`, 보조 텍스트는 `gray-600`을 사용합니다.

---

## 3. 여백 (Spacing)

4px 그리드 기준 (Tailwind 기본 spacing 스케일과 동일하게 사용 가능):

| 토큰 | 값 |
|---|---|
| space-1 | 4px |
| space-2 | 8px |
| space-3 | 12px |
| space-4 | 16px |
| space-5 | 20px |
| space-6 | 24px |
| space-8 | 32px |
| space-10 | 40px |
| space-16 | 64px |

화면 좌우 기본 패딩: **20px**
카드/섹션 간 기본 간격: **24px**

---

## 4. 모서리 둥글기 (Radius)

"적당히 둥근" — 일반적인 모바일 앱 느낌:

| 토큰 | 값 | 용도 |
|---|---|---|
| radius-sm | 8px | 입력창, 작은 태그 |
| radius-md | 12px | 버튼, 리스트 아이템 |
| radius-lg | 16px | 카드, 배너 |
| radius-full | 9999px | 배지 점, 아바타, 알약형 버튼 |

---

## 5. 그림자 (Shadow)

과하지 않은 은은한 elevation:

| 토큰 | 값 | 용도 |
|---|---|---|
| shadow-sm | `0 1px 2px rgba(0,0,0,0.04)` | 리스트 아이템 |
| shadow-md | `0 2px 8px rgba(0,0,0,0.08)` | 카드 |
| shadow-lg | `0 4px 16px rgba(0,0,0,0.10)` | 모달, 팝업 |

---

## 6. 컴포넌트 스펙

### 버튼
| 종류 | 배경 | 텍스트 | 테두리 | radius |
|---|---|---|---|---|
| Primary | orange-500 (pressed: orange-600) | white | 없음 | radius-md |
| Secondary | white | orange-500 | 1px orange-500 | radius-md |
| Ghost/Text | 투명 | gray-700 | 없음 | - |
| Disabled | gray-200 | gray-400 | 없음 | radius-md |

사이즈: `lg` 높이 52px / `md` 높이 44px / `sm` 높이 36px, 좌우 패딩 16~20px

### 입력창 (Input)
- 배경 `gray-100`, 테두리 없음 (또는 `gray-300` 1px)
- 포커스 시 테두리 `orange-500` 2px
- radius-sm, 높이 48px, placeholder `gray-400`

### 카드
- 배경 `white`, radius-lg, `shadow-sm`
- 내부 패딩 16~20px
- 배너형 카드(이미지처럼 프로모션용)는 radius-lg + 오렌지 그라데이션 배경 허용

### 탭 (세그먼트, 예: "전체 · 보험 · 금융 · 건강")
- 활성: `gray-900` Bold + 하단 밑줄 `orange-500` 2px
- 비활성: `gray-500` Regular, 밑줄 없음
- 탭 간 간격 20~24px

### 상단 앱바 (Top App Bar)
- 배경 `white`, 높이 56px, 하단 구분선 없음(스크롤 시 `gray-200` 1px 표시)
- 아이콘 색상 `gray-800`, 아이콘 크기 24px
- 알림 아이콘에 미확인 표시 시 `orange-500` 8px 도트 (radius-full)

### 배지/알림 점
- 크기 8px, `orange-500`, radius-full
- 숫자 배지: 배경 `orange-500`, 텍스트 `white`, radius-full, 최소 크기 18px

### 아이콘
- 기본 24px, 인라인 텍스트 옆은 20px, 대형 강조는 28px
- 기본 색상 `gray-800`, 비활성/보조는 `gray-400`

---

## 7. Codex(AI 에이전트)에게 전달 시 안내

새 화면을 요청할 때마다 이 파일을 함께 첨부하고 "이 디자인 시스템의 토큰만 사용해서 만들어줘"라고 명시하세요. 임의로 색상/spacing 값을 새로 만들지 않도록 방지하는 게 목적입니다. 같은 프로젝트에 `tailwind.config.js`도 함께 제공하면 Codex가 `bg-orange-500`처럼 토큰 클래스명을 바로 재사용할 수 있습니다.
