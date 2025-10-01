## Changelog

### 0.2.0 - Initial public release
* CLI command `vscotero ingest` with options: `--path`, `--clean`, `--limit`, `--debug`, `--version`.
* BibTeX + Zotero sqlite ingestion -> Markdown notes with YAML front matter.
* Annotation grouping by highlight color with configurable colormap.
* Safe sqlite copy to avoid locked database errors.
* Normalized + fuzzy path matching for attachment -> bib entry resolution.
* Test suite covering writer, annotations, and ingestion core.
