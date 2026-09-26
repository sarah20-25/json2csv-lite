# json2csv-lite

Tiny, dependency-free JSON to CSV converter for Python.

- No external dependencies
- Supports list-of-dicts **and** dict-of-lists
- Optional nested-dict flattening
- Works with files or strings

## Install

```bash
pip install json2csv-lite
```

## Usage

```python
from json2csv_lite import json_to_csv

data = [
    {"name": "Ali", "age": 30},
    {"name": "Sara", "age": 25},
]

csv_text = json_to_csv(data)
print(csv_text)
# name,age
# Ali,30
# Sara,25
```

Write directly to a file:

```python
json_to_csv(data, output="people.csv")
```

Flatten nested objects:

```python
data = [{"id": 1, "meta": {"lang": "py", "level": 3}}]
print(json_to_csv(data, flatten=True))
# id,meta.lang,meta.level
# 1,py,3
```

From a JSON string:

```python
from json2csv_lite import json_string_to_csv

json_string_to_csv('[{"a": 1}, {"a": 2}]')
```

## API

### `json_to_csv(data, output=None, *, delimiter=",", include_header=True, flatten=False)`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `data` | `list[dict]` or `dict[str, list]` | – | Input data |
| `output` | `str`, `Path`, or `None` | `None` | Optional output file path |
| `delimiter` | `str` | `","` | CSV delimiter |
| `include_header` | `bool` | `True` | Include header row |
| `flatten` | `bool` | `False` | Flatten nested dicts with dot notation |

### `json_string_to_csv(json_string, output=None, **kwargs)`

Convenience wrapper around `json_to_csv`.

## License

MIT
