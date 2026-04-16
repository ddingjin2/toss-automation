# Tossinvest Public Web Test Case Specification

## 1. Purpose

이 문서는 토스증권 공개 웹 UI 자동화의 테스트 케이스 명세서다.

대상은 `https://www.tossinvest.com`에서 비로그인 사용자도 접근 가능한 공개 영역이며, 인증/계좌/거래/관심종목 저장처럼 개인 상태가 필요한 기능은 운영 자동화 대상에서 제외하거나 스테이징 필요 항목으로 분리한다.

## 2. Assumptions

| 구분 | 내용 | 자동화 판단 |
|---|---|---|
| 공개 홈 | 홈, 피드, 주식 골라보기, 내 계좌 진입점, 검색 진입점 | 자동화 |
| 시장 정보 | 지수, 실시간 차트, 카테고리, 투자자 동향 | 자동화 |
| 종목 검색 | 공개 검색 입력 및 검색 결과 | 자동화 |
| 종목 상세 | 검색 결과에서 접근 가능한 상세/시세/차트 영역 | 조건부 자동화 |
| 내 계좌 | 비로그인 상태의 인증 유도 UX | 자동화 |
| 관심종목 | 저장 동작은 인증/계좌 상태 필요 가능성 높음 | 스테이징 필요 |
| 주문/거래 | 실거래 및 계좌 상태 필요 | 운영 자동화 제외 |
| 네트워크 오류 | API 지연/오류 재현 필요 | mock 또는 스테이징 필요 |

## 3. Test Case Format

테스트 케이스 원본은 YAML로 관리한다.

파일: `test_cases/tossinvest_public_cases.yaml`

YAML을 선택한 이유:

- 사람이 리뷰하기 쉽다.
- `steps`, `tags`, `data` 같은 중첩 구조를 자연스럽게 표현한다.
- 이후 pytest parameter generator 입력으로 재사용하기 쉽다.
- Markdown 표보다 자동 처리에 유리하고, JSON보다 사람이 수정하기 쉽다.

필수 필드:

| 필드 | 설명 | 예시 |
|---|---|---|
| `id` | 테스트 케이스 고유 ID | `TI-WEB-001` |
| `title` | 케이스 제목 | `홈 랜딩 공개 셸 로딩` |
| `precondition` | 사전 조건 | `사용자는 비로그인 상태다.` |
| `steps` | 실행 절차 | `홈에 접속한다.` |
| `expected_result` | 기대 결과 | `검색 진입점이 표시된다.` |
| `priority` | 우선순위 | `P0`, `P1`, `P2` |
| `tags` | 기능/성격 태그 | `[home, smoke, ui]` |
| `data` | 입력 데이터 | `{ query: "삼성전자" }` |
| `smoke` | smoke suite 포함 여부 | `true` |
| `regression` | regression suite 포함 여부 | `true` |

추가 관리 필드:

| 필드 | 설명 |
|---|---|
| `automation_status` | `ready`, `conditional`, `staging_required`, `needs_mock_or_staging`, `manual_or_lab` |

## 4. Test Suite Definition

| Suite | 목적 | 실행 시점 | 포함 기준 |
|---|---|---|---|
| Smoke | PR gate용 핵심 경로 검증 | Pull Request | 홈, 검색 진입, 계좌 인증 유도, 모바일 기본 렌더링 |
| BVT | 새 빌드가 regression 진입 가능한지 빠르게 판정 | 배포 직후, PR merge 전, release candidate | 공개 critical path, 인증 게이트, 기본 시장 데이터, 모바일/데스크톱 렌더링 |
| Regression | 공개 UI 회귀 검증 | main push, nightly | smoke 외 공개 기능, 필터, 푸터, 상세, 오류 없음 |
| Critical Path | 사용자 핵심 흐름 검증 | smoke/regression 공통 | 홈 -> 검색 -> 종목 상세, 홈 -> 내 계좌 -> 인증 유도 |
| Negative | 예외 UX 검증 | regression | 없는 종목 검색, API 오류, 미지원 브라우저 |
| Accessibility | 접근성 기본 검증 | regression 또는 nightly | 키보드 이동, accessible name |
| Cross-browser | 브라우저 호환성 | nightly 권장 | Chromium 기본, Firefox/WebKit 확장 |

