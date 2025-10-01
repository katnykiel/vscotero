from vscotero.cli import ingest_core
from pathlib import Path


def test_cli_ingest(temp_env):
    # Directly call the function to ensure core logic executes
    ingest_core(Path(temp_env["config"]))
    md_file = temp_env["md_dir"] / "smith2024example.md"
    assert md_file.exists()
    md_file = temp_env["md_dir"] / "smith2024example.md"
    assert md_file.exists()
