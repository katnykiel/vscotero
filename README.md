# vsco-tero

> An unholy blend of vs-code and zotero for literature review

This extension generates literature notes (.md) from your zotero library and autopopulates them with the following:

- item metadata
- your zotero annotations

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


how do we make queries simple and reduce redundant queries?
- this should be rebuilt to handle the new changes and make the code more general
- note query structure
  - populate the md notes with a mix of user-added and llm-generated insight from the paper by reading the pdfs
  - map the md files to an embedding space
  - when you make a query, get closest md files by embedding the query
  - set a parameter that controls how many embedding files you want to use for each query (better answers -> more lit notes)
  - when you download a new paper, easily run an update script and get the annotations from LLMs so you can read it and have some context

- add options to include PDFs in the query (convert to text)
- one big query? are pdfs actually more expensive? can we just do all the md notes?

- add keywords to the PDFs for a better graph view

- do we want to generate new notes for questions asked?

- use langchain? maybe not in the initial build but eventually yea this seems like the robust way to do it