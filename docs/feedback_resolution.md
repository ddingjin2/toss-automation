# Feedback Resolution

This document records which review feedback was accepted immediately, which items are accepted but deferred, and which items are intentionally not applied to the current public-web BVT scope.

## Accepted And Fixed

| Feedback | Resolution | Files |
|---|---|---|
| BVT/smoke core paths should fail instead of `skip` when a required entry point disappears. | Converted BVT-critical search, account, login, navigation, and stock-detail paths from `pytest.skip` to assertions. Optional watchlist/favorite UI remains skippable because it is not guaranteed on the public unauthenticated surface. | `tests/test_home.py`, `tests/test_search.py`, `tests/test_stock_detail.py`, `tests/test_bvt_extended.py`, `tests/test_login.py` |
| Search input locator is too broad because it falls back to any `input`. | Removed generic `input` fallback. Search now targets semantic search controls and the observed Toss search field attributes: `input[type='search'][data-section-name='검색']` and `input[type='search'][placeholder*='검색']`. | `pages/home_page.py`, `pages/search_page.py` |
| Search result click fallback should not click arbitrary text. | Removed plain text click fallback from result opening. Stock detail navigation now also waits for `/stocks/` URL after Enter, which matches the current public behavior. | `pages/search_page.py`, `pages/stock_detail_page.py` |
| `wait_for_any_visible` uses cumulative timeout and gives weak failure signal. | Reworked it to build a visible locator union and wait once with a total timeout budget. Failure messages now include candidate count and timeout. | `utils/waits.py`, `pages/base_page.py` |
| Loading resolve test allowed loading text as a passing condition. | Updated the test to wait for visible loading text to disappear if it appears, then require final market content. | `tests/test_stock_detail.py` |

## Accepted But Deferred

| Feedback | Reason For Deferral | Intended Follow-Up |
|---|---|---|
| Split `conftest.py` into fixture modules. | Current fixture file is still small enough, and splitting now would mostly be mechanical churn. | Split when authenticated fixtures, API seed fixtures, or multiple browser profiles are added. |
| Add data layer for stock aliases and no-result query. | Useful, but current high-risk issues were locator and skip policy. | Add `data/search_queries.yaml` plus typed loader before increasing search/quote coverage. |
| Separate tests by `smoke/`, `regression/`, `contracts/` folders. | Current file count is still manageable. Moving files now would create path churn without changing behavior. | Reorganize when test count crosses a practical threshold or when DOM contract tests are introduced. |
| Add browser console/network logs to artifacts. | Screenshot, trace, video, JUnit, and Allure are already available. | Add console/network capture when diagnosing recurrent CI-only failures. |
| Add `contract` and `quarantine` markers. | Good policy, but no quarantined or DOM-contract suite exists yet. | Add with first contract/quarantine tests. |

## Not Applied To Current Scope

| Feedback | Decision | Rationale |
|---|---|---|
| Run main regression on Firefox/WebKit immediately. | Not applied now. | Toss public web explicitly guides users toward Chrome/Edge in the current UI. Cross-browser testing should be lab/nightly after support policy is confirmed, not a blocking main regression gate. |
| Remove all skips everywhere. | Not applied globally. | Optional or staging-dependent public UI, such as watchlist/favorite controls, may not exist for unauthenticated production users. Those skips preserve truthful scope boundaries. BVT-critical paths now fail. |
| Automate successful real login in production. | Not applied. | Real login requires Toss app approval, QR/SMS/identity controls, or a staging auth bypass. Production BVT should only verify public login UX and private data non-exposure. |

## Validation After Fix

```text
ruff check tossinvest-ui-tests
All checks passed

black --check tossinvest-ui-tests
20 files would be left unchanged

pytest -q tests -m bvt --browser chromium
31 passed, 6 deselected in 76.61s

pytest -q tests --browser chromium
37 passed in 94.89s
```
