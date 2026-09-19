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

## 6. 2차 리뷰 반영 내역

2차 리뷰에서 지적된 항목은 운영 신호에 직접 영향을 주는 항목과 구조 확장 항목으로 나누어 처리했습니다.

### 즉시 수용 및 반영

| 피드백 | 반영 내용 | 관련 파일 |
|---|---|---|
| 선택적 공개 UI와 핵심 회귀의 경계가 불명확하다. | 공개 비로그인 세션에서 항상 보장되지 않는 UI는 `optional_public_ui` marker로 격리했습니다. BVT/Smoke 핵심 경로는 계속 실패로 처리합니다. | `pytest.ini`, `tests/test_home.py`, `tests/test_stock_detail.py` |
| `pyproject.toml`과 `pytest.ini`에 pytest 설정이 중복되어 있다. | pytest 설정은 `pytest.ini`로 단일화하고, `pyproject.toml`에는 패키징/format/lint 설정만 남겼습니다. | `pyproject.toml`, `pytest.ini` |
| 실패 분석 정보가 screenshot/trace/video 중심이다. | 실패 시 브라우저 console log를 `artifacts/console/`에 저장하고 Allure에 첨부하도록 추가했습니다. | `tests/conftest.py` |
| 공개 웹 한글 오류 카피를 놓칠 수 있다. | 공통 public error assertion에 한글 오류 패턴을 추가했습니다. | `utils/assertions.py` |
| `TI-WEB-051`은 이름은 clickable인데 실제 클릭하지 않는다. | 홈, 피드, 주식 골라보기 공개 네비게이션은 실제 클릭 후 body 표시와 오류 미노출을 검증하도록 변경했습니다. 계좌 메뉴는 인증 경계이므로 별도 로그인/BVT 테스트에서 다룹니다. | `tests/test_bvt_extended.py` |
| `test_bvt_extended.py` 내부 공통 assertion 중복이 있다. | public error, private account data, text visibility assertion을 `utils/assertions.py` 공통 helper로 재사용하도록 정리했습니다. | `tests/test_bvt_extended.py`, `utils/assertions.py` |
| CI에서 외부 사이트 상태와 테스트 실패 구분이 약하다. | smoke/regression 실행 전 공개 사이트 health check step을 추가했습니다. | `.github/workflows/ui-tests.yml` |
| `pytest -n auto`는 runner 자원 변동성을 키울 수 있다. | main regression 병렬 실행을 `-n 2`로 고정했습니다. | `.github/workflows/ui-tests.yml` |

### 보류 또는 단계적 반영

| 피드백 | 결정 | 이유 |
|---|---|---|
| `tests/smoke`, `tests/bvt`, `tests/regression` 디렉터리로 즉시 재구성 | 보류 | 현재 37개 규모에서는 파일 이동 비용이 검증 이득보다 큽니다. 테스트 수가 70개 이상이 되거나 authenticated suite가 들어올 때 분리합니다. |
| Firefox/WebKit regression 즉시 추가 | 보류 | 현재 공개 사이트 안내와 운영 기준은 Chrome/Edge 중심입니다. Chromium 안정화 후 nightly/lab job으로 먼저 추가하는 것이 안전합니다. |
| YAML 명세 기반 pytest generator 도입 | 보류 | 현재는 `allure.story`로 명세 ID 추적을 우선 유지합니다. generator는 데이터 기반 반복 테스트가 늘어나는 시점에 도입합니다. |
| 모든 텍스트 locator 제거 | 부분 보류 | 공개 웹에 `data-testid` 계약이 없으므로 완전 제거는 불가능합니다. 다만 검색 입력과 결과 클릭처럼 오탐 위험이 큰 locator는 이미 축소했고, 앞으로 DOM contract를 확보하면 추가 전환합니다. |
| `conftest.py` fixture 모듈 즉시 분리 | 보류 | console artifact 추가 후에도 파일 크기는 관리 가능한 수준입니다. storage state, auth session, network logging fixture가 추가될 때 분리합니다. |

