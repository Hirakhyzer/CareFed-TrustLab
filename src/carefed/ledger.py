from __future__ import annotations

import json
from pathlib import Path
from .aggregation import hash_payload

def verify(path: str | Path) -> dict:
    path = Path(path)
    previous = None
    count = 0
    for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), start=1):
        if not line.strip():
            continue
        record = json.loads(line)
        saved = record.pop('record_hash')
        if record.get('previous_hash') != previous:
            return {'valid': False, 'line': number, 'reason': 'previous mismatch'}
        if saved != hash_payload(record):
            return {'valid': False, 'line': number, 'reason': 'record mismatch'}
        previous = saved
        count += 1
    return {'valid': True, 'records': count, 'final_hash': previous}
