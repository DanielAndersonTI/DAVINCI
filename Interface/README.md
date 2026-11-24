# DAVINCI Architect

This local prototype collects generalized system requirements and displays microservice architecture results from the existing pipeline. It uses Python's standard-library HTTP server. The pipeline itself lives in `Experimento_Multiagente/` and is not modified by the interface.

## Local startup

From the repository root, run:

```powershell
python Interface/server.py
```

Open <http://127.0.0.1:8000/> in a browser. Stop the server with `Ctrl+C`.

## Browser workflow

1. Choose the pipeline configuration (C0 to C5) and the AI provider in the setup bar. The defaults are C1 and DeepSeek.
2. Complete the required fields in the first system block.
3. Use `ADD ANOTHER SYSTEM` to add up to ten systems.
4. Choose `RUN PIPELINE` to run the real pipeline for each submitted system.
5. Review Services, Interactions, and Best Results.
6. Select `DOWNLOAD FULL REPORT (PDF)` or `DOWNLOAD YAML SPECIFICATION (PDF)` after a successful run.
7. Select `NEW DECOMPOSITION` to reset the form. The configuration and provider are not reset.

The selectors open an in-page menu; clicking outside opens a confirmation popup. A choice is saved only after `CONFIRM`; `DISCARD` restores the previous value. Both values persist on the server, so they survive reloads and restarts.

The `USER GUIDE` page explains the pipeline, every configuration, the providers, the metrics, and the key handling.

## Settings and API keys

- `Interface/settings.json` stores the active configuration, the active provider, and the active key number per provider. It contains no secret and is ignored by Git.
- API keys live only in `Experimento_Multiagente/.env`, which is ignored by Git. The existing key becomes `Key 1`; new keys are numbered sequentially and the previous active key stays as a commented line.
- The browser receives only labels such as `Key 1` and whether a provider is configured. Key values are never returned in a response and never written to `settings.json`, reports, or run artifacts.
- The provider environment is applied before each run. `criar_llm()` reads the provider variables on every call, so the pipeline source does not need to change.

## API routes

- `GET /` serves the interface.
- `GET /user-guide` serves the English user guide.
- `GET /static/<asset>` serves frontend assets.
- `GET /api/settings` returns configurations, providers, labels, models, and configured status. It never returns a key value.
- `POST /api/settings` saves a confirmed configuration, provider, or key number.
- `POST /api/settings/api-key` validates and stores a new key in `.env`.
- `POST /api/systems` creates an empty system-block model.
- `DELETE /api/systems/<index>` validates removal of a system block.
- `POST /api/pipeline/run` executes the real pipeline for each submitted system.
- `GET /api/pipeline/progress` returns the progress fields used by the loading bar.
- `GET /api/report/pdf` downloads the latest successful architecture report.
- `GET /api/report/specification-pdf` downloads the YAML specification report.

## Testing

From the repository root, run:

```powershell
python -m unittest discover -s Interface/tests -p "test_*.py"
node --check Interface/static/js/app.js
node --check Interface/static/js/ui-state.js
node Interface/tests/test_ui_state.js
```

The tests mock `run_real_pipeline`, so no external model credentials are required and no tokens are spent. Tests that touch persisted artifacts patch `Interface.server.RESULTS_DIR` to a temporary directory; the default remains `result/` at the repository root.
