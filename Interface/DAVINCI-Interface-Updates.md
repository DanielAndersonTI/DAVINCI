# DAVINCI Interface Updates

Working specification and final acceptance checklist for the usability additions to
the DAVINCI Architect web interface.

- Status: implemented and verified on 2026-11-23. See the verification record in
  section 15.
- Scope: `Interface/` only. The pipeline under `Experimento_Multiagente/` must keep
  working unchanged.
- Language: every string, comment, test name, and document added to the repository
  is written in English.
- Purpose of this file: at the end of the implementation, every box below is
  checked against the running system. A requirement is complete only when its
  item here is verified, not when the code merely exists.

---

## 1. Pipeline configuration selector

### Requirements

- [x] The main page offers a selector with **C0, C1, C2, C3, C4, C5**.
- [x] Default on first load or missing settings: **C1** (the complete pipeline).
- [x] C5 is listed as a control condition. Its description states that, without a
      frozen run directory, it regenerates the proposals like C1 and runs Agent 3
      twice, so it costs more.
- [x] Each option shows a short label and a one-line purpose.
- [x] The selected configuration persists on the server and survives a server
      restart and a page reload.
- [x] The choice changes only when the user explicitly confirms a new choice.
      It is not reset by `NEW DECOMPOSITION`, by a completed run, or by a reload.
- [x] The results page exposes the same selector, so a new run can use another
      configuration without going back to the form.
- [x] `RUN AGAIN` uses the configuration active at the moment of the click, not a
      value captured before.
- [x] The selector is disabled while a run is in progress.
- [x] The selector opens an in-page menu. No page reload occurs, so data already
      typed into the system inputs is preserved.

### Confirmation flow

- [x] Clicking a configuration opens the menu without changing the active value.
- [x] Clicking outside the menu opens a confirmation popup.
- [x] Confirming saves the new value, applies it, and closes the popup.
- [x] Discarding closes the popup and restores the previous value on screen.
- [x] Without confirmation, nothing is saved and nothing changes.
- [x] The popup follows the DAVINCI visual identity: navy, gold, square corners,
      uppercase labels, responsive at phone width.

---

## 2. AI provider selector

### Requirements

- [x] The interface offers three providers: **DeepSeek**, **Gemini**, **Claude**.
- [x] Default on first load or missing settings: **DeepSeek**.
- [x] The user chooses only the provider. The model is not selectable and uses the
      existing defaults:
  - DeepSeek: `deepseek-chat`
  - Gemini: `gemini-flash-latest`
  - Claude: `claude-sonnet-4-5-20250929`
- [x] The provider choice persists on the server, like the configuration.
- [x] The run executed after confirmation uses the selected provider.
- [x] Switching provider requires no change to the pipeline source. The server
      sets the provider environment variables before each run; `criar_llm()` reads
      them on every call and `load_dotenv` does not override values already set.
- [x] The interface shows, for the selected provider, whether a key is
      configured. It does not show the key.
- [x] If the selected provider has no key, the interface blocks the run with a
      clear message instead of starting a request that fails at the LLM call.
- [x] Providers that are not selected stay inert. Their keys do not have to be
      valid for the system to run.

### Confirmation flow

- [x] Same behavior as the configuration selector: in-page menu, no reload,
      confirmation popup on click outside, discard restores the previous value.
- [x] The provider becomes active only after the popup is confirmed.

---

## 3. API key management

### Storage model

- [x] Keys live in a single file, `Experimento_Multiagente/.env`, which is already
      ignored by Git. Keys are not duplicated in any other file.
- [x] `Interface/settings.json` stores only configuration, provider, and which key
      number is active per provider. It never stores a key value.
- [x] The key that exists today for a provider becomes **Key 1** of that provider.
      New keys are numbered sequentially: Key 2, Key 3, and so on.
- [x] Adding a new key does not delete the previous one. The previous key stays in
      the `.env` file as an inactive commented line, with provider and number.
- [x] The active line used by the pipeline is rewritten to point to the selected
      key. Only one active key per provider exists at a time.

### Add-key panel

- [x] Clicking a provider opens, below it, an optional panel to add a new key for
      that provider.
- [x] The panel contains a password field and a **`SAVE KEY`** button. Nothing is
      written until the button is clicked.
