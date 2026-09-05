from __future__ import annotations
import csv, json, re
from datetime import datetime
from pathlib import Path

ALIASES = {
    'event_id': ('ev_id', 'EventId', 'event_id'),
    'aircraft_key': ('Aircraft_Key', 'aircraft_key', 'acft_key'),
    'event_date': ('ev_date', 'EventDate', 'event_date'),
    'publication_date': ('PublicationDate', 'publication_date', 'pub_date'),
    'make': ('acft_make', 'Make', 'make'),
    'model': ('acft_model', 'Model', 'model'),
    'serial_number': ('acft_serial_no', 'AircraftSerialNumber', 'serial_number'),
    'phase': ('phase_flt_spec', 'broad_phase', 'BroadPhaseOfFlight', 'phase'),
    'fatalities': ('inj_tot_f', 'TotalFatalInjuries', 'fatalities'),
    'ground_fatalities': ('inj_f_grnd', 'GroundFatalInjuries', 'ground_fatalities'),
    'schedule': ('oper_sched', 'sched', 'Schedule', 'schedule'),
    'carrier': ('oper_name', 'AirCarrier', 'carrier'),
    'far_part': ('far_part', 'FARDescription'),
    'aircraft_category': ('acft_category', 'AircraftCategory', 'aircraft_category'),
}


def _pick(row, names):
    for n in names:
        v = row.get(n)
        if v not in (None, ''):
            return str(v).strip()
    return None


def _int(v):
    try: return int(float(v or 0))
    except (ValueError, TypeError): return 0


def _date(v):
    if not v: return None
    for fmt in ('%m/%d/%y %H:%M:%S', '%m/%d/%Y %H:%M:%S', '%Y-%m-%d', '%m/%d/%Y'):
        try: return datetime.strptime(v.strip(), fmt).date().isoformat()
        except ValueError: pass
    return None


def normalize_row(row):
    d = {k: _pick(row, v) for k, v in ALIASES.items()}
    d['event_date'] = _date(d['event_date']) or d['event_date']
    d['fatalities'] = _int(d['fatalities'])
    d['ground_fatalities'] = _int(d['ground_fatalities'])
    # Preserve the two NTSB fields separately. Target fatality is boolean here to
    # avoid assuming whether any source-specific total double-counts ground deaths.
    d['fatal'] = d['fatalities'] > 0 or d['ground_fatalities'] > 0
    d['external_fatality_present'] = d['ground_fatalities'] > 0
    d['boeing'] = 'BOEING' in (d['make'] or '').upper()
    sched = (d['schedule'] or '').strip().upper(); far = (d['far_part'] or '').strip().upper()
    d['scheduled_service'] = sched == 'SCHD'
    # Preserve a tri-state interpretation. NUSC/NUSN are explicit NTSB dictionary
    # codes; blank/UNK remains unknown rather than being silently treated as
    # non-commercial. The legacy boolean remains for compatibility.
    if far in {'121', '125', '129', '135', 'NUSC'} or sched in {'SCHD', 'NSCH'}:
        d['commercial_status'] = 'commercial'
    elif far in {'NUSN', '091', '091F', '103', '133', '137', '141'}:
        d['commercial_status'] = 'noncommercial'
    else:
        d['commercial_status'] = 'unknown'
    d['commercial'] = d['commercial_status'] == 'commercial'
    d['available_at'] = d['publication_date']
    return d


def _read(path):
    with Path(path).open(errors='replace', newline='') as f:
        return list(csv.DictReader(f))


def _key(row): return (_pick(row, ALIASES['event_id']), _pick(row, ALIASES['aircraft_key']))


def load_event_sequence_phase_map(data_dictionary_csv):
    """Load official eADMS Events_Sequence phase prefixes.

    eADMS encodes phase in wildcard Occurrence_Code values such as 502xxx
    (Approach-IFR Final Approach). Only explicit dictionary rows are admitted.
    """
    out = {}
    if not data_dictionary_csv or not Path(data_dictionary_csv).exists(): return out
    for row in _read(data_dictionary_csv):
        if (row.get('Table') or '').strip() != 'Events_Sequence': continue
        if (row.get('Column') or '').strip() != 'Occurrence_Code': continue
        code = (row.get('code_iaids') or '').strip()
        meaning = (row.get('meaning') or '').strip()
        if re.fullmatch(r'\d{3}x{3}', code, flags=re.IGNORECASE) and meaning:
            out[code[:3]] = meaning
    return out


