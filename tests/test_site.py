import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def test_observatory_pages_and_shared_styles_exist():
    for name in ('index.html','validation.html','methodology.html','provenance.html','styles.css'):
        assert (ROOT/'site'/name).is_file()


def test_public_readiness_seed_is_fail_closed():
    state=json.loads((ROOT/'site/data/final-readiness.json').read_text())
    assert state['scientific_fit_ready'] is False
    assert state['scientific_promotion_ready'] is False
    assert state['absolute_accident_probabilities_enabled'] is False
    assert state['validated_prediction_claim_allowed'] is False
    assert not any(state['gates'].values())


def test_site_exposes_research_limitations_and_dynamic_state():
    index=(ROOT/'site/index.html').read_text()
    assert 'Experimental research' in index
    assert 'not an operational safety tool' in index
    assert './data/status.json' in index
    assert './data/final-readiness.json' in index
    assert 'F-002' in index


def test_single_workflow_generates_and_deploys_site():
    workflows=list((ROOT/'.github/workflows').glob('*.yml'))+list((ROOT/'.github/workflows').glob('*.yaml'))
    assert len(workflows)==1
    text=workflows[0].read_text()
    assert text.startswith('name: AGGIORNA\n')
    assert "Path('site/data/final-readiness.json').write_text" in text
    assert 'git add site/data data/manifests forecasts evaluations' in text
    assert 'actions/upload-pages-artifact@v3' in text
    assert 'actions/deploy-pages@v4' in text
