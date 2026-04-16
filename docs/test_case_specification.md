# 토스증권 공개 웹 테스트 케이스 명세

## 1. 목적

이 문서는 토스증권 공개 웹 UI 자동화의 테스트 케이스 명세입니다.

테스트 케이스 원본은 `test_cases/tossinvest_public_cases.yaml`에서 관리합니다. 이 문서는 사람이 읽기 쉬운 요약과 suite 정책을 제공합니다.

## 2. 현재 현황

| 항목 | 값 |
|---|---:|
| 전체 테스트 케이스 | 60개 |
| BVT 후보 ID | 33개 |
| pytest 전체 자동화 테스트 | 37개 |
| pytest BVT 자동화 테스트 | 31개 |
| 최근 BVT 실행 결과 | 31 passed, 6 deselected |
| 최근 전체 suite 실행 결과 | 37 passed |

## 3. 테스트 케이스 포맷

테스트 케이스는 YAML로 관리합니다.

파일:

```text
test_cases/tossinvest_public_cases.yaml
```

YAML을 사용하는 이유:

- 리뷰하기 쉽습니다.
- `steps`, `tags`, `data` 같은 중첩 데이터를 표현하기 좋습니다.
- 이후 pytest parameterization 또는 generator 입력으로 사용할 수 있습니다.
- JSON보다 사람이 수정하기 쉽고, Markdown 표보다 자동 처리에 유리합니다.

필수 필드:

| 필드 | 설명 | 예시 |
|---|---|---|
| `id` | 테스트 케이스 고유 ID | `TI-WEB-053` |
| `title` | 테스트 제목 | `BVT 로그인 페이지 기본 옵션 노출` |
| `precondition` | 사전 조건 | `사용자는 로그인 페이지에 접속해 있다.` |
| `steps` | 실행 절차 | `QR코드로 로그인을 선택한다.` |
| `expected_result` | 기대 결과 | `QR 로그인 안내가 표시된다.` |
| `priority` | 우선순위 | `P0`, `P1`, `P2` |
| `tags` | 기능/성격 태그 | `[bvt, login, auth]` |
| `data` | 테스트 데이터 | `{ query: "삼성전자" }` |
| `smoke` | smoke 포함 여부 | `true` |
| `regression` | regression 포함 여부 | `true` |
| `automation_status` | 자동화 상태 | `ready`, `conditional`, `staging_required` |

## 4. 자동화 상태 정의

| 상태 | 의미 |
|---|---|
| `ready` | 운영 공개 웹에서 자동화 가능 |
| `conditional` | 공개 DOM 또는 서비스 상태에 따라 조건부 검증 |
| `staging_required` | 스테이징 계정/데이터 필요 |
| `needs_mock_or_staging` | mock 또는 fault injection 필요 |
| `manual_or_lab` | 수동 또는 별도 lab 환경 필요 |

## 5. Suite 정의

| Suite | 설명 |
|---|---|
| BVT | 빌드가 기본 품질 기준을 만족하는지 빠르게 확인 |
| Smoke | PR에서 빠르게 실행하는 핵심 경로 |
| Regression | main/nightly에서 실행하는 공개 웹 회귀 검증 |
| Login | 실제 로그인 성공 전까지의 공개 로그인 UX 검증 |
| Auth | 비로그인 보호와 인증 경계 검증 |
| Responsive | 모바일/데스크톱 뷰포트 검증 |
| Search | 종목 검색 검증 |
| Quote | 시세/차트/종목 상세 검증 |

## 6. 주요 테스트 케이스 범위

