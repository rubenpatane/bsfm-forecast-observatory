from __future__ import annotations
from datetime import datetime, timezone

def parse_time(value:str)->datetime:
    v=value.strip().replace('Z','+00:00')
    dt=datetime.fromisoformat(v)
    if dt.tzinfo is None: dt=dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

def eligible(row:dict, cutoff:str, available_field='available_at')->bool:
    value=row.get(available_field)
    if not value: return False
    return parse_time(value)<=parse_time(cutoff)

def point_in_time(rows:list[dict], cutoff:str, available_field='available_at')->list[dict]:
    return [r for r in rows if eligible(r,cutoff,available_field)]

def assert_no_future(rows:list[dict], cutoff:str, available_field='available_at')->None:
    leaked=[r for r in rows if not eligible(r,cutoff,available_field)]
    if leaked: raise ValueError(f'future leakage: {len(leaked)} rows unavailable at cutoff {cutoff}')
