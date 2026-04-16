# Toss Securities Public Web Test Strategy

## Assumptions

- Public URL: `https://www.tossinvest.com`.
- Publicly verifiable areas: home landing, navigation, feed/news entry, stock discovery, public search, public quote/chart surfaces, footer policy links, responsive rendering.
- Authentication/account-bound areas: account portfolio, watchlist persistence, order placement, trade confirmation, account-specific balances. These require staging data or a controlled authenticated session.
- Unknown or unstable details are marked as `conditional`, `needs_mock_or_staging`, or `manual_or_lab` in `test_cases/tossinvest_public_cases.yaml`.

## Scope

Automate:

- P0/P1 public critical path: landing, search entry, known stock search, stock detail reachability when publicly available, auth gate for account entry.
- Regression checks for public quote/chart containers, menu navigation, footer/compliance copy, responsive viewports.
- Negative checks that can be validated without sensitive state, such as no-result search and no full-page application error.
- Public login UX checks: login entry navigation, signin options, QR guidance, SMS auth form rendering, safe handling of empty auth requests, signup entry visibility, browser back from signin, and unauthenticated account guard.

Do not automate against production by default:

- Real order placement, account balances, real watchlist mutation, authenticated personal data.
- Pixel-perfect chart internals and real-time price exact values. Values are time-sensitive and brittle.
- CAPTCHA, device binding, OTP, and external app deep-link completion.
- Successful real login, logout, authenticated account access, session persistence, and post-login mutations unless a staging account plus controlled authentication flow is available.

## Risk-Based Priority

- P0: home availability, search entry, stock lookup, account/auth boundary.
- P0: public login entry, signin page availability, unauthenticated account guard, and private data non-exposure.
- P1: chart/filter rendering, responsive layout, known error handling, footer compliance, QR/SMS login guidance.
- P2: unsupported browser lab cases, broad accessibility audits, deep link edge cases.

## Suite Split

- Smoke: PR gate, public critical path only, under a few minutes.
- BVT: build verification gate for public web readiness. Current Chromium headed result is `31 passed, 6 deselected`.
- Regression: main branch or scheduled run, broader public UI coverage.
- Critical path: home -> search -> stock detail -> quote area; home -> account -> auth gate.
- Negative: unknown search, unsupported browser lab, network/API errors with mocks.
- Accessibility: keyboard traversal and basic accessible names first; axe integration later.
- Cross-browser: Chromium in PR; Firefox/WebKit in scheduled or nightly regression.

## Login Automation Scope

Production-safe login automation covers only public and non-sensitive behavior:

- Home login entry opens `/signin`.
- Signin page exposes Toss app, phone number, QR, terms, and signup entry.
- QR login guidance renders without application error.
- App-less SMS login form renders without application error.
- Empty SMS auth request fails safely or keeps the form stable.
- Browser back from signin restores the public home.
- Unauthenticated account entry routes to login/auth context.
- Private account data is not exposed before authentication.

Out of scope for production BVT:

- Successful login with real Toss app approval, SMS OTP, QR approval, device binding, or certificate flow.
- Authenticated account page assertions.
- Logout/session persistence/session expiry assertions.
- Watchlist persistence or trading workflows.

These require staging support: test account, test identity data, deterministic OTP or auth bypass, storage state lifecycle policy, and strict handling of sensitive artifacts.

## Flaky Prevention

- Use role/text-based locators first, CSS only as fallback.
- Do not fall back to arbitrary `input` elements or plain text clicks for core flows.
- Keep assertions in tests; keep Page Objects action-oriented.
- Do not assert exact market prices or list order.
- Do not use arbitrary sleeps. Wait for DOM readiness and specific visible UI.
- Isolate browser context per test.
- Attach screenshot, trace, and video on failure.
- BVT/smoke critical paths must fail when required entry points disappear.
- Mark only production-state dependent or optional public UI tests as conditional, skippable, or staging-required.

## Anti-Patterns

- Selecting by generated class names.
- Waiting with `time.sleep`.
- Asserting exact real-time prices.
- Sharing login/session state across unrelated tests.
- Mutating real user data in production.
- Encoding business assumptions in fixtures instead of test data.