- [x] The panel can be left empty. In that case the key already registered for the
      provider is used.
- [x] The panel contains an optional checkbox, in English, labeled
      **`Set as the active key for this AI`**. Checked, the new key becomes active;
      unchecked, the key is only registered and the current active key remains.
- [x] Saving validates that the field is not empty and that the target provider is
      one of the three supported providers.
- [x] After saving, the field is cleared and the panel shows the new key as
      available, without revealing any part of its value.

### Key selection

- [x] When a provider has more than one registered key, selecting that provider
      also requires choosing the key.
- [x] The key selector lists labels only, such as `Key 1` and `Key 2`.
- [x] The chosen key number persists per provider.
- [x] Provider and key are confirmed together by the same popup when the panel is
      closed.

---

## 4. Security requirements

These are blocking. Any failure here blocks delivery, regardless of usability.

- [x] No key value ever appears in an HTTP response.
- [x] No key value is written to the DOM after saving: not in text, attributes,
      data attributes, comments, or hidden inputs.
- [x] No key value is stored in `localStorage`, `sessionStorage`, cookies, or
      IndexedDB.
- [x] No key value is written to server logs. The request body is never logged.
- [x] No key value is written to run artifacts, `sumario.json`, PDF reports,
      `execution_metadata.json`, or `settings.json`.
- [x] Error messages returned to the browser never echo the submitted key or the
      request body.
- [x] The key input uses `type="password"` with autocomplete disabled.
- [x] The key input is cleared immediately after a successful save, and also after
      a failed save.
- [x] The save request is sent with cache disabled.
- [x] The browser receives only labels (`Key 1`, `Key 2`) and the configured or not
      configured status.
- [x] `git check-ignore` confirms that `Experimento_Multiagente/.env` and
      `Interface/settings.json` are ignored before any commit.
- [x] `.env.example` keeps placeholders only.
- [x] Documented limitation: while the user types, the value exists in the input,
      and at the instant of the save click it travels in the POST body, visible in
      DevTools. Nothing persists in the browser after that. This limitation is
      declared in the User Guide, not hidden.

---

## 5. PDF reports

- [x] The full report prints the pipeline configuration used, for example
      `Configuration: C1`.
- [x] The full report prints the AI used and its default model, for example
      `AI: DeepSeek (deepseek-chat)`.
- [x] The architectural specification PDF prints the same two fields.
- [x] Each system block in the reports identifies the configuration that produced
      it.
- [x] Runs restored from disk after a server restart also show configuration and
      AI, read from a small metadata file written into the run directory at run
      time.
- [x] A restored run whose metadata file predates this change prints
      `not recorded` instead of failing or inventing a value.
- [x] No key value or key fragment appears in either PDF.

---

## 6. Progress indicator

- [x] During a run, the bar advances slowly and continuously, not only when a
      system finishes.
- [x] When a system completes, the bar accelerates toward the new checkpoint.
- [x] The bar never reaches 100% before the final response arrives.
- [x] The status text keeps reporting completed systems, total systems, and the
      current system.
- [x] The animation stops and the bar is cleared or completed on success, on
      error, and on a cancelled request.
- [x] The server-side progress contract (`/api/pipeline/progress`) keeps its
      current fields and semantics.

---

## 7. User Guide page

- [x] A new page is added and linked from the header menu as **`USER GUIDE`**.
      The name `Documentation` is not used.
- [x] The page is written in English and served by the local server.
- [x] The page explains the pipeline and each configuration C0 to C5: agents
      executed, what changes, when to use it, and the C5 cost note.
- [x] The page explains the three providers and their default models.
- [x] The page explains how configuration and provider persist, and that the
      choice is confirmed in a popup.
- [x] The page explains how keys are stored, numbered, and selected, and includes
      the declared DevTools limitation.
- [x] The page explains the metrics shown on the results page and what each PDF
      contains.
- [x] The header of the main page and the header of the User Guide share the same
      navigation.
- [x] The layout is responsive at phone width and follows the existing palette
      and typography.

---

## 8. Persistence

- [x] A single server-side file, `Interface/settings.json`, holds:
  - active configuration;
  - active provider;
  - active key number per provider.
- [x] The file contains no secret and is ignored by Git.
- [x] Missing, unreadable, or corrupt settings fall back to C1 and DeepSeek
      without crashing the server.
