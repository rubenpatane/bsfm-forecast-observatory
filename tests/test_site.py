import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_observatory_pages_and_shared_assets_exist():
 for name in ('index.html','validation.html','methodology.html','provenance.html','styles.css','i18n.js'):
  assert (ROOT/'site'/name).is_file()

def test_public_readiness_seed_is_fail_closed():
 state=json.loads((ROOT/'site/data/final-readiness.json').read_text())
 assert state['scientific_fit_ready'] is False
 assert state['scientific_promotion_ready'] is False
 assert state['absolute_accident_probabilities_enabled'] is False
 assert state['validated_prediction_claim_allowed'] is False
 assert not any(state['gates'].values())

def test_all_pages_have_persistent_bilingual_controls():
 for name in ('index.html','validation.html','methodology.html','provenance.html'):
  text=(ROOT/'site'/name).read_text()
  assert './i18n.js' in text
  assert 'data-lang="it"' in text and 'data-lang="en"' in text
  assert 'data-i18n="overview"' in text
 js=(ROOT/'site/i18n.js').read_text()
 assert 'localStorage' in js and "searchParams.set('lang'" in js
 assert 'ITA' not in js or 'it' in js

def test_site_exposes_frozen_forecast_refinements_and_evidence_state():
 index=(ROOT/'site/index.html').read_text()
 assert 'Experimental research' in index and 'not an operational safety tool' in index
 assert 'F-002' in index and 'R-F002-*' in index
 assert './data/refinements.json' in index
 assert './data/evidence-state.json' in index
 assert 'not counted in its original score' in index

def test_single_workflow_generates_evidence_refinements_and_deploys_site():
 workflows=list((ROOT/'.github/workflows').glob('*.yml'))+list((ROOT/'.github/workflows').glob('*.yaml'))
 assert len(workflows)==1
 text=workflows[0].read_text()
 assert text.startswith('name: AGGIORNA\n')
 assert 'write_evidence_state' in text
 assert 'write_public_refinements' in text
 assert 'git add site/data data/manifests forecasts evaluations' in text
 assert 'actions/upload-pages-artifact@v3' in text and 'actions/deploy-pages@v4' in text
