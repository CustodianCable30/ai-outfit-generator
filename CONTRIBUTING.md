# Contributing to ai-outfit-generator

Thanks for wanting to push a commit. This repo is a Windows desktop outfit
generator that pairs a local diffusion pipeline with a rules-based styling
engine. Contributions welcome — read the whole file before you open a PR.

## Ground rules

- One feature per PR. If you're touching `engine/` and `handlers/` in the same
  branch, split it.
- Every handler must have a matching test under `tests/`. No exceptions.
- Run `black .` and `ruff check .` before you push. CI will reject otherwise.
- Do not commit model weights. Put them in `models/weights/` locally; the
  downloader (`services/weight_fetcher.py`) handles the rest.

## Dev setup

```powershell
git clone https://github.com/yourname/ai-outfit-generator
cd ai-outfit-generator
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m src.app --dev
```

Python 3.11+ required. CUDA optional but recommended for the diffusion stage.

## Adding a new outfit handler

1. Drop a module in `handlers/` named `<style>_handler.py`.
2. Subclass `handlers.base_handler.BaseHandler`.
3. Register it in `handlers/__init__.py::HANDLER_REGISTRY`.
4. Add fixtures in `tests/fixtures/outfits/`.
5. Write a test that asserts the handler returns a valid `OutfitPlan`.

## Style rules

- Type hints on every public function.
- No bare `except:`. Catch specifically.
- Logging via `utils.logger.get_logger(__name__)`, never `print` in `engine/`.
- Keep `engine/` side-effect free. IO belongs in `services/`.

## Reporting bugs

Open an issue with: OS build, Python version, GPU model, the exact command,
and the full traceback. Screenshots of the rendered outfit help a lot.