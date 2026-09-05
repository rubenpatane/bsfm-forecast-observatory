import csv
from bsfm.ntsb import normalize_row,join_events_aircraft

def test_ntsb_normalization_preserves_availability():
 r=normalize_row({'EventId':'x','EventDate':'01/01/2020','PublicationDate':'02/01/2020','Make':'BOEING','Model':'737-800','TotalFatalInjuries':'2','AirCarrier':'Example Air'})
 assert r['boeing'] and r['fatal'] and r['commercial']
 assert r['available_at']=='02/01/2020'

def test_unknown_commercial_is_not_assumed():
 r=normalize_row({'Make':'BOEING','Model':'737-800'})
 assert r['commercial'] is False
 assert r['available_at'] is None

def test_event_aircraft_join(tmp_path):
 e=tmp_path/'events.csv'; a=tmp_path/'aircraft.csv'
 with e.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['ev_id','ev_date','inj_tot_f']); w.writeheader(); w.writerow({'ev_id':'E1','ev_date':'2020-01-01','inj_tot_f':'1'})
 with a.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['ev_id','acft_make','acft_model','far_part']); w.writeheader(); w.writerow({'ev_id':'E1','acft_make':'BOEING','acft_model':'737-800','far_part':'121'})
 r=join_events_aircraft(e,a)
 assert len(r)==1 and r[0]['boeing'] and r[0]['fatal'] and r[0]['commercial']