- [x] The interface reads the persisted values on load and reflects them in both
      selectors.
- [x] Writes are atomic enough that an interrupted write does not leave the file
      unreadable. A temporary file plus replace is acceptable.

---

## 9. Compatibility and non-regression

- [x] No change to agent prompts, pipeline functions, parsers, or metrics.
- [x] `POST /api/pipeline/run` keeps accepting payloads without `mode` (existing
      behavior defaults to C0 at the adapter level).
- [x] An unknown `mode` is rejected with a clear error instead of silently
      running another configuration.
- [x] Existing routes keep their contracts: `/`, `/static/*`, `/img/*`,
      `/api/systems`, `/api/report/pdf`, `/api/report/specification-pdf`,
      `/api/pipeline/progress`.
- [x] Existing tests pass unchanged:
      `test_contracts`, `test_server`, `test_c4_dispatch`,
      `test_pdf_c0_diagnostic`.
- [x] The interface still runs with the real pipeline when credentials exist, and
      fails with the existing friendly message when they do not.
- [x] The server still starts with `python Interface/server.py` from the
      repository root.

---

## 10. Test plan

### Automated, no LLM calls

- [x] Unit tests for the settings module: defaults, read, write, corrupt file,
      provider validation, configuration validation.
- [x] Unit tests for the `.env` key manager:
  - existing plain key is migrated to `Key 1`;
  - a new key is appended as `Key 2` and the previous line is commented;
  - the active key line matches the selected key;
  - a failed write leaves the previous file intact;
  - no test prints a key value.
- [x] Route tests: `GET` and `POST` for settings, `/user-guide`, mode validation,
      key validation, and the guarantee that no response body contains the
      submitted key.
- [x] PDF tests: configuration and AI markers present in both PDFs, absent key
      values, restored run with and without metadata.
- [x] Front-end static tests: `node --check` for every JavaScript file, plus a
      dependency-free Node test for the selector state functions (persisted
      value, pending value, confirm, discard).
- [x] End-to-end test with the pipeline mocked: select C3 and Gemini, run one
      system, assert the adapter received `mode = c3` and the provider
      environment was set, and assert the response carries configuration and AI.

### Manual usability checks

- [x] Fill two systems, change the configuration, cancel the popup, confirm the
      inputs are intact and the value unchanged.
- [x] Change the configuration and confirm; reload the page; the value persists.
- [x] Change the provider, confirm, run one cheap system, and verify the provider
      used in the server output.
- [x] Add a second key for one provider without checking the box; verify the
      active key did not change and the new key is listed.
- [x] Add a third key with the box checked; verify it becomes active.
- [x] Download both PDFs and verify configuration, AI, and model.
- [x] Inspect the page after saving a key: storage, DOM, and network responses
      contain no key value.

---

## 11. Out of scope for this round

- Registering a new provider from scratch.
- Choosing or editing the model.
- Validating a key against the provider before saving.
- Multi-user accounts, authentication, or remote deployment.
- Any change to the pipeline, to the experiment artifacts, or to the VIA work.

---

## 12. Decisions log

| Topic | Decision |
|---|---|
| Default configuration | C1 |
| C5 in the selector | Yes, labeled as a control condition |
| Default provider | DeepSeek, model `deepseek-chat` |
| Persistence | Server-side `Interface/settings.json`, no secrets |
| Key file | Single `Experimento_Multiagente/.env`, Git-ignored |
| Existing key | Becomes Key 1 of its provider |
| New key | Optional, saved only via `SAVE KEY`, old key commented |
| Active key checkbox | Optional, English label |
| Multiple keys | Key selector appears; choice persists per provider |
| Confirmation | Popup after clicking outside the in-page menu, for C and AI |
| Reports | Configuration and AI in both PDFs, restored runs via run metadata |
| Progress | Continuous slow creep, faster at each completed system |
| Menu page | `USER GUIDE`, English |
| Language | Repository text in English |

---

## 13. Estimated effort

| Block | Estimate |
|---|---|
| Backend settings and `.env` key manager | 50 min |
| Interface selectors and popups | 50 min |
| PDFs and progress bar | 35 min |
| User Guide | 40 min |
| Tests, regression, usability, README updates | 45 min |
| **Total** | **3h30 to 3h50** |