## 4.1 BVT Completion Criteria

BVT 완료라고 말하려면 아래 조건을 모두 만족해야 한다.

| 기준 | 완료 조건 |
|---|---|
| 대상 확정 | `test_cases/tossinvest_public_cases.yaml`의 `bvt_suite.candidate_ids`가 review로 승인되어 있다. |
| 자동화 매핑 | `ready` BVT 케이스가 pytest marker `bvt` 또는 `smoke`로 자동 실행된다. |
| 실행 결과 | 최신 빌드에서 ready BVT 케이스가 100% pass다. |
| 조건부 처리 | `conditional` BVT 케이스는 공개 DOM 제한으로 skip되거나 스테이징에서 pass해야 한다. |
| 증적 | Allure, screenshot, trace, test result artifact가 남는다. |
| CI 연결 | PR 또는 배포 전 pipeline에서 BVT가 자동 실행된다. |

## 5. Test Case Summary

| ID | Title | Priority | Tags | Smoke | Regression | Status |
|---|---|---|---|---|---|---|
| TI-WEB-001 | 홈 랜딩 공개 셸 로딩 | P0 | home, landing, ui | Y | Y | ready |
| TI-WEB-002 | 홈 투자 유의 문구 노출 | P1 | home, compliance, footer | N | Y | ready |
| TI-WEB-003 | 홈 실시간 차트 필터 전환 | P1 | home, chart, quote | N | Y | ready |
| TI-WEB-004 | 피드 메뉴 이동 | P1 | navigation, feed | N | Y | ready |
| TI-WEB-005 | 주식 골라보기 메뉴 이동 | P1 | navigation, discovery | Y | Y | ready |
| TI-WEB-006 | 내 계좌 진입 시 인증 유도 | P0 | auth, account, security | Y | Y | ready |
| TI-WEB-007 | 검색 진입점 클릭 | P0 | search, ui | Y | Y | ready |
| TI-WEB-008 | 국내 종목명 검색 | P0 | search, domestic | Y | Y | ready |
| TI-WEB-009 | 해외 종목명 검색 | P1 | search, us-stock | N | Y | ready |
| TI-WEB-010 | 존재하지 않는 종목 검색 | P1 | search, negative | N | Y | ready |
| TI-WEB-011 | 검색 결과에서 종목 상세 진입 | P0 | search, stock-detail, quote | Y | Y | conditional |
| TI-WEB-012 | 종목 상세 시세 영역 노출 | P0 | stock-detail, quote | Y | Y | conditional |
| TI-WEB-013 | 종목 상세 차트 기간 선택 | P1 | stock-detail, chart | N | Y | conditional |
| TI-WEB-014 | 관심종목 추가 비로그인 인증 유도 | P1 | watchlist, auth | N | Y | staging_required |
| TI-WEB-015 | 주문/거래 CTA 비로그인 보호 | P0 | trade, auth, security | N | Y | staging_required |
| TI-WEB-016 | 모바일 홈 반응형 렌더링 | P0 | responsive, mobile | Y | Y | ready |
| TI-WEB-017 | 데스크톱 홈 반응형 렌더링 | P1 | responsive, desktop | N | Y | ready |
| TI-WEB-018 | 지원하지 않는 브라우저 안내 | P2 | compatibility, negative | N | N | manual_or_lab |
| TI-WEB-019 | 네트워크 지연 중 로딩 처리 | P1 | loading, network | N | Y | needs_mock_or_staging |
| TI-WEB-020 | 시장 데이터 API 오류 메시지 | P1 | error, network, negative | N | Y | needs_mock_or_staging |
| TI-WEB-021 | 주요 링크 키보드 접근 | P1 | accessibility, keyboard | N | Y | ready |
| TI-WEB-022 | 이미지 대체 텍스트 기본 접근성 | P2 | accessibility | N | Y | ready |
| TI-WEB-023 | 새로고침 후 홈 상태 복원 | P1 | home, reliability | N | Y | ready |
| TI-WEB-024 | 공개 정책 링크 이동 | P2 | footer, compliance, navigation | N | Y | ready |
| TI-WEB-025 | 검색 입력값 초기화 | P1 | search, usability | N | Y | ready |
| TI-WEB-026 | 슬래시 키 검색 단축키 | P1 | search, keyboard, accessibility | N | Y | ready |
| TI-WEB-027 | 검색 결과 키보드 선택 | P1 | search, keyboard, accessibility | N | Y | conditional |
| TI-WEB-028 | 모든 지수 목록 진입 | P1 | home, index, navigation | N | Y | ready |
| TI-WEB-029 | 시장 상태 배지 노출 | P1 | home, market-status | N | Y | ready |
| TI-WEB-030 | 지금 뜨는 카테고리 상세 진입 | P1 | home, category, navigation | N | Y | conditional |
| TI-WEB-031 | 국내 투자자 동향 탭 전환 | P1 | home, investor-trend, quote | N | Y | ready |
| TI-WEB-032 | 피드 콘텐츠 상세 진입 | P1 | feed, news, navigation | N | Y | conditional |
| TI-WEB-033 | 주식 골라보기 조건 변경 | P1 | stock-picker, filter, discovery | N | Y | conditional |
| TI-WEB-034 | 푸터 고객센터 링크 접근 | P2 | footer, customer-support, navigation | N | Y | ready |
| TI-WEB-035 | 태블릿 뷰포트 홈 렌더링 | P1 | responsive, tablet | N | Y | ready |
| TI-WEB-036 | 브라우저 뒤로가기 상태 복원 | P1 | navigation, reliability | N | Y | ready |
| TI-WEB-037 | BVT 홈 최초 진입 10초 이내 안정화 | P0 | bvt, home, availability | Y | Y | ready |
| TI-WEB-038 | BVT 홈 전체 앱 오류 미노출 | P0 | bvt, home, error | Y | Y | ready |
| TI-WEB-039 | BVT 검색 입력 포커스 및 입력 가능성 | P0 | bvt, search, keyboard | Y | Y | ready |
| TI-WEB-040 | BVT 검색 결과 기본 응답 | P0 | bvt, search, domestic | Y | Y | ready |
| TI-WEB-041 | BVT 내 계좌 개인 정보 비노출 | P0 | bvt, auth, account, security | Y | Y | ready |
| TI-WEB-042 | BVT 실시간 차트 기본 목록 노출 | P0 | bvt, quote, chart, home | Y | Y | ready |
| TI-WEB-043 | BVT 시장 상태와 지수 요약 노출 | P0 | bvt, market-status, index | Y | Y | ready |
| TI-WEB-044 | BVT 모바일 홈 핵심 콘텐츠 렌더링 | P0 | bvt, responsive, mobile | Y | Y | ready |
| TI-WEB-045 | BVT 네비게이션 왕복 | P0 | bvt, navigation, reliability | Y | Y | ready |
| TI-WEB-046 | BVT 푸터 컴플라이언스 문구 노출 | P1 | bvt, footer, compliance | N | Y | ready |
| TI-WEB-047 | BVT 없는 종목 검색의 안전한 실패 | P1 | bvt, search, negative | N | Y | ready |
| TI-WEB-048 | BVT 종목 상세 진입 후 오류 미노출 | P0 | bvt, stock-detail, quote | Y | Y | conditional |
| TI-WEB-049 | BVT 새로고침 후 홈 복구 | P1 | bvt, home, reliability | N | Y | ready |
| TI-WEB-050 | BVT 데스크톱 기본 뷰포트 렌더링 | P1 | bvt, responsive, desktop | N | Y | ready |
| TI-WEB-051 | BVT 주요 메뉴 클릭 가능성 | P1 | bvt, navigation, accessibility | N | Y | ready |
| TI-WEB-052 | BVT 초기 로드 중 로딩 상태 이탈 | P1 | bvt, loading, reliability | N | Y | ready |
| TI-WEB-053 | BVT 홈 로그인 진입점에서 로그인 페이지 이동 | P0 | bvt, login, auth, navigation | Y | Y | ready |
| TI-WEB-054 | BVT 로그인 페이지 기본 옵션 노출 | P0 | bvt, login, auth | Y | Y | ready |
| TI-WEB-055 | BVT QR 로그인 안내 노출 | P1 | bvt, login, auth, qr | N | Y | ready |
| TI-WEB-056 | BVT 토스 앱 없이 문자 인증 로그인 폼 노출 | P1 | bvt, login, auth, sms | N | Y | ready |
| TI-WEB-057 | BVT 빈 문자 인증 요청 안전 처리 | P1 | bvt, login, auth, negative | N | Y | ready |
| TI-WEB-058 | BVT 로그인 페이지에서 뒤로가기 홈 복귀 | P0 | bvt, login, navigation, reliability | Y | Y | ready |
| TI-WEB-059 | BVT 로그인 페이지 가입하기 진입점 노출 | P1 | bvt, login, signup | N | Y | ready |
| TI-WEB-060 | BVT 비로그인 내 계좌 진입 시 로그인 컨텍스트 유도 | P0 | bvt, login, auth, account, security | Y | Y | ready |

