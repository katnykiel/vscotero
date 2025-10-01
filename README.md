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
vscotero is currently distributed as source only. A published Python package (PyPI) is planned for a future release.

1. Configure Zotero to auto‑export a BibTeX file (Better BibTeX recommended).
2. Clone this repository.
3. Choose one of the local setup options below.

#### Option A: Use uv (recommended)
Use uv to create and manage an isolated environment automatically (no manual activation needed).

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

#### Option B: Plain pip / virtualenv
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
vscotero --path config.toml
```

#### (Future) PyPI installation (planned)
Will become as simple as:
```bash
pip install vscotero
vscotero --path config.toml
```

4. Create / fill `config.toml` (example below).

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
