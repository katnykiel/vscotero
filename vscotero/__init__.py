"""vscotero: VSCode + Zotero literature note ingester."""

from importlib import metadata as _metadata

try:  # pragma: no cover - fallback if metadata missing in editable install
	__version__ = _metadata.version("vscotero")
except _metadata.PackageNotFoundError:  # pragma: no cover
	__version__ = "0.0.0+dev"

from .cli import app  # noqa: F401

__all__ = ["app", "__version__"]

