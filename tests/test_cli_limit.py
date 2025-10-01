from vscotero.cli import ingest_core
from pathlib import Path


def test_cli_limit_idempotent(temp_env):
    ingest_core(Path(temp_env["config"]), limit=1)
    ingest_core(Path(temp_env["config"]), limit=1)
    files = list(temp_env["md_dir"].glob("*.md"))
    assert len(files) == 1
