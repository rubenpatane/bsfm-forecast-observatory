from bsfm.historical_label_pipeline import build

def test_pipeline_has_six_steps_and_separates_pit():
 d=build()
 assert d['steps']==['extract','normalize','link','provenance','separate_descriptive_from_pit','emit_training_dataset']
 assert d['row_count']>0
 assert all('pit_status' in r and 'labels' in r for r in d['rows'])
