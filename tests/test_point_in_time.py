import pytest
from bsfm.point_in_time import point_in_time,assert_no_future

def test_future_rows_are_excluded():
 rows=[{'id':'known','available_at':'2020-01-01T00:00:00Z'},{'id':'future','available_at':'2020-02-01T00:00:00Z'},{'id':'unknown'}]
 got=point_in_time(rows,'2020-01-15T00:00:00Z')
 assert [x['id'] for x in got]==['known']

def test_guard_rejects_leakage():
 with pytest.raises(ValueError,match='future leakage'):
  assert_no_future([{'available_at':'2021-01-02T00:00:00Z'}],'2021-01-01T00:00:00Z')
