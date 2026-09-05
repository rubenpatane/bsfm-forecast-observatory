from bsfm.exposure_import import aggregate_standardized_flight_legs


def _row(day, leg, equipment, *, operated=True, scope='global_commercial', vintage='v1'):
    return {
        'flight_date': day,
        'leg_id': leg,
        'equipment_code': equipment,
        'operated': operated,
        'scope': scope,
        'vintage_id': vintage,
    }


def test_standardized_import_counts_operated_target_legs_by_year_and_cohort():
    rows = [
        _row('2019-01-01', 'A', 'B738'),
        _row('2019-01-02', 'B', 'B38M'),
        _row('2019-01-03', 'C', 'B733'),
        _row('2019-01-04', 'D', 'B732'),
        _row('2019-01-05', 'E', 'B744'),
    ]
    out = aggregate_standardized_flight_legs(rows)
    got = {(r['year'], r['cohort']): r['departures'] for r in out['exposure_rows']}
    assert got[(2019, '737-NG')] == 1.0
    assert got[(2019, '737-MAX')] == 1.0
    assert got[(2019, '737-Classic')] == 1.0
    assert got[(2019, '737-Original')] == 1.0
    assert got[(2019, '747')] == 1.0
    assert out['complete_for_g2'] is True


def test_standardized_import_never_proxy_splits_unknown_or_generic_737():
    out = aggregate_standardized_flight_legs([
        _row('2019-01-01', 'A', '737'),
        _row('2019-01-02', 'B', 'B737X'),
    ])
    assert out['exposure_rows'] == []
    assert out['unknown_equipment'] == [
        {'equipment_code': '737', 'rows': 1},
        {'equipment_code': 'B737X', 'rows': 1},
    ]
    assert out['complete_for_g2'] is False


def test_standardized_import_excludes_cancelled_out_of_scope_and_out_of_range_rows():
    out = aggregate_standardized_flight_legs([
        _row('2019-01-01', 'A', 'B738', operated=False),
        _row('2019-01-02', 'B', 'B738', scope='regional_only'),
        _row('2009-12-31', 'C', 'B738'),
        _row('2019-01-03', 'D', 'B738'),
    ])
    assert out['diagnostics']['not_operated_rows'] == 1
    assert out['diagnostics']['out_of_scope_rows'] == 1
    assert out['diagnostics']['out_of_range_rows'] == 1
    assert out['diagnostics']['counted_rows'] == 1


def test_standardized_import_deduplicates_exact_rows_and_flags_conflicts():
    same = _row('2019-01-01', 'A', 'B738')
    out = aggregate_standardized_flight_legs([
        same,
        dict(same),
        _row('2019-01-01', 'A', 'B38M'),
    ])
    assert out['diagnostics']['exact_duplicate_rows'] == 1
    assert out['diagnostics']['conflicting_duplicate_rows'] == 1
    assert out['complete_for_g2'] is False


def test_standardized_import_requires_vendor_vintage_and_boolean_operated():
    out = aggregate_standardized_flight_legs([
        {'flight_date': '2019-01-01', 'leg_id': 'A', 'equipment_code': 'B738', 'operated': True, 'scope': 'global_commercial'},
        {'flight_date': '2019-01-02', 'leg_id': 'B', 'equipment_code': 'B738', 'operated': 'yes', 'scope': 'global_commercial', 'vintage_id': 'v1'},
    ])
    assert out['diagnostics']['invalid_rows'] == 2
    assert out['complete_for_g2'] is False
