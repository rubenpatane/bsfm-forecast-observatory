from bsfm.ntsb import normalize_row

def test_ntsb_normalization_preserves_availability():
 r=normalize_row({'EventId':'x','EventDate':'01/01/2020','PublicationDate':'02/01/2020','Make':'BOEING','Model':'737-800','TotalFatalInjuries':'2','AirCarrier':'Example Air'})
 assert r['boeing'] and r['fatal'] and r['commercial']
 assert r['available_at']=='02/01/2020'

def test_unknown_commercial_is_not_assumed():
 r=normalize_row({'Make':'BOEING','Model':'737-800'})
 assert r['commercial'] is False
 assert r['available_at'] is None
