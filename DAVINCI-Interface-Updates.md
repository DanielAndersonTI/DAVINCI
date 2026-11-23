# DAVINCI Interface Updates

Working specification and final acceptance checklist for the usability additions to
the DAVINCI Architect web interface.

- Status: approved, not implemented.
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

- [ ] The main page offers a selector with **C0, C1, C2, C3, C4, C5**.
- [ ] Default on first load or missing settings: **C1** (the complete pipeline).
- [ ] C5 is listed as a control condition. Its description states that, without a
      frozen run directory, it regenerates the proposals like C1 and runs Agent 3
      twice, so it costs more.
- [ ] Each option shows a short label and a one-line purpose.
- [ ] The selected configuration persists on the server and survives a server
      restart and a page reload.
- [ ] The choice changes only when the user explicitly confirms a new choice.
      It is not reset by `NEW DECOMPOSITION`, by a completed run, or by a reload.
- [ ] The results page exposes the same selector, so a new run can use another
      configuration without going back to the form.
- [ ] `RUN AGAIN` uses the configuration active at the moment of the click, not a
      value captured before.
- [ ] The selector is disabled while a run is in progress.
- [ ] The selector opens an in-page menu. No page reload occurs, so data already
      typed into the system inputs is preserved.

### Confirmation flow

- [ ] Clicking a configuration opens the menu without changing the active value.
- [ ] Clicking outside the menu opens a confirmation popup.
- [ ] Confirming saves the new value, applies it, and closes the popup.
- [ ] Discarding closes the popup and restores the previous value on screen.
- [ ] Without confirmation, nothing is saved and nothing changes.
- [ ] The popup follows the DAVINCI visual identity: navy, gold, square corners,
      uppercase labels, responsive at phone width.

---

## 2. AI provider selector

### Requirements

- [ ] The interface offers three providers: **DeepSeek**, **Gemini**, **Claude**.
- [ ] Default on first load or missing settings: **DeepSeek**.
- [ ] The user chooses only the provider. The model is not selectable and uses the
      existing defaults:
  - DeepSeek: `deepseek-chat`
  - Gemini: `gemini-flash-latest`
  - Claude: `claude-sonnet-4-5-20250929`
- [ ] The provider choice persists on the server, like the configuration.
- [ ] The run executed after confirmation uses the selected provider.
- [ ] Switching provider requires no change to the pipeline source. The server
      sets the provider environment variables before each run; `criar_llm()` reads
      them on every call and `load_dotenv` does not override values already set.
- [ ] The interface shows, for the selected provider, whether a key is
      configured. It does not show the key.
- [ ] If the selected provider has no key, the interface blocks the run with a
      clear message instead of starting a request that fails at the LLM call.
- [ ] Providers that are not selected stay inert. Their keys do not have to be
      valid for the system to run.

### Confirmation flow

- [ ] Same behavior as the configuration selector: in-page menu, no reload,
      confirmation popup on click outside, discard restores the previous value.
- [ ] The provider becomes active only after the popup is confirmed.

---

## 3. API key management

### Storage model

- [ ] Keys live in a single file, `Experimento_Multiagente/.env`, which is already
      ignored by Git. Keys are not duplicated in any other file.
- [ ] `Interface/settings.json` stores only configuration, provider, and which key
      number is active per provider. It never stores a key value.
- [ ] The key that exists today for a provider becomes **Key 1** of that provider.
      New keys are numbered sequentially: Key 2, Key 3, and so on.
- [ ] Adding a new key does not delete the previous one. The previous key stays in
      the `.env` file as an inactive commented line, with provider and number.
- [ ] The active line used by the pipeline is rewritten to point to the selected
      key. Only one active key per provider exists at a time.

### Add-key panel

- [ ] Clicking a provider opens, below it, an optional panel to add a new key for
      that provider.
- [ ] The panel contains a password field and a **`SAVE KEY`** button. Nothing is
      written until the button is clicked.
- [ ] The panel can be left empty. In that case the key already registered for the
      provider is used.
- [ ] The panel contains an optional checkbox, in English, labeled
      **`Set as the active key for this AI`**. Checked, the new key becomes active;
      unchecked, the key is only registered and the current active key remains.
- [ ] Saving validates that the field is not empty and that the target provider is
      one of the three supported providers.
- [ ] After saving, the field is cleared and the panel shows the new key as
      available, without revealing any part of its value.

### Key selection

- [ ] When a provider has more than one registered key, selecting that provider
      also requires choosing the key.
- [ ] The key selector lists labels only, such as `Key 1` and `Key 2`.
- [ ] The chosen key number persists per provider.
- [ ] Provider and key are confirmed together by the same popup when the panel is
      closed.

---

## 4. Security requirements

These are blocking. Any failure here blocks delivery, regardless of usability.

- [ ] No key value ever appears in an HTTP response.
- [ ] No key value is written to the DOM after saving: not in text, attributes,
      data attributes, comments, or hidden inputs.
- [ ] No key value is stored in `localStorage`, `sessionStorage`, cookies, or
      IndexedDB.
- [ ] No key value is written to server logs. The request body is never logged.
- [ ] No key value is written to run artifacts, `sumario.json`, PDF reports,
      `execution_metadata.json`, or `settings.json`.
- [ ] Error messages returned to the browser never echo the submitted key or the
      request body.
- [ ] The key input uses `type="password"` with autocomplete disabled.
- [ ] The key input is cleared immediately after a successful save, and also after
      a failed save.
- [ ] The save request is sent with cache disabled.
- [ ] The browser receives only labels (`Key 1`, `Key 2`) and the configured or not
      configured status.
