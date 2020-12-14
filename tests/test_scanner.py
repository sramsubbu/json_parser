import pytest
from myjson import scanner


def test_scanner_integer():
    text = "12"
    obj = scanner.Scanner(text)
    item = obj.get_next().string
    assert item == "12"

    text = "12.34"
    obj = scanner.Scanner(text)
    item = obj.get_next().string
    assert item == "12.34"


def test_scanner_string():
    text = '"12"'
    obj = scanner.Scanner(text)
    item = obj.get_next().string
    assert item == '12'


def test_scanner_keyword():
    texts = ["true", "false", "null"]
    for text in texts:
        obj = scanner.Scanner(text)
        item = obj.get_next().string
        assert item == text


def test_scanner_singles():
    singles = ",:[]{}"
    for single in singles:
        obj = scanner.Scanner(single)
        item = obj.get_next().string
        assert item == single


def test_successive():
    text = '"Hello" 12.5'
    obj = scanner.Scanner(text)
    item = obj.get_next().string
    assert item == 'Hello'
    item = obj.get_next()
    assert item.type == 'float'
    assert item.string == '12.5'


# @pytest.mark.skip
def test_all_items():
    text = '["Hello",12]'
    obj = scanner.Scanner(text)
    items = []
    while True:
        try:
            item = obj.get_next()
            items.append(item.string)
        except IndexError:
            break
        else:
            if item.type == 'EOF':
                break

    assert len(items) == 5+1


# @pytest.mark.skip
def test_skip_whitespace():
    text = ' [\n "Hello" ,\n 12\t\n]'
    obj = scanner.Scanner(text)
    items = []
    while True:
        try:
            item = obj.get_next()
            items.append(item.string)
        except IndexError:
            break
        if item.type == 'EOF':
            break

    assert len(items) == 5+1 # including 1 EOF token
