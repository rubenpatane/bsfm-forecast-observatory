import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PAGES=('index.html','forecast.html','validation.html','methodology.html','provenance.html')

def test_observatory_pages_and_shared_assets_exist():
 for name in (*PAGES,'styles.css','i18n.js','page-copy.js','comparables.js','forecast.js','validation-results.js'):
  assert (ROOT/'site'/name).is_file()
 assert (ROOT/'site/data/research-state.json').is_file()

def test_public_readiness_seed_is_fail_closed():
 state=json.loads((ROOT/'site/data/final-readiness.json').read_text())
 assert state['scientific_fit_ready'] is False
 assert state['scientific_promotion_ready'] is False
 assert state['absolute_accident_probabilities_enabled'] is False
 assert state['validated_prediction_claim_allowed'] is False
 assert not any(state['gates'].values())

def test_all_pages_have_complete_bilingual_controls_and_mobile_menu():
 for name in PAGES:
  text=(ROOT/'site'/name).read_text()
  assert '<html lang="it"' in text
  assert './i18n.js' in text
  assert 'data-lang="it"' in text and 'data-lang="en"' in text
  assert 'data-i18n="overview"' in text
  assert 'data-i18n="forecast"' in text
  assert 'class="menu-toggle"' in text
  assert 'class="nav-menu"' in text
  assert 'aria-expanded="false"' in text
 js=(ROOT/'site/i18n.js').read_text()
 assert 'localStorage' in js and "searchParams.set('lang'" in js
 assert "localStorage.getItem('bsfm-lang')" in js
 assert "navigator.language" in js
 assert "menu.classList.toggle('open')" in js
 assert 'bsfm-language' in js
 css=(ROOT/'site/styles.css').read_text()
 assert '@media(max-width:820px)' in css
 assert '.menu-toggle{display:none' in css
 assert '.nav-menu.open{display:flex' in css
 assert '.nav-menu>.lang{display:flex' in css
 assert '.nav-menu>.navlink,.nav-menu>.nav-update{display:none}' in css

def test_global_navigation_exposes_source_and_last_update():
 js=(ROOT/'site/i18n.js').read_text()
 assert "https://github.com/rubenpatane/bsfm-forecast-observatory" in js
 assert "className='navlink code-link'" in js
 assert "data/real-data.json" in js and "data/comparable-cases.json" in js
 assert "site-update-bar" in js and "nav-update" in js
 assert "Europe/Rome" in js
 assert "updated:'Ultimo aggiornamento'" in js
 assert "updated:'Last updated'" in js

def test_home_explains_observatory_and_exposes_real_acquired_data():
 index=(ROOT/'site/index.html').read_text()
 assert 'Ricerca sperimentale' in index and 'non è uno strumento operativo di sicurezza' in index
 assert 'Che cos’è BSFM' in index and 'Come funziona' in index
 assert 'F-002' in index and 'R-F002-*' in index
 assert './data/refinements.json' in index
 assert './data/evidence-state.json' in index
 assert './data/real-data.json' in index
 assert 'FAA SDR' in index and 'NTSB AVALL' in index
 assert 'non è necessariamente un incidente' in index
 assert 'latestReports' in index and 'topModels' in index and 'ntsbStats' in index
 assert 'Geografia descrittiva' in index and 'Operatore' in index and 'MSN' in index

def test_home_loads_generated_nonfatal_comparables():
 index=(ROOT/'site/index.html').read_text()
 js=(ROOT/'site/comparables.js').read_text()
 assert './comparables.js' in index
 assert './data/comparable-cases.json' in js
 assert './data/real-data.json' in js
 assert 'similar_boeing_reports' in js
 assert 'Confronto descrittivo ≠ validazione' in js
 assert 'non modifica il suo punteggio' in js
 assert 'const CASES=' not in js

def test_methodology_exposes_versioned_automatic_research_cycle():
 html=(ROOT/'site/methodology.html').read_text()
 js=(ROOT/'site/research-cycle.js').read_text()
 assert 'research-cycle.js' in html
 assert 'Riaffinamento parametri' in html and 'Distribuzione temporale' in html
 assert './data/research-cycle.json' in js
 assert 'minimal shrinkage estimator' in html
 assert 'Gamma–Poisson shrinkage' in js
 assert 'P(T=d) = S(d−1)' in js
 assert 'Rolling-origin refit at every cutoff' in js

