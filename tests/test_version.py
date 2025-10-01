from vscotero import __version__
from typer.testing import CliRunner
from vscotero.cli import app


def test_version_constant():
    assert isinstance(__version__, str)
    assert len(__version__) > 0


def test_version_flag():
    runner = CliRunner()
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "vscotero" in result.stdout.lower()