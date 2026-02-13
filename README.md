## vscotero

Generate markdown literature notes from your Zotero library (metadata + annotations) for use in VS Code (Foam / wiki links compatible).

![demonstration of vscotero usage](demo.gif)

### Features

- Extract item metadata from a Zotero auto‑exported BibTeX file
- Pull PDF annotations directly from the Zotero `zotero.sqlite` database
- Group annotations by highlight color (configurable colormap)

### Recommended installation: pip

```bash
pip install vscotero
```

Then configure Zotero to auto-export a BibTeX file (Better BibTeX recommended) and create a `config.toml` file (see example below).

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

### Color Map
Override in `config.toml` (any subset):
```toml
[notes.colormap]
"#ffd400" = "Insights"
"#ff6666" = "Discrepancies"
```

See `CHANGELOG.md` for release notes.

#### Build from source

```bash
git clone https://github.com/katnykiel/vscotero
cd vscotero
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### TODOs

- fix the config system
  - add CLI option, put config.toml in some default path
  - remove .bib path? doesn't db have this info
- confirmation prompt before deletion
- check if it overwrites notes (it does, fix)
- add color hex codes to default config.toml with description
- error handling
- better tests for edge cases / bad config
- add a nix install