def test_translation_dictionary_covers_all_public_page_keys():
 base=(ROOT/'site/i18n.js').read_text()
 page_copy=(ROOT/'site/page-copy.js').read_text()
 extension=(ROOT/'site/comparables.js').read_text()
 dictionaries=base+'\n'+page_copy+'\n'+extension
 for name in PAGES:
  text=(ROOT/'site'/name).read_text()
  import re
  for key in re.findall(r'data-i18n="([^"]+)"',text):
   assert dictionaries.count(key+':')>=2, (name,key)

def test_single_workflow_generates_real_data_evidence_refinements_comparables_and_deploys_site():
 workflows=list((ROOT/'.github/workflows').glob('*.yml'))+list((ROOT/'.github/workflows').glob('*.yaml'))
 assert len(workflows)==1
 text=workflows[0].read_text()
 assert text.startswith('name: AGGIORNA\n')
 assert 'write_evidence_state' in text
 assert 'write_public_refinements' in text
 assert 'write_public_comparables' in text
 assert 'write_public_research_state' in text
 assert 'write_public_forecast' in text
 assert "site/data/real-data.json" in text
 assert "'ntsb_snapshot'" in text
 assert 'git add site/data data/manifests forecasts evaluations' in text
 assert 'actions/upload-pages-artifact@v3' in text and 'actions/deploy-pages@v4' in text

def test_public_copy_does_not_claim_scientific_validation():
 index=(ROOT/'site/index.html').read_text().lower()
 validation=(ROOT/'site/validation.html').read_text().lower()
 assert 'fino a quando le evidenze richieste non sono complete' in index
 assert 'resta esplicitamente bloccato' in index
 assert 'un’esecuzione software verde non può trasformare' in validation

def test_validation_page_exposes_current_evidence_boundaries():
 text=(ROOT/'site/validation.html').read_text()
 assert '35/35' in text and '14/16' in text
 assert 'faa_sdr_precursors' in text
 assert 'minimal shrinkage estimator' in text
 assert './data/research-state.json' in text

def test_forecast_page_exposes_frozen_record_and_descriptive_boundaries():
 text=(ROOT/'site/forecast.html').read_text()
 assert './data/forecast.json' in (ROOT/'site/forecast.js').read_text()
 assert 'Geografia descrittiva' in text and 'Operatore' in text and 'MSN' in text
 assert 'Non previsto' in text and 'non sono successi valutabili' in text
 assert 'F-002 è immutabile' in text
 assert '7c34f318d7df9d942698e01783e86794a46509ca33c8fae9b156a50f8def4f48' in text
 assert './comparables.js' in text

def test_validation_page_renders_machine_readable_negative_result():
 text=(ROOT/'site/validation.html').read_text()
 js=(ROOT/'site/validation-results.js').read_text()
 assert './data/public-data-validation.json' in js
 assert 'Il candidato non supera la baseline' in text
 assert 'candidateScore' in text and 'baselineScore' in text
 assert 'Campione insufficiente: 3 su 10' in text

def test_complete_pages_explain_model_lineage_and_machine_readable_artifacts():
 method=(ROOT/'site/methodology.html').read_text()
 provenance=(ROOT/'site/provenance.html').read_text()
 assert 'BSFM 1.2' in method and 'minimal_shrunk_hazard_v1' in method and 'BSFM-PD 1.3' in method
 assert 'Le regole non cambiano da sole' in method
 for artifact in ('forecast.json','research-state.json','public-data-validation.json','research-cycle.json','final-readiness.json','evidence-state.json'):
  assert artifact in provenance

def test_pages_have_accessible_landmarks_and_reduced_motion_support():
 for name in PAGES:
  text=(ROOT/'site'/name).read_text()
  assert 'class="skip-link"' in text
  assert 'id="content"' in text
  assert '<main' in text and '<footer' in text
 css=(ROOT/'site/styles.css').read_text()
 assert 'prefers-reduced-motion:reduce' in css
