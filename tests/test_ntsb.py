import csv
from bsfm.ntsb import normalize_row, join_events_aircraft, load_event_sequence_phase_map


def test_ntsb_explicit_part121_is_commercial():
    r = normalize_row({'EventId':'x','EventDate':'01/01/2020','Make':'BOEING','Model':'737-800','TotalFatalInjuries':'2','far_part':'121','oper_sched':'SCHD'})
    assert r['boeing'] and r['fatal'] and r['commercial'] and r['scheduled_service']
    assert r['event_date'] == '2020-01-01'
    assert r['available_at'] is None


def test_ntsb_nusc_is_commercial_by_official_dictionary_code():
    r = normalize_row({'Make':'BOEING','Model':'737','far_part':'NUSC'})
    assert r['commercial'] is True


def test_external_ground_fatality_makes_event_fatal_without_rewriting_count():
    r = normalize_row({'Make':'BOEING','Model':'777','inj_tot_f':'0','inj_f_grnd':'1','far_part':'NUSC'})
    assert r['fatalities'] == 0
    assert r['ground_fatalities'] == 1
    assert r['fatal'] is True and r['external_fatality_present'] is True


def test_operator_name_alone_does_not_imply_commercial():
    r = normalize_row({'Make':'BOEING','Model':'737-800','oper_name':'Private Example LLC'})
    assert r['commercial'] is False


def write(path, fields, row):
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerow(row)


def test_phase_recovery_uses_official_event_sequence_dictionary(tmp_path):
    e=tmp_path/'events.csv'; a=tmp_path/'aircraft.csv'; s=tmp_path/'seq.csv'; d=tmp_path/'dict.csv'
    write(e,['ev_id','ev_date','inj_tot_f'],{'ev_id':'E1','ev_date':'01/02/20 00:00:00','inj_tot_f':'1'})
    write(a,['ev_id','Aircraft_Key','acft_make','acft_model','far_part'],{'ev_id':'E1','Aircraft_Key':'7','acft_make':'BOEING','acft_model':'737-800','far_part':'121'})
    write(s,['ev_id','Aircraft_Key','Occurrence_No','Occurrence_Code','Occurrence_Description','phase_no','eventsoe_no','Defining_ev'],{'ev_id':'E1','Aircraft_Key':'7','Occurrence_No':'1','Occurrence_Code':'502250','Occurrence_Description':'Approach-IFR final approach Midair collision','phase_no':'502','eventsoe_no':'250','Defining_ev':'1'})
    write(d,['Table','Column','code_iaids','meaning'],{'Table':'Events_Sequence','Column':'Occurrence_Code','code_iaids':'502xxx','meaning':'Approach-IFR Final Approach'})
    assert load_event_sequence_phase_map(d) == {'502':'Approach-IFR Final Approach'}
    r=join_events_aircraft(e,a,sequence_csv=s,data_dictionary_csv=d)[0]
    assert r['phase'] == 'Approach-IFR Final Approach'
    assert r['phase_recovered_code'] == '502'
    assert r['phase_recovery_source'] == 'Events_Sequence.Occurrence_Code'


def test_unknown_sequence_code_is_not_heuristically_guessed(tmp_path):
    e=tmp_path/'events.csv'; a=tmp_path/'aircraft.csv'; s=tmp_path/'seq.csv'; d=tmp_path/'dict.csv'
    write(e,['ev_id','ev_date'],{'ev_id':'E1','ev_date':'01/02/20 00:00:00'})
    write(a,['ev_id','Aircraft_Key','acft_make'],{'ev_id':'E1','Aircraft_Key':'1','acft_make':'BOEING'})
    write(s,['ev_id','Aircraft_Key','Occurrence_No','Occurrence_Code','Occurrence_Description','phase_no','eventsoe_no','Defining_ev'],{'ev_id':'E1','Aircraft_Key':'1','Occurrence_No':'1','Occurrence_Code':'999999','Occurrence_Description':'Landing-looking free text','phase_no':'999','eventsoe_no':'999','Defining_ev':'1'})
    write(d,['Table','Column','code_iaids','meaning'],{'Table':'Events_Sequence','Column':'Occurrence_Code','code_iaids':'502xxx','meaning':'Approach-IFR Final Approach'})
    r=join_events_aircraft(e,a,sequence_csv=s,data_dictionary_csv=d)[0]
    assert r['phase_recovered'] is None


def test_missing_foreign_operation_code_stays_unknown_not_noncommercial():
    r=normalize_row({'Make':'BOEING','Model':'777','far_part':'','oper_sched':'','oper_name':'Airline Name'})
    assert r['commercial'] is False
    assert r['commercial_status']=='unknown'


def test_nusn_is_explicitly_noncommercial():
    r=normalize_row({'Make':'BOEING','Model':'737','far_part':'NUSN'})
    assert r['commercial_status']=='noncommercial'