| ID 범위 | 주요 내용 |
|---|---|
| TI-WEB-001 ~ 006 | 홈, 푸터, 메뉴, 내 계좌 인증 유도 |
| TI-WEB-007 ~ 010 | 검색 진입, 국내/해외/없는 종목 검색 |
| TI-WEB-011 ~ 015 | 종목 상세, 차트, 관심종목, 거래 CTA 보호 |
| TI-WEB-016 ~ 024 | 반응형, 오류, 접근성, 새로고침, 정책 링크 |
| TI-WEB-025 ~ 036 | 검색 UX, 지수, 시장 상태, 피드, 주식 골라보기, 태블릿, 뒤로가기 |
| TI-WEB-037 ~ 052 | BVT 확장 케이스: 홈 안정화, 앱 오류 미노출, 검색, 차트, 시장 정보, 로딩, 네비게이션 |
| TI-WEB-053 ~ 060 | 로그인 BVT: 로그인 진입, 옵션, QR, 문자 인증 폼, 빈 요청, 가입 링크, 비로그인 계좌 보호 |

## 7. BVT 후보

YAML의 `bvt_suite.candidate_ids`에 BVT 후보 ID를 관리합니다.

현재 BVT 후보는 다음 성격을 포함합니다.

- 홈 최초 진입 안정화
- 전체 앱 오류 미노출
- 검색 입력과 대표 종목 검색
- 공개 종목 상세 진입
- 실시간 차트와 지수 요약
- 모바일/데스크톱 렌더링
- 로그인 진입과 로그인 옵션
- QR/SMS 로그인 안내
- 비로그인 계좌 보호
- 개인 정보 비노출
- 새로고침/뒤로가기/초기 로딩 안정성

## 8. 자동화 파일 매핑

| 파일 | 담당 영역 |
|---|---|
| `tests/test_home.py` | 홈, 내 계좌 인증 유도, 차트 필터 |
| `tests/test_search.py` | 검색 진입, 대표 종목 검색, 없는 종목 검색 |
| `tests/test_stock_detail.py` | 종목 상세, 시세/차트, 관심종목 인증 유도, 로딩 해소 |
| `tests/test_responsive.py` | 모바일/데스크톱 렌더링 |
| `tests/test_bvt_extended.py` | BVT 확장: 홈, 시장 정보, 차트, 네비게이션, 로딩 |
| `tests/test_login.py` | 로그인 진입, 로그인 옵션, QR, 문자 인증, 가입, 비로그인 계좌 보호 |

## 9. Marker 정책

| Marker | 용도 |
|---|---|
| `bvt` | 빌드 검증 테스트 |
| `smoke` | PR 핵심 경로 |
| `regression` | 회귀 테스트 |
| `login` | 로그인 공개 UX |
| `auth` | 인증 경계와 비로그인 보호 |
| `search` | 종목 검색 |
| `quote` | 시세/차트/종목 상세 |
| `responsive` | 반응형 |
| `slow` | 상대적으로 오래 걸리는 테스트 |
| `ui` | 브라우저 기반 UI 테스트 |

## 10. 실행 명령

BVT:

```bash
pytest -m bvt
```

BVT headed:

```bash
pytest -q tests -m bvt --browser chromium --headed
```

로그인:

```bash
pytest -m login
```

전체 테스트:

```bash
pytest
```

Allure:

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

## 11. 유지보수 규칙

- BVT/smoke 핵심 경로는 `skip`으로 숨기지 않습니다.
- 선택적 UI 또는 스테이징 의존 기능만 제한적으로 skip합니다.
- 검색 입력은 구체적인 search input locator를 사용합니다.
- 검색 결과 클릭은 링크/카드 등 조작 가능한 요소만 사용합니다.
- Page Object에는 assertion을 넣지 않습니다.
- assertion은 테스트 파일에 둡니다.
- 실시간 가격/순위 정확값은 검증하지 않습니다.
- 실패 증적을 항상 남깁니다.

## 12. 남은 과제

| 과제 | 필요 조건 |
|---|---|
| 실제 로그인 성공 | 스테이징 계정, 인증 우회, 고정 OTP |
| 로그아웃/세션 유지/세션 만료 | 인증 storage state, TTL 제어 |
| 관심종목 저장 성공 | 스테이징 계정, 데이터 초기화 API |
| 주문/거래 보호 심화 | 모의 계좌 또는 거래 차단 테스트 계정 |
| 네트워크 오류 UX | API mock 또는 fault injection |
| visual regression | baseline과 승인 정책 |
| DOM contract suite | data-testid 또는 접근성 role 계약 |