- [ ] `git check-ignore` confirms that `Experimento_Multiagente/.env` and
      `Interface/settings.json` are ignored before any commit.
- [ ] `.env.example` keeps placeholders only.
- [ ] Documented limitation: while the user types, the value exists in the input,
      and at the instant of the save click it travels in the POST body, visible in
      DevTools. Nothing persists in the browser after that. This limitation is
      declared in the User Guide, not hidden.

---

## 5. PDF reports

- [ ] The full report prints the pipeline configuration used, for example
      `Configuration: C1`.
- [ ] The full report prints the AI used and its default model, for example
      `AI: DeepSeek (deepseek-chat)`.
- [ ] The architectural specification PDF prints the same two fields.
- [ ] Each system block in the reports identifies the configuration that produced
      it.
- [ ] Runs restored from disk after a server restart also show configuration and
      AI, read from a small metadata file written into the run directory at run
      time.
- [ ] A restored run whose metadata file predates this change prints
      `not recorded` instead of failing or inventing a value.
- [ ] No key value or key fragment appears in either PDF.

---

## 6. Progress indicator

- [ ] During a run, the bar advances slowly and continuously, not only when a
      system finishes.
- [ ] When a system completes, the bar accelerates toward the new checkpoint.
- [ ] The bar never reaches 100% before the final response arrives.
- [ ] The status text keeps reporting completed systems, total systems, and the
      current system.
- [ ] The animation stops and the bar is cleared or completed on success, on
      error, and on a cancelled request.
- [ ] The server-side progress contract (`/api/pipeline/progress`) keeps its
      current fields and semantics.

---

## 7. User Guide page

- [ ] A new page is added and linked from the header menu as **`USER GUIDE`**.
      The name `Documentation` is not used.
- [ ] The page is written in English and served by the local server.
- [ ] The page explains the pipeline and each configuration C0 to C5: agents
      executed, what changes, when to use it, and the C5 cost note.
- [ ] The page explains the three providers and their default models.
- [ ] The page explains how configuration and provider persist, and that the
      choice is confirmed in a popup.
- [ ] The page explains how keys are stored, numbered, and selected, and includes
      the declared DevTools limitation.
- [ ] The page explains the metrics shown on the results page and what each PDF
      contains.
- [ ] The header of the main page and the header of the User Guide share the same
      navigation.
- [ ] The layout is responsive at phone width and follows the existing palette
      and typography.

---

## 8. Persistence

- [ ] A single server-side file, `Interface/settings.json`, holds:
  - active configuration;
  - active provider;
  - active key number per provider.
- [ ] The file contains no secret and is ignored by Git.
- [ ] Missing, unreadable, or corrupt settings fall back to C1 and DeepSeek
      without crashing the server.
- [ ] The interface reads the persisted values on load and reflects them in both
      selectors.
- [ ] Writes are atomic enough that an interrupted write does not leave the file
      unreadable. A temporary file plus replace is acceptable.

---

## 9. Compatibility and non-regression

- [ ] No change to agent prompts, pipeline functions, parsers, or metrics.
- [ ] `POST /api/pipeline/run` keeps accepting payloads without `mode` (existing
      behavior defaults to C0 at the adapter level).
- [ ] An unknown `mode` is rejected with a clear error instead of silently
      running another configuration.
- [ ] Existing routes keep their contracts: `/`, `/static/*`, `/img/*`,
      `/api/systems`, `/api/report/pdf`, `/api/report/specification-pdf`,
      `/api/pipeline/progress`.
- [ ] Existing tests pass unchanged:
      `test_contracts`, `test_server`, `test_c4_dispatch`,
      `test_pdf_c0_diagnostic`.
- [ ] The interface still runs with the real pipeline when credentials exist, and
      fails with the existing friendly message when they do not.
- [ ] The server still starts with `python Interface/server.py` from the
      repository root.

---

## 10. Test plan

### Automated, no LLM calls

- [ ] Unit tests for the settings module: defaults, read, write, corrupt file,
      provider validation, configuration validation.
- [ ] Unit tests for the `.env` key manager:
  - existing plain key is migrated to `Key 1`;
  - a new key is appended as `Key 2` and the previous line is commented;
  - the active key line matches the selected key;
  - a failed write leaves the previous file intact;
  - no test prints a key value.
- [ ] Route tests: `GET` and `POST` for settings, `/user-guide`, mode validation,
      key validation, and the guarantee that no response body contains the
      submitted key.
- [ ] PDF tests: configuration and AI markers present in both PDFs, absent key
      values, restored run with and without metadata.
- [ ] Front-end static tests: `node --check` for every JavaScript file, plus a
      dependency-free Node test for the selector state functions (persisted
      value, pending value, confirm, discard).
- [ ] End-to-end test with the pipeline mocked: select C3 and Gemini, run one
      system, assert the adapter received `mode = c3` and the provider
      environment was set, and assert the response carries configuration and AI.

### Manual usability checks

- [ ] Fill two systems, change the configuration, cancel the popup, confirm the
      inputs are intact and the value unchanged.
- [ ] Change the configuration and confirm; reload the page; the value persists.
- [ ] Change the provider, confirm, run one cheap system, and verify the provider
      used in the server output.
- [ ] Add a second key for one provider without checking the box; verify the
      active key did not change and the new key is listed.
- [ ] Add a third key with the box checked; verify it becomes active.
- [ ] Download both PDFs and verify configuration, AI, and model.
- [ ] Inspect the page after saving a key: storage, DOM, and network responses
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
node --check Interface/static/js/settings.js
node Interface/tests/test_ui_state.js
python Interface/server.py
```

Then open `http://127.0.0.1:8000/` and `http://127.0.0.1:8000/user-guide`.