---

## 14. Verification commands

Run from the repository root, inside the project virtual environment:

```powershell
cd "C:\Users\Daniel\OneDrive\I.T\UFCG\Minha_Pesquisa\DAVINCI"
.\Experimento_Multiagente\venv\Scripts\Activate.ps1
python -m unittest discover -s Interface/tests -p "test_*.py"
node --check Interface/static/js/app.js
node --check Interface/static/js/ui-state.js
node Interface/tests/test_ui_state.js
python Interface/server.py
```

Then open `http://127.0.0.1:8000/` and `http://127.0.0.1:8000/user-guide`.

---

## 15. Verification record

Date: 2026-11-23. Environment: Windows 10, Edge driven headless through the
Chrome DevTools Protocol, local server on `127.0.0.1`.

### Automated

- `python -m unittest discover -s Interface/tests -p "test_*.py"`: 55 tests, OK.
  This includes the pre-existing modules and the new ones.
- `node --check` for `app.js` and `ui-state.js`: no syntax errors.
- `node Interface/tests/test_ui_state.js`: 13 checks passed.

### Live browser checks

- Configuration menu lists C0 to C5; provider menu lists DeepSeek, Gemini and
  Claude; the initial selection is C1 and DeepSeek; the key panel shows the
  password field.
- Selecting an option does not open the popup and does not reload the page.
  Clicking outside opens the styled popup with the pending values. Discard
  restores the previous value; confirm saves it, and a reload keeps it.
- Two filled system blocks survived discard and confirm with all values intact,
  and the interface reported no page navigation during the interaction.
- With a temporary `.env` owned by a mock server, keys 2 and 3 were added for
  Gemini through the browser. The first stayed inactive; the second, submitted
  with the checkbox, became active. The panel cleared the field and the checkbox
  after each save. Choosing Key 2 in the popup made it active, and the `.env`
  rewrite matched: previous keys commented, one active line per provider.
- No submitted key appeared in the DOM, in `localStorage`, in `sessionStorage`,
  or in any settings response. `settings.json` contained labels and numbers
  only.
- A mocked pipeline run (no LLM call) with C3 and Gemini showed the bar creeping
  from about 2% to 84% during the run, accelerating after each completed system,
  never reaching 100% before the response, then completing at 100%. The status
  text reported completed and total systems plus the running system. The
  results summary printed `Run configuration: C3 | AI: Gemini
  (gemini-flash-latest)`. `RUN AGAIN` after confirming C4 produced a C4 summary.
- At phone width (390 px), the home page and the User Guide had no horizontal
  overflow (`scrollWidth` equal to `innerWidth`).

### Fix applied during verification

The first live pass showed the confirmation popup opening as soon as an option
was clicked, with a message that omitted the key change. The option handler
re-renders its menu, detaching the clicked node before the event reaches the
document; the outside-click check then failed to see the setup-group ancestor.
The listener now inspects `event.composedPath()`, which preserves the original
ancestors. Re-verified: option and key clicks keep the menu open, and the
popup opens only on an outside click with every pending change in the message.

### Not performed, and why

- A browser run against a real LLM provider: the mocked route test asserts the
  adapter received `mode = c3`, `DAVINCI_LLM_PROVIDER`, and the provider key
  variable. Real 7ep runs were executed through the adapter and through a fresh
  server, as recorded in section 16.
- Writing a key into the real `Experimento_Multiagente/.env`: the browser flow
  ran against a temporary `.env` to keep the real file untouched. The real file
  is covered by the unit tests, which also use a temporary file.
- Opening the PDFs visually: both PDFs were generated and inspected
  programmatically by the tests, which assert the configuration and AI markers,
  the `not recorded` fallback, and the absence of key values.

---

## 16. Real LLM run and TLS trust store

Date: 2026-11-23. System: 7ep, configuration C1, provider DeepSeek
(`deepseek-chat`), key 2.

### Symptom

The pipeline returned a results page with empty proposals. The tracer metadata
recorded two LLM calls with `status: failed` and no tokens. The response still
had `ok: true` because the adapter did not treat empty outputs as an error.

### Cause

Avast Web/Mail Shield intercepts TLS with a local root that is not in certifi.
The same DeepSeek call succeeds with `curl` and fails through CrewAI/LiteLLM
with `CERTIFICATE_VERIFY_FAILED`. The API key and the DeepSeek balance were
valid; a new key changed nothing.

