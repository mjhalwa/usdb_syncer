"""Tests for functions from the note_utils module."""

import os
from glob import glob

from usdb_dl import SongId
from usdb_dl.logger import get_logger
from usdb_dl.notes_parser import SongTxt

_logger = get_logger(__file__, SongId(1))


def test_notes_parser_normalized(resource_dir: str) -> None:
    folder = os.path.join(resource_dir, "txt", "normalized")
    for path in glob(f"{folder}/*.txt"):
        with open(path, encoding="utf-8") as file:
            contents = file.read()
        txt = SongTxt(contents, _logger)
        assert str(txt) == contents


def test_notes_parser_deviant(resource_dir: str) -> None:
    folder = os.path.join(resource_dir, "txt", "deviant")
    for path in glob(f"{folder}/*_in.txt"):
        with open(path, encoding="utf-8") as file:
            contents = file.read()
        with open(path.replace("_in.txt", "_out.txt"), encoding="utf-8") as file:
            out = file.read()
        txt = SongTxt(contents, _logger)
        assert str(txt) == out
