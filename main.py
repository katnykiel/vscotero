"""Deprecated entrypoint; prefer the CLI command:

    vscotero ingest --path config.toml

This shim remains for backward compatibility.
"""

from vscotero.cli import main as _main

if __name__ == "__main__":  # pragma: no cover
    _main()

