# vsco-tero

> An unholy blend of vs-code and Zotero for literature review

This extension generates literature notes (.md) from your Zotero library and autopopulates them with the following:

- item metadata
- your Zotero annotations
- author names

![demonstration of vsco-tero usage](demo.gif)

# Requirements

This extension requires installations of [VSCode](https://code.visualstudio.com/) and [Zotero](https://www.zotero.org/), with the following requirements:

zotero:
- auto-export .bib file
- absolute paths in zotero

vscode:
- [foam](https://github.com/foambubble/foam) vscode extension

## Installation 

- add the config information to `config.toml`
- run `main.py`

## todos

- [X] make lit notes from bib file
  - [X] make authors taggable
- [X] debug logging
- [X] checking for md files that have already been created -k
- [X] config info (pdf path, md path, api keys, .bib file) in vscode settings -a
- [X] get annotations from zotero -k
- [ ] figure out environment export
- [ ] write zotero setup manual -k
- [ ] populate lit notes with llm content
- [ ] make this into an extension
- [ ] VSC Settings UI Fields:
  - [ ] Path to Zotero .bib file
  - [ ] Path to Zotero PDFs
  - [ ] Path to Zotero Annotations
  - [ ] Path to Literature Notes
  - [ ] OpenAI API Key