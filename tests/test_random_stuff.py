import pytest


def test_read_file(new_file):
    with open(new_file, 'r') as f:
        txt = f.read()
    assert txt == 'abcdef'