def recover_sequence_phase(items, phase_map):
    if not phase_map: return None
    def order(item):
        def as_int(v):
            try: return int(v)
            except (TypeError, ValueError): return 999999
        return (0 if str(item.get('defining_event') or '').strip() == '1' else 1,
                as_int(item.get('occurrence_no')), as_int(item.get('eventsoe_no')))
    for item in sorted(items or [], key=order):
        code = str(item.get('occurrence_code') or '').strip()
        prefix = code[:3] if len(code) >= 3 else ''
        if prefix in phase_map:
            return {'code': prefix, 'label': phase_map[prefix], 'source': 'Events_Sequence.Occurrence_Code'}
    return None


def _group_details(path, kind):
    if not path or not Path(path).exists(): return {}
    grouped = {}
    for row in _read(path):
        if kind == 'sequence':
            item = {
                'occurrence_no': _pick(row, ('Occurrence_No',)),
                'occurrence_code': _pick(row, ('Occurrence_Code',)),
                'occurrence_description': _pick(row, ('Occurrence_Description',)),
                'phase_no': _pick(row, ('phase_no',)),
                'eventsoe_no': _pick(row, ('eventsoe_no',)),
                'defining_event': _pick(row, ('Defining_ev',)),
            }
        else:
            item = {'finding_no': _pick(row, ('finding_no',)), 'finding_code': _pick(row, ('finding_code',)),
                    'finding_description': _pick(row, ('finding_description',)), 'cause_factor': _pick(row, ('Cause_Factor',))}
        grouped.setdefault(_key(row), []).append(item)
    return grouped


def _admin(path):
    if not path or not Path(path).exists(): return {}
    out = {}
    for row in _read(path):
        eid = _pick(row, ALIASES['event_id'])
        out[eid] = {'record_status': _pick(row, ('rec_stat',)), 'approval_date': _date(_pick(row, ('approval_date',))),
                    'admin_last_change': _date(_pick(row, ('lchg_date',)))}
    return out


def join_events_aircraft(events_csv, aircraft_csv, sequence_csv=None, findings_csv=None, admin_csv=None, data_dictionary_csv=None):
    events = _read(events_csv); aircraft = _read(aircraft_csv); by_event = {}
    sequence = _group_details(sequence_csv, 'sequence'); findings = _group_details(findings_csv, 'finding'); admin = _admin(admin_csv)
    phase_map = load_event_sequence_phase_map(data_dictionary_csv)
    for a in aircraft: by_event.setdefault(_pick(a, ALIASES['event_id']), []).append(a)
    rows = []
    for e in events:
        eid = _pick(e, ALIASES['event_id']); matches = by_event.get(eid) or [{}]
        for a in matches:
            merged = dict(e); merged.update({k: v for k, v in a.items() if v not in (None, '')})
            r = normalize_row(merged); key = (eid, r['aircraft_key'])
            r['event_sequence'] = sequence.get(key, []); r['findings'] = findings.get(key, [])
            recovered = recover_sequence_phase(r['event_sequence'], phase_map)
            r['phase_recovered'] = recovered['label'] if recovered else None
            r['phase_recovered_code'] = recovered['code'] if recovered else None
            r['phase_recovery_source'] = recovered['source'] if recovered else None
            if recovered: r['phase'] = recovered['label']
            r.update(admin.get(eid, {'record_status': None, 'approval_date': None, 'admin_last_change': None}))
            r['outcome_approved'] = bool(r['approval_date'])
            rows.append(r)
    return rows


def write_normalized(events_csv, aircraft_csv, out_jsonl, sequence_csv=None, findings_csv=None, admin_csv=None, data_dictionary_csv=None):
    rows = join_events_aircraft(events_csv, aircraft_csv, sequence_csv, findings_csv, admin_csv, data_dictionary_csv)
    p = Path(out_jsonl); p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('w') as f:
        for r in rows: f.write(json.dumps(r, sort_keys=True) + '\n')
    return {
        'rows': len(rows), 'boeing_rows': sum(r['boeing'] for r in rows),
        'fatal_boeing_rows': sum(r['boeing'] and r['fatal'] for r in rows),
        'commercial_boeing_rows': sum(r['boeing'] and r['commercial'] for r in rows),
        'scheduled_boeing_rows': sum(r['boeing'] and r['scheduled_service'] for r in rows),
        'availability_known': sum(bool(r['available_at']) for r in rows),
        'outcome_approval_known': sum(bool(r['approval_date']) for r in rows),
        'rows_with_sequence': sum(bool(r['event_sequence']) for r in rows),
        'rows_with_findings': sum(bool(r['findings']) for r in rows),
        'rows_with_recovered_phase': sum(bool(r['phase_recovered']) for r in rows),
        'fatal_rows_with_external_fatality': sum(bool(r['external_fatality_present']) for r in rows),
    }
