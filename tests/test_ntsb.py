import csv
from bsfm.ntsb import normalize_row,join_events_aircraft

def test_ntsb_explicit_part121_is_commercial():
 r=normalize_row({'EventId':'x','EventDate':'01/01/2020','Make':'BOEING','Model':'737-800','TotalFatalInjuries':'2','far_part':'121','oper_sched':'SCHD'})
 assert r['boeing'] and r['fatal'] and r['commercial'] and r['scheduled_service']
 assert r['event_date']=='2020-01-01'
 assert r['available_at'] is None

def test_operator_name_alone_does_not_imply_commercial():
 r=normalize_row({'Make':'BOEING','Model':'737-800','oper_name':'Private Example LLC'})
 assert r['commercial'] is False
 assert r['scheduled_service'] is False

def test_event_aircraft_join(tmp_path):
 e=tmp_path/'events.csv'; a=tmp_path/'aircraft.csv'
 with e.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['ev_id','ev_date','inj_tot_f']); w.writeheader(); w.writerow({'ev_id':'E1','ev_date':'01/01/20 00:00:00','inj_tot_f':'1'})
 with a.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['ev_id','acft_make','acft_model','far_part','phase_flt_spec']); w.writeheader(); w.writerow({'ev_id':'E1','acft_make':'BOEING','acft_model':'737-800','far_part':'121','phase_flt_spec':'LDG'})
 r=join_events_aircraft(e,a)
 assert len(r)==1 and r[0]['boeing'] and r[0]['fatal'] and r[0]['commercial']
 assert r[0]['phase']=='LDG' and r[0]['event_date']=='2020-01-01'
