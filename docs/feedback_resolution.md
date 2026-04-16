# 피드백 반영 내역

이 문서는 리뷰 피드백 중 즉시 반영한 항목, 수용하되 보류한 항목, 현재 범위에서는 적용하지 않은 항목을 정리합니다.

## 1. 즉시 수용 및 반영

| 피드백 | 반영 내용 | 관련 파일 |
|---|---|---|
| BVT/smoke 핵심 경로가 `skip`으로 숨겨질 수 있다. | 검색, 계좌, 로그인, 네비게이션, 종목 상세 같은 BVT 핵심 경로는 진입점 부재 시 실패하도록 변경했습니다. | `tests/test_home.py`, `tests/test_search.py`, `tests/test_stock_detail.py`, `tests/test_bvt_extended.py`, `tests/test_login.py` |
| 검색 입력 locator가 너무 넓다. | 임의의 `input` fallback을 제거하고, 검색 전용 `input[type='search']`와 실제 공개 DOM의 `data-section-name='검색'` 조건을 사용했습니다. | `pages/home_page.py`, `pages/search_page.py` |
| 검색 결과 클릭이 단순 텍스트까지 허용한다. | 단순 텍스트 클릭 fallback을 제거했습니다. 검색 후 `/stocks/` URL 전환을 기다리는 로직도 추가했습니다. | `pages/search_page.py`, `pages/stock_detail_page.py` |
| wait helper가 후보별 누적 timeout으로 느리고 원인이 불명확하다. | locator union 기반으로 전체 timeout budget을 한 번만 사용하도록 변경했습니다. 실패 메시지에는 후보 개수와 timeout이 표시됩니다. | `utils/waits.py`, `pages/base_page.py` |
| 로딩 해소 테스트가 실제로 로딩 해소를 보장하지 않는다. | 로딩 문구가 보이면 사라질 때까지 기다린 뒤 최종 시장 콘텐츠가 표시되는지 확인하도록 변경했습니다. | `tests/test_stock_detail.py` |

## 2. 수용하지만 보류

| 피드백 | 보류 이유 | 후속 계획 |
|---|---|---|
| `conftest.py`를 fixture 모듈로 분리 | 현재 규모에서는 기계적 변경에 가깝고, 테스트 동작 개선 효과가 작습니다. | 인증 fixture, API seed fixture, 다중 브라우저 프로필이 생길 때 분리합니다. |
| 테스트 데이터 레이어 도입 | 우선순위가 더 높은 skip/locator/wait 문제를 먼저 해결했습니다. | `data/search_queries.yaml`과 typed loader를 추가해 검색 데이터 중복을 줄입니다. |
| suite 디렉터리 분리 | 현재 테스트 수에서는 파일 이동 비용이 더 큽니다. | DOM contract 또는 authenticated suite가 생길 때 `smoke/`, `regression/`, `contracts/`로 분리합니다. |
| console/network log 저장 | 현재 screenshot, trace, video, JUnit, Allure가 이미 있습니다. | CI 전용 장애가 반복되면 console/network capture를 추가합니다. |
| `contract`, `quarantine` marker 추가 | 아직 해당 suite가 없습니다. | 첫 DOM contract 또는 quarantine 대상이 생기면 추가합니다. |

## 3. 현재 범위에서는 적용하지 않음

| 피드백 | 결정 | 이유 |
|---|---|---|
| main regression을 Firefox/WebKit까지 즉시 확대 | 지금은 적용하지 않습니다. | 현재 토스증권 공개 웹은 Chrome/Edge 최신 버전 사용 안내가 노출됩니다. 공식 지원 범위 확인 전에는 lab/nightly로 분리하는 것이 안전합니다. |
| 모든 skip 제거 | 전면 적용하지 않습니다. | 관심종목 버튼처럼 비로그인 운영 공개 DOM에서 항상 보장되지 않는 UI는 선택적 검증입니다. BVT 핵심 경로만 실패로 전환했습니다. |
| 운영에서 실제 로그인 성공 자동화 | 적용하지 않습니다. | 토스 앱 승인, QR 승인, SMS/OTP, 본인확인 등 제어 불가능한 인증 단계가 필요합니다. 스테이징 계정과 인증 우회가 필요합니다. |

## 4. 검증 결과

정적 검증:

```text
ruff check tossinvest-ui-tests
All checks passed
```

```text
black --check tossinvest-ui-tests
20 files would be left unchanged
```

BVT:

```text
pytest -q tests -m bvt --browser chromium
31 passed, 6 deselected in 76.61s
```

전체 테스트:

```text
pytest -q tests --browser chromium
37 passed in 94.89s
```

## 5. 결론

이번 피드백 반영으로 BVT의 품질 신호가 더 강해졌습니다.

- 핵심 경로 부재가 skip으로 숨겨지지 않습니다.
- 검색 locator가 덜 모호해졌습니다.
- 검색 결과 클릭 오탐 가능성이 줄었습니다.
- wait helper의 최악 실행 시간이 줄었습니다.
- 로딩 테스트가 이름과 실제 검증에 더 가까워졌습니다.

아직 남은 구조 개선은 있습니다. 다만 현재 목적은 “토스증권 공개 웹 BVT와 초기 regression 기반”이므로, 대규모 구조 변경보다는 suite가 커지는 시점에 단계적으로 진행하는 것이 적절합니다.
