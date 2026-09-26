import pytest
from json2csv_lite import json_string_to_csv, json_to_csv


def test_basic_list_of_dicts():
    data = [{"name": "Ali", "age": 30}, {"name": "Sara", "age": 25}]
    assert json_to_csv(data) == "name,age\nAli,30\nSara,25\n"


def test_missing_keys_filled_with_empty():
    csv_text = json_to_csv([{"a": 1}, {"a": 2, "b": 3}])
    assert "a,b\n" in csv_text
    assert "1,\n" in csv_text
    assert "2,3\n" in csv_text


def test_none_and_bool():
    csv_text = json_to_csv([{"x": None, "y": True, "z": False}])
    assert "x,y,z\n" in csv_text
    assert ",true,false\n" in csv_text


def test_flatten_nested_dict():
    csv_text = json_to_csv([{"id": 1, "meta": {"k": "v", "n": 2}}], flatten=True)
    assert "id,meta.k,meta.n\n" in csv_text
    assert "1,v,2\n" in csv_text


def test_dict_of_lists():
    csv_text = json_to_csv({"name": ["Ali", "Sara"], "age": [30, 25]})
    assert csv_text == "name,age\nAli,30\nSara,25\n"


def test_dict_of_lists_mismatched():
    with pytest.raises(ValueError):
        json_to_csv({"a": [1, 2], "b": [1]})


def test_output_file(tmp_path):
    out = tmp_path / "out.csv"
    json_to_csv([{"a": 1}], output=out)
    assert out.read_text(encoding="utf-8") == "a\n1\n"


def test_custom_delimiter():
    assert json_to_csv([{"a": 1, "b": 2}], delimiter=";") == "a;b\n1;2\n"


def test_json_string_wrapper():
    assert json_string_to_csv('[{"a": 1}, {"a": 2}]') == "a\n1\n2\n"


def test_unsupported_type():
    with pytest.raises(TypeError):
        json_to_csv("not a list or dict")
