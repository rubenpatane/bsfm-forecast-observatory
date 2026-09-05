import pytest
from bsfm.point_in_time import point_in_time,assert_no_future,eligible

def test_future_and_unknown_rows_are_excluded():
 rows=[{'id':'known','available_at':'2020-01-01T00:00:00Z'},{'id':'future','available_at':'2020-02-01T00:00:00Z'},{'id':'unknown'}]
 got=point_in_time(rows,'2020-01-15T00:00:00Z')
 assert [x['id'] for x in got]==['known']

def test_exact_cutoff_is_eligible():
 assert eligible({'available_at':'2020-01-15T00:00:00Z'},'2020-01-15T00:00:00Z')

def test_timezone_offsets_are_normalized():
 assert eligible({'available_at':'2020-01-15T01:00:00+01:00'},'2020-01-15T00:00:00Z')

def test_malformed_availability_fails_loudly():
 with pytest.raises(ValueError): eligible({'available_at':'not-a-time'},'2020-01-15T00:00:00Z')

def test_guard_rejects_future_or_unknown_as_leakage():
 with pytest.raises(ValueError,match='future leakage'):
  assert_no_future([{'available_at':'2021-01-02T00:00:00Z'}],'2021-01-01T00:00:00Z')
 with pytest.raises(ValueError,match='future leakage'):
  assert_no_future([{}],'2021-01-01T00:00:00Z')
