from __future__ import annotations
from pathlib import Path
from .ntsb import join_events_aircraft


def audit_snapshot(directory, start_year=2010, end_year=2025):
    d = Path(directory)
    rows = join_events_aircraft(
        d/'events.csv', d/'aircraft.csv', sequence_csv=d/'Events_Sequence.csv',
        data_dictionary_csv=d/'eADMSPUB_DataDictionary.csv')
    usable = []
    for row in rows:
        if not row['boeing'] or not row['commercial']:
            continue
        if (row.get('aircraft_category') or '').upper() not in {'', 'AIR'}:
            continue
        try: year = int((row.get('event_date') or '')[:4])
        except (TypeError, ValueError): continue
        if start_year <= year <= end_year:
            usable.append(row)
    recovered = sum(bool(r.get('phase_recovered')) for r in usable)
    with_sequence = sum(bool(r.get('event_sequence')) for r in usable)
    fatal_external_only = [r for r in usable if r['fatal'] and r['fatalities'] == 0 and r['ground_fatalities'] > 0]
    serial_conflict_candidates = [r for r in usable if r.get('serial_number')]
    return {
        'period': [start_year, end_year],
        'boeing_commercial_airplane_rows': len(usable),
        'rows_with_event_sequence': with_sequence,
        'rows_with_recovered_phase': recovered,
        'phase_recovery_fraction': recovered / len(usable) if usable else None,
        'phase_recovery_given_sequence_fraction': recovered / with_sequence if with_sequence else None,
        'external_fatality_only_rows': len(fatal_external_only),
        'external_fatality_only_event_ids': sorted({r['event_id'] for r in fatal_external_only}),
        'rows_with_serial_number': len(serial_conflict_candidates),
        'scope_note': 'NTSB AVALL is supporting/discovery evidence, not global ground truth.',
    }
