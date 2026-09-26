"""Convert JSON data (list of dicts or dict of lists) to CSV."""
from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Any, Iterable, Sequence


def _collect_headers(rows: Iterable[dict]) -> list[str]:
    headers: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                headers.append(key)
    return headers


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def json_to_csv(
    data: Any,
    output: str | Path | None = None,
    *,
    delimiter: str = ",",
    include_header: bool = True,
    flatten: bool = False,
) -> str:
    rows = _normalize(data)
    if flatten:
        rows = [_flatten_row(r) for r in rows]
    headers = _collect_headers(rows)

    buffer = io.StringIO()
    writer = csv.DictWriter(
        buffer,
        fieldnames=headers,
        delimiter=delimiter,
        extrasaction="ignore",
        lineterminator="\n",
    )
    if include_header:
        writer.writeheader()
    for row in rows:
        writer.writerow({k: _stringify(row.get(k)) for k in headers})

    csv_text = buffer.getvalue()
    if output is not None:
        Path(output).write_text(csv_text, encoding="utf-8")
    return csv_text


def json_string_to_csv(
    json_string: str,
    output: str | Path | None = None,
    **kwargs: Any,
) -> str:
    return json_to_csv(json.loads(json_string), output=output, **kwargs)


def _normalize(data: Any) -> list[dict]:
    if isinstance(data, list):
        if not all(isinstance(item, dict) for item in data):
            raise TypeError("When data is a list, every item must be a dict.")
        return data
    if isinstance(data, dict):
        keys = list(data.keys())
        lengths = {len(v) for v in data.values() if isinstance(v, Sequence)}
        if len(lengths) > 1:
            raise ValueError("All lists in dict-of-lists must have the same length.")
        n = lengths.pop() if lengths else 0
        return [{k: data[k][i] for k in keys} for i in range(n)]
    raise TypeError("data must be a list of dicts or a dict of lists.")


def _flatten_row(row: dict, prefix: str = "") -> dict:
    flat: dict[str, Any] = {}
    for key, value in row.items():
        new_key = f"{prefix}{key}"
        if isinstance(value, dict):
            flat.update(_flatten_row(value, prefix=f"{new_key}."))
        else:
            flat[new_key] = value
    return flat
