# Tossinvest UI Tests

Python 3.11+, Playwright, pytest, Allure 기반 토스증권 공개 웹 UI 자동화 프로젝트입니다.

## Assumptions

- 기본 대상은 `https://www.tossinvest.com` 공개 웹입니다.
- 인증, 계좌, 주문, 관심종목 저장처럼 개인 상태가 필요한 기능은 운영 환경에서 기본 자동화하지 않습니다.
- 해당 기능은 스테이징 계정, 테스트 데이터, 인증 세션 주입 정책이 준비된 뒤 별도 suite로 확장합니다.

## Project Structure

```text
tossinvest-ui-tests/
├── .github/workflows/ui-tests.yml
├── config/settings.py
├── docs/test_strategy.md
├── pages/
│   ├── base_page.py
│   ├── home_page.py
│   ├── search_page.py
│   └── stock_detail_page.py
├── test_cases/tossinvest_public_cases.yaml
├── tests/
│   ├── conftest.py
│   ├── test_home.py
│   ├── test_responsive.py
│   ├── test_search.py
│   └── test_stock_detail.py
├── utils/
│   ├── artifacts.py
│   └── waits.py
├── .env.example
├── pyproject.toml
├── pytest.ini
└── README.md
```

- `config/`: 환경별 base URL, 브라우저, timeout, artifact 설정.
- `pages/`: Page Object Model. 행동과 locator 관리만 담당합니다.
- `tests/`: pytest 테스트. assertion은 이 계층에 둡니다.
- `utils/`: 공통 wait와 실패 증적 attachment.
- `test_cases/`: 사람이 읽고 자동 생성에도 쓸 수 있는 YAML 테스트 명세.
- `docs/`: 테스트 전략, 테스트 케이스 명세서, 유지보수 기준.
- `.github/workflows/`: PR smoke, main regression CI.

## Specification Documents

- Test strategy: `docs/test_strategy.md`
- Test case specification: `docs/test_case_specification.md`
- Test case source YAML: `test_cases/tossinvest_public_cases.yaml`

## Current BVT Status

- Total test cases in YAML: 60
- BVT candidate IDs in YAML: 33
- Automated BVT tests collected by pytest: 31
- Latest headed Chromium BVT result: `31 passed, 6 deselected`
- Login coverage included in BVT: public login entry, signin page options, QR login guidance, SMS login form, empty SMS auth request safety, browser back from signin, signup entry, unauthenticated account access guard.

The current BVT is sufficient for the public web surface. It does not prove a successful real user login, account access, logout, trading, or watchlist persistence. Those require a staging account, test identity data, and an authentication bypass or controlled OTP/app approval flow.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
playwright install --with-deps
cp .env.example .env
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
playwright install
Copy-Item .env.example .env
```

## Run Tests

전체 테스트:

```bash
pytest
```

Smoke만 실행:

```bash
pytest -m smoke
```

BVT만 실행:

```bash
pytest -m bvt
```

BVT를 실제 브라우저 창으로 실행:

```bash
pytest -q tests -m bvt --browser chromium --headed
```

특정 마커 실행:

```bash
pytest -m "search and not slow"
pytest -m responsive
pytest -m quote
pytest -m login
```

headed 실행:

```bash
pytest --headed
```

브라우저 변경:

```bash
BROWSER=firefox pytest -m regression
pytest --browser webkit -m smoke
```

병렬 실행:

```bash
pytest -n auto -m regression
```

Flaky 재시도:

```bash
pytest --reruns 1 --reruns-delay 1 -m smoke
```

## Allure

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

## Configuration

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
```

민감정보는 `.env`에만 두고 커밋하지 않습니다.

## Quality Rules

- locator는 role/text/placeholder 우선, CSS는 fallback으로만 사용합니다.
- 임의 sleep을 쓰지 않습니다.
- 시장 가격, 순위, 실시간 리스트 순서는 고정값으로 검증하지 않습니다.
- Page Object는 클릭/입력/이동 같은 행동만 담당합니다.
- assertion은 테스트 파일에 둡니다.
- 실패 시 screenshot, trace, video를 남깁니다.

## Maintenance

- 공개 DOM 변경으로 conditional 테스트가 skip되면 selector만 고치지 말고 실제 사용자 흐름 변경 여부를 확인합니다.
- 인증/거래 기능은 스테이징 계정과 테스트 데이터 초기화 API가 준비된 뒤 별도 marker로 분리합니다.
- 테스트 케이스 YAML의 `automation_status`가 `needs_mock_or_staging`인 항목은 mocking layer 또는 전용 환경이 준비될 때 자동화합니다.