## 6. Automation Mapping

| Test File | Covered Areas |
|---|---|
| `tests/test_home.py` | 홈 랜딩, 푸터, 내 계좌 인증 유도, 실시간 차트 필터 |
| `tests/test_search.py` | 검색 진입, 국내 종목 검색, 없는 종목 검색 |
| `tests/test_stock_detail.py` | 검색 기반 상세 진입, 시세/차트 영역, 관심종목 인증 유도, 로딩 오류 없음 |
| `tests/test_responsive.py` | 모바일/데스크톱 뷰포트 렌더링 |
| `tests/test_bvt_extended.py` | BVT 홈 가용성, 시장/지수, 검색, 차트, 네비게이션, 새로고침, 로딩 안정성 |
| `tests/test_login.py` | 로그인 진입, 로그인 옵션, QR 안내, 문자 인증 폼, 빈 요청 안전성, 가입 진입점, 비로그인 계좌 보호 |

## 7. Marker Mapping

| Marker | 용도 |
|---|---|
| `bvt` | 빌드가 regression에 진입 가능한지 판정하는 공개 웹 BVT |
| `auth` | 인증 경계와 비로그인 보호 검증 |
| `login` | 공개 로그인 진입 및 로그인 안내 UX 검증 |
| `smoke` | PR마다 실행할 핵심 경로 |
| `regression` | main push 또는 nightly 회귀 검증 |
| `slow` | 일반 UI 테스트보다 오래 걸리는 항목 |
| `ui` | 브라우저 기반 UI 테스트 |
| `search` | 종목 검색 관련 테스트 |
| `quote` | 시세, 차트, 종목 상세 관련 테스트 |
| `responsive` | viewport 반응형 테스트 |