### Fix

- `criar_llm()` calls `_apply_ca_bundle()`, which reads `DAVINCI_CA_BUNDLE`
  from the `.env` file and sets `SSL_CERT_FILE`, `REQUESTS_CA_BUNDLE` and
  `CURL_CA_BUNDLE` when they are not already set. Verification stays enabled.
- The local `.env` (gitignored) points `DAVINCI_CA_BUNDLE`, `SSL_CERT_FILE`
  and `REQUESTS_CA_BUNDLE` to a local PEM bundle in
  `%LOCALAPPDATA%\DAVINCI`. The standard variables also cover a server process
  that still runs the previous code.
- `run_real_pipeline()` returns `ok: false` with "The pipeline returned no
  proposals..." when every proposal is empty, instead of reporting success.

### Verification

- 7ep C1 through the adapter: `ok: true`, F1 1.0 for Proposal A and the
  consolidated architecture, 0.9 for interactions, 21.9 s.
- 7ep C1 through a fresh server on port 8012 with no TLS variables in the
  shell: `ok: true`, F1 1.0 for Proposal A and consolidated, 0.9333 for
  Proposal B, 22.4 s.
- `python -m unittest discover -s Interface/tests -p "test_*.py"`: 55 tests,
  OK.

### Remaining operational note

The three server instances that were already running loaded the previous code,
and at least one holds a stale `SSL_CERT_FILE`. Close them and start a new
server from the repository root. No shell variable is needed after the `.env`
change.

---

## 17. Provider switching: one source of truth

Date: 2026-11-23. Reported symptom: after selecting Gemini and then DeepSeek,
a run still reached Gemini and failed.

### Where the provider was decided

Four places had to agree, and two of them could keep an old value:

1. The browser sends `provider` with every run (`app.js`, `executePipeline`).
2. `server.py` applies it with `apply_provider_environment()` before the run.
3. `criar_llm()` in `main_fewshot.py` reads `DAVINCI_LLM_PROVIDER` from the
   process environment, which `load_dotenv()` fills from `.env`.
4. Every pipeline entrypoint calls `criar_llm()` once and passes that single
   object to every agent; no agent or helper builds its own LLM.

`set_provider()` wrote only `Interface/settings.json`. The `.env` file kept
its own `DAVINCI_LLM_PROVIDER` line, so the two files diverged: settings said
`deepseek` while `.env` still said `gemini`. Any path that reached
`criar_llm()` without `apply_provider_environment()` first used Gemini. The
same divergence reappeared after every switch.

### Fix

- `set_provider()` now rewrites the active `DAVINCI_LLM_PROVIDER` line in
  `.env` atomically and sets `os.environ` immediately. The `.env` file is
  created if it is missing.
- `apply_provider_environment()` pins the same line when a run carries a
  provider that was not saved through the settings endpoint. The write is
  skipped when the value already matches, so a normal run does not touch the
  file.
- `create_server()` calls `sync_provider_environment()`, which applies the
  provider saved in `settings.json` at start. A run request without an
  explicit provider then uses the saved selection instead of an inherited
  environment value.
- The existing `.env` was corrected from `gemini` to `deepseek`, matching
  `settings.json`. Only the provider line changed; no key was read or written.

### Regression test

`Interface/tests/test_provider_switch.py` cycles DeepSeek, Gemini and Claude
through `apply_provider_environment()` and the real `criar_llm()` with a fake
`LLM` object, and asserts the model prefix and the API key used in each case.
It also asserts that `set_provider()` rewrites `.env`, that a later standalone
`criar_llm()` follows the last UI selection, and that server start applies the
saved provider.

### What this guarantees, and what it does not

- Interface runs, runs restarted after a provider switch, and standalone
  scripts that call `criar_llm()` now read the same provider.
- Old `main.py`, `experimento_completo.py` and `diagnosticar_openrouter.py`
  were not used by the interface and were not changed. They still hold their
  own hardcoded providers and remain outside this guarantee.
- A server started before this change keeps the old code until it is
  restarted. Close it and start a new one.

### Verification

- `python -m unittest discover -s Interface/tests -p "test_*.py"`: 55 tests,
  OK.
