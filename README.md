## vscotero

Generate markdown literature notes from your Zotero library (metadata + annotations) for use in VS Code (Foam / wiki links compatible).

![demonstration of vscotero usage](demo.gif)

### Features
- Extract item metadata from a Zotero auto‑exported BibTeX file
- Pull PDF annotations directly from the Zotero `zotero.sqlite` database (copied safely to avoid locks)
- Group annotations by highlight color (configurable colormap)
- Produce one Markdown note per reference with YAML front matter
- Deterministic & scriptable CLI (`vscotero ingest`)

### Installation

1. Configure Zotero to auto‑export a BibTeX file (Better BibTeX recommended).
2. Install via pip (recommended once published) OR work from source (below).

#### Option A: From PyPI (once released)
```bash
pip install vscotero
vscotero ingest --path config.toml --limit 1
```

#### Option B: Latest (GitHub) with pip
```bash
pip install git+https://github.com/katnykiel/vscotero.git
vscotero ingest --path config.toml --limit 1
```

#### Option C: Clone + uv (recommended for development)
Clone this repo, then:

Sync / install (safe to re-run):
```bash
uv sync
```

Check the CLI version:
```bash
uv run vscotero --version
```

Ingest (example with a limit + debug):
```bash
uv run vscotero ingest --path config.toml --limit 1 --debug
```

Run tests:
```bash
uv run pytest -q
```

#### Option D: Plain pip / virtualenv
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
vscotero --path config.toml
```
3. Create / fill `config.toml` (example below).

### Publishing (maintainers)
Build & upload using uv (preferred):
```bash
uv build          # produces sdist + wheel under dist/
uv publish        # prompts for PyPI token on first use or use UV_PUBLISH_TOKEN
```

Test on TestPyPI first:
```bash
uv publish --index-url https://test.pypi.org/legacy/
pip install --index-url https://test.pypi.org/simple --no-deps vscotero
```

Alternative (twine):
```bash
pip install build twine
python -m build
twine upload dist/*
```

Version bump workflow (semantic-ish):
1. Update `version` in `pyproject.toml` (and CHANGELOG)
2. Commit + tag, e.g. `git tag -a v0.2.1 -m "v0.2.1"`
3. `git push --follow-tags`
4. Run publish

After release, verify:
```bash
pip install --upgrade vscotero
vscotero --version
```

### Example `config.toml`
```toml
[notes]
bib_path = "/absolute/path/to/library.bib"   # Zotero auto-export (Better BibTeX)
md_path  = "/absolute/path/to/notes"         # Output folder for generated notes
db_path  = "~/Zotero/zotero.sqlite"           # Zotero database path
```

### Usage
Ingest all notes:
```bash
vscotero ingest --path config.toml
```

Clean existing notes first:
```bash
vscotero ingest --path config.toml --clean
```

Limit number (debugging):
```bash
vscotero ingest --path config.toml --limit 5
```

### Color Map
Override in `config.toml` (any subset):
```toml
[notes.colormap]
"#ffd400" = "Insights"
"#ff6666" = "Discrepancies"
```

### Development
Run tests:
```bash
uv run pytest -q
```

View version:
```bash
vscotero --version
```

See `CHANGELOG.md` for release notes.