## 8. Execution Commands

Smoke:

```bash
pytest -m smoke
```

BVT:

```bash
pytest -m bvt
pytest -q tests -m bvt --browser chromium --headed
```

Regression:

```bash
pytest -m regression
```

Login:

```bash
pytest -m login
```

Search only:

```bash
pytest -m search
```

Responsive only:

```bash
pytest -m responsive
```

Allure result:

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

## 9. Maintenance Rules

- Page Object는 locator와 사용자 행동만 담당한다.
- assertion은 테스트 파일에 둔다.
- generated class selector는 사용하지 않는다.
- `time.sleep`은 사용하지 않는다.
- 실시간 가격, 순위, 등락률의 정확값을 assertion하지 않는다.
- 인증/거래/계좌 상태가 필요한 테스트는 운영 smoke에 넣지 않는다.
- 실패 증적은 screenshot, trace, video, Allure attachment로 남긴다.

## 10. Open Items

| 항목 | 필요한 조건 |
|---|---|
| 실제 로그인 성공 검증 | 스테이징 계정, 테스트 본인확인 데이터, 고정 OTP 또는 인증 우회, storage state 관리 정책 |
| 로그아웃/세션 유지/세션 만료 | 인증된 storage state, 세션 TTL 제어, 민감 artifact 마스킹 |
| 관심종목 저장 검증 | 스테이징 계정, 테스트 데이터 초기화 정책 |
| 주문 CTA 보호 심화 검증 | 거래 불가 테스트 계좌 또는 mock 환경 |
| 네트워크 지연/오류 UX | API route mocking 또는 스테이징 fault injection |
| 접근성 심화 검사 | axe 연동 및 기준 위반 허용 정책 |
| visual regression | baseline 저장소와 diff 승인 프로세스 |
