---
description: Generate Laravel tests with Pest following best practices
argument-hint: "[feature/controller/specific test description]"
---

# Laravel Testing with Pest

**Request:** $ARGUMENTS

## Before Writing Tests

- Use Laravel MCP `search_docs` if unsure about current syntax
- Identify test type: Feature (HTTP/database), Browser (Pest v4 + Playwright), or Unit (pure logic)

## Behavior

**Vague request** (e.g., "test TaskController"): Propose a test plan first covering happy path, validation, authorization, edge cases, and business rules. Wait for confirmation.

**Specific request** (e.g., "test users cannot cancel after 24 hours"): Write the test directly.

---

## Syntax Rules

- Always `it()`, never `test()`
- Always `expect()` over PHPUnit assertions
- Chain expectations on the same subject
- Test names as behavioral specs: `it('prevents duplicate votes on the same proposal')`
- Never generic names like `it('works')` or `it('returns 200')`

## Structure

- Follow Arrange-Act-Assert with clear separation
- Use `describe()` to group related tests
- Use `beforeEach()` for shared setup within describe blocks
- One behavioral concept per test (multiple assertions okay)

## Pest Features to Use

- **Chained expectations**: `expect($user)->name->toBe('X')->email->toEndWith('@example.com')`
- **Higher-order expectations**: `expect($users)->each->toBeInstanceOf(User::class)`
- **Negation**: `->not->toBeEmpty()`
- **Datasets**: `->with([...])` for parameterized tests, use named datasets for clarity
- **Hooks**: `beforeEach()`, `afterEach()` for setup/teardown
- Docs: search "Pest expectations", "Pest datasets", "Pest hooks"

---

## Feature/Integration Tests

- Use `actingAs()` for authentication
- Use `assertInertia()` for Inertia responses - verify component and props
- Use `assertDatabaseHas()`, `assertDatabaseCount()`, `assertModelExists()`
- If feature dispatches events → use `Event::fake()` and `Event::assertDispatched()`
- If feature sends notifications → use `Notification::fake()` and `Notification::assertSentTo()`
- If feature queues jobs → use `Queue::fake()` and `Queue::assertPushed()`
- If feature sends mail → use `Mail::fake()` and `Mail::assertSent()`
- Use factories with states for different scenarios
- Docs: search "Laravel HTTP tests", "Laravel database testing", "Laravel mocking"

## Browser Tests (Pest v4)

- Uses Playwright, NOT Dusk
- Install: `pestphp/pest-plugin-browser` + `playwright`
- Entry point: `visit('/path')` returns page object
- Interactions: `click()`, `type()`, `fill()`, `press()`, `select()`, `check()`, `radio()`, `attach()`, `hover()`, `drag()`
- Device simulation: `->on()->mobile()`, `->on()->iPhone14Pro()`
- Browser selection: `->firefox()`, `->safari()` or CLI `--browser firefox`
- Dark mode: `->inDarkMode()`
- Smoke testing: `assertNoSmoke()`, `assertNoJavaScriptErrors()`, `assertNoConsoleLogs()`, `assertNoAccessibilityIssues()`
- Visual regression: `assertScreenshotMatches()`
- Debugging: `->tinker()` for REPL, `->debug()` to pause, `->screenshot()`
- Run: `--headed` for visible browser, `--debug` to pause on failure, `--parallel` for speed
- Docs: search "Pest browser testing"

---

## File Organization

- `tests/Feature/` - HTTP and database tests, grouped by domain (Auth/, Tasks/, Api/)
- `tests/Browser/` - Browser tests for critical JS-dependent flows
- `tests/Unit/` - Pure logic tests
- `tests/Pest.php` - Configuration, traits, custom helpers

## Philosophy

- Test behavior, not implementation
- Test what would hurt if it broke
- Focus on: state transitions, authorization boundaries, business rules, validation
- Use factories religiously - never manually create models
- Don't mock what you don't own
- Don't test Laravel framework internals

## Coverage Checklist

For any feature, verify:
- [ ] Happy path
- [ ] Unauthenticated → redirect/401
- [ ] Unauthorized → 403
- [ ] Invalid input → validation errors
- [ ] Resource not found → 404
- [ ] Duplicate/conflicting actions handled
- [ ] Business rule boundaries enforced
- [ ] Edge cases: empty arrays, null values, zero quantities, boundary values, max lengths, special characters, concurrent requests