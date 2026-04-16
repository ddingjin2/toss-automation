# 토스증권 공개 웹 UI 자동화

토스증권 공개 웹(`https://www.tossinvest.com`)을 대상으로 하는 Python 기반 UI 자동화 프로젝트입니다.

이 프로젝트의 목적은 운영 공개 웹에서 안전하게 검증 가능한 범위의 BVT, smoke, regression 테스트를 제공하는 것입니다. 실제 로그인 성공, 계좌 접근, 거래, 관심종목 저장 같은 인증 후 기능은 스테이징 계정과 인증 제어 정책이 준비된 뒤 별도 suite로 확장합니다.

## 기술 스택

- 언어: Python 3.11+
- E2E 프레임워크: Playwright for Python
- 테스트 러너: pytest
- 리포트: Allure
- 설정 관리: pydantic-settings
- 패키징: pyproject.toml
- 코드 스타일: ruff, black
- CI: GitHub Actions

## 현재 상태

- 전체 테스트 케이스 명세: 60개
- BVT 후보 ID: 33개
- pytest 전체 자동화 테스트: 37개
- pytest BVT 자동화 테스트: 31개
- 최근 Chromium headed BVT 실행 결과: `31 passed, 6 deselected`
- 최근 Chromium 전체 suite 실행 결과: `37 passed`

## 자동화 범위

운영 공개 웹에서 자동화하는 범위:

- 홈 랜딩과 주요 네비게이션
- 검색 진입과 대표 종목 검색
- 공개 종목 상세 진입과 시세/차트 영역
- 실시간 차트, 지수, 시장 상태 노출
- 로그인 진입, 로그인 옵션, QR 안내, 문자 인증 폼
- 비로그인 내 계좌 진입 시 인증 유도
- 개인 계좌 정보 비노출
- 모바일/데스크톱 기본 렌더링
- 새로고침, 뒤로가기, 기본 로딩 안정성

운영 공개 웹에서 자동화하지 않는 범위:

- 실제 로그인 성공
- 로그아웃, 세션 유지, 세션 만료
- 실제 계좌 잔고/평가금액 검증
- 관심종목 저장 성공
- 주문/거래/체결
- OTP, 앱 승인, QR 승인 완료

위 영역은 스테이징 계정, 테스트 본인확인 데이터, 고정 OTP 또는 인증 우회, storage state 관리 정책이 필요합니다.

## 프로젝트 구조

```text
tossinvest-ui-tests/
├── .github/workflows/ui-tests.yml
├── config/
│   └── settings.py
├── docs/
│   ├── feedback_resolution.md
│   ├── test_case_specification.md
│   └── test_strategy.md
├── pages/
│   ├── base_page.py
│   ├── home_page.py
│   ├── login_page.py
│   ├── search_page.py
│   └── stock_detail_page.py
├── test_cases/
│   └── tossinvest_public_cases.yaml
├── tests/
│   ├── conftest.py
│   ├── test_bvt_extended.py
│   ├── test_home.py
│   ├── test_login.py
│   ├── test_responsive.py
│   ├── test_search.py
│   └── test_stock_detail.py
├── utils/
│   ├── artifacts.py
│   ├── assertions.py
│   └── waits.py
├── .env.example
├── pyproject.toml
├── pytest.ini
└── README.md
```

## 문서

- 테스트 전략: `docs/test_strategy.md`
- 테스트 케이스 명세: `docs/test_case_specification.md`
- 피드백 반영 내역: `docs/feedback_resolution.md`
- 테스트 케이스 원본 YAML: `test_cases/tossinvest_public_cases.yaml`

## 설치

Windows PowerShell:

```powershell
cd C:\dev\tossinvest-ui-tests
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
playwright install
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cd tossinvest-ui-tests
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
playwright install --with-deps
cp .env.example .env
```

## 실행 명령

전체 테스트:

```bash
pytest
```

BVT:

```bash
pytest -m bvt
```

BVT를 실제 브라우저 창으로 실행:

```bash
pytest -q tests -m bvt --browser chromium --headed
```

Smoke:

```bash
pytest -m smoke
```

Regression:

```bash
pytest -m regression
```

로그인 UX 테스트:

```bash
pytest -m login
```

검색 테스트:

```bash
pytest -m search
```

반응형 테스트:

```bash
pytest -m responsive
```

브라우저 지정:

```bash
pytest -m bvt --browser chromium
```

headed 모드:

```bash
pytest -m bvt --browser chromium --headed
```

병렬 실행:

```bash
pytest -n auto -m regression
```

재시도:

```bash
pytest --reruns 1 --reruns-delay 1 -m smoke
```

## Allure 리포트

결과 생성:

```bash
pytest --alluredir=allure-results
```

리포트 열기:

```bash
allure serve allure-results
```

정적 리포트 생성:

```bash
allure generate allure-results -o allure-report --clean
```

## 환경 변수

`.env`에서 변경합니다.

```env
BASE_URL=https://www.tossinvest.com
HEADLESS=true
BROWSER=chromium
VIEWPORT_WIDTH=1440
VIEWPORT_HEIGHT=900
TIMEOUT=10000
TRACE_ON_FAILURE=true
VIDEO_ON_FAILURE=true
DEFAULT_STOCK_QUERY=삼성전자
MOBILE_VIEWPORT_WIDTH=390
MOBILE_VIEWPORT_HEIGHT=844
```

민감정보는 `.env` 또는 CI secret으로만 관리하고 저장소에 커밋하지 않습니다.

## 품질 기준

- BVT/smoke 핵심 경로는 진입점이 사라지면 실패해야 합니다.
- 운영 공개 웹에서 선택적으로 노출되는 UI만 제한적으로 skip합니다.
- 검색 입력은 임의의 `input`으로 fallback하지 않습니다.
- 검색 결과 클릭은 링크/인터랙션 가능한 요소만 대상으로 합니다.
- Page Object는 행동과 locator만 담당하고 assertion은 테스트 파일에 둡니다.
- 임의 sleep을 사용하지 않습니다.
- 실시간 가격, 순위, 등락률 정확값은 assertion하지 않습니다.
- 실패 시 screenshot, trace, video, Allure attachment를 남깁니다.

## CI

GitHub Actions는 다음 흐름을 제공합니다.

- Pull Request: smoke 테스트 실행
- main push: regression 테스트 실행
- test-results, allure-results, failure artifacts 업로드
- Playwright 브라우저 캐시와 pip 캐시 사용

현재 main regression은 Chromium 중심입니다. Firefox/WebKit은 토스증권 공개 웹의 공식 지원 범위가 확인된 뒤 nightly 또는 lab suite로 분리하는 것이 안전합니다.