### 최신 검증 결과

정적 검사:

```text
ruff check tossinvest-ui-tests
All checks passed
```

```text
black --check tossinvest-ui-tests
20 files would be left unchanged
```

BVT collection:

```text
pytest --collect-only -q tossinvest-ui-tests\tests -m bvt
31/37 tests collected (6 deselected)
```

BVT 실제 브라우저 실행:

```text
pytest -q tests -m bvt --browser chromium
31 passed, 6 deselected in 86.89s
```

전체 suite 실제 브라우저 실행:

```text
pytest -q tests --browser chromium
37 passed in 96.69s
```

크레딧 소진전 마지막 대화내역

• 전부 수정할 필요는 없습니다. 현재 로컬 main 기준으로 보면 리뷰 중 일부는 이미 반영됐고, 일부는 지금 당장 고칠 항목
  | SearchPage.result_matching() 텍스트 기반 locator | 수정 권장 | 아직 단순 get_by_text()라 검색 결과 “항목”이 아니
  라 텍스트 노출만으로 통과할 수 있습니다. /C:/dev/projects/tossinvest-ui-tests/pages/search_page.py:34 |
  |---|---|
  | optional_public_ui marker 일관 적용 | skip이 남은 공개 선택 UI 테스트 2개에 이미 붙어 있습니다. /C:/dev/
  tossinvest-ui-tests/tests/test_home.py:59, /C:/dev/projects/tossinvest-ui-tests/tests/test_stock_detail.py:50 |
  | BasePage.first_visible() 순차 대기 | 이미 wait_for_any_visible() 기반입니다. 리뷰 지적은 현재 코드 기준으로는 오
  래된 내용입니다. /C:/dev/projects/tossinvest-ui-tests/pages/base_page.py:42 |
  | 실패 시 console log 수집 | 이미 page.on("console")로 수집하고 실패 시 Allure에 attach합니다. /C:/dev/tossinvest-
  ui-tests/tests/conftest.py:87 |
  | CI 병렬 -n auto | 이미 -n 2로 고정돼 있습니다. /C:/dev/projects/tossinvest-ui-tests/.github/workflows/ui-tests.yml:120 |
  | health check | 이미 smoke/regression 전에 있습니다. /C:/dev/projects/tossinvest-ui-tests/.github/workflows/ui-
  tests.yml:37, /C:/dev/projects/tossinvest-ui-tests/.github/workflows/ui-tests.yml:107 |

  당장 안 해도 됨
  | 항목 | 판단 |
  |---|---|
  | conftest.py fixture 분리 | 아직 필수는 아닙니다. auth session, storage state, network log fixture가 들어갈 때 분
  리하는 게 낫습니다. |
  | tests/smoke, tests/bvt, tests/regression 물리 디렉터리 재구성 | 지금 37개 규모에서는 이동 비용이 큽니다. 테스트
  가 더 늘거나 authenticated suite가 생길 때 하는 게 맞습니다. |
  | Chromium + WebKit/Firefox matrix | 공개 서비스 지원 정책과 CI 비용을 감안하면 nightly/lab job부터 추가하는 게 현
  실적입니다. main gate에 바로 넣을 필요는 낮습니다. |
  | 모든 텍스트 locator 제거 | 서비스 DOM에 data-testid 계약이 없어서 전면 제거는 어렵습니다. 오탐 위험 큰 검색 결
  과/클릭 경로부터 줄이는 방식이 맞습니다. |
  | YAML 기반 generator | 지금은 allure.story 매핑으로 충분합니다. 데이터 반복 케이스가 늘 때 도입하면 됩니다. |

  결론: 전부 수정 대상은 아니고, 지금 바로 손볼 만한 건 3개입니다.

  1. SearchPage.result_matching()를 link/card 기반으로 좁히기
  2. 대표 종목 검색 중복을 BVT/기능 테스트 중 하나로 정리하거나 helper로 통합하기
  3. feedback_resolution.md의 console/network 관련 stale 문구 정리하기