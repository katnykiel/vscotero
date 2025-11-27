{ pkgs ? import <nixpkgs> {} }:

let
  python = pkgs.python313;
  pythonPackages = python.pkgs;
in
pkgs.mkShell {
  buildInputs = [
    python
    pythonPackages.bibtexparser
    pythonPackages.pandas
    pythonPackages.pyyaml
    pythonPackages.toml
    pythonPackages.typer
    pythonPackages.pytest
    pythonPackages.setuptools
  ];

  shellHook = ''
    # Set up Python path to include the current directory because i'm quirky
    export PYTHONPATH="$PWD:$PYTHONPATH"
    
    # Create alias for vscotero command
    alias vscotero='python -c "from vscotero.cli import app; app()"'
  '';
}