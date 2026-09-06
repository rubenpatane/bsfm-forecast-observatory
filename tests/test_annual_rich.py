from bsfm.annual_rich import validate_rich_annual_evidence


def test_rich_event_allows_unknown_values_but_requires_explicit_keys_and_provenance():
    event={'event_id':'x','date':'2014-01-01','flight_number':None,'model':'777','registration':'X','msn':None,'operator':'Y','phase':None,'geography':'Z','decision':'unresolved','provenance':[{'publisher':'authority'}]}
    assert validate_rich_annual_evidence({'year':2014,'events':[event]})['valid']


def test_rich_event_missing_key_fails_closed():
    event={'event_id':'x','date':'2014-01-01','decision':'include','provenance':[{'publisher':'authority'}]}
    audit=validate_rich_annual_evidence({'year':2014,'events':[event]})
    assert not audit['valid'] and any(x.startswith('missing_event_model') for x in audit['errors'])
