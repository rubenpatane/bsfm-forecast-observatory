from datetime import date, timedelta
import json
from pathlib import Path

from bsfm.public_data_backtest import seasonal_naive_daily_path, run_exploratory_backtest

ROOT = Path(__file__).resolve().parents[1]


def test_daily_path_uses_latest_lag_eligible_same_month_and_preserves_daily_rate():
    monthly = [
        {'period': '2020-01', 'cohort': '737', 'departures': 310.0},
        {'period': '2021-01', 'cohort': '737', 'departures': 620.0},
    ]
    rows = seasonal_naive_daily_path(monthly, ['737'], '2023-01-01', 2, '2022-12-31', 365)
    assert [r['source_period'] for r in rows] == ['2021-01', '2021-01']
    assert rows[0]['exposure_by_cohort']['737'] == 20.0


def test_checked_in_backtest_executes_but_fails_frozen_power_rule():
    spec = json.loads((ROOT / 'config/model-public-data-v1.3.json').read_text())
    outcomes = json.loads((ROOT / 'data/census/public-data-v1.3-outcomes.json').read_text())['events']
    exposure = json.loads((ROOT / 'data/exposure/bts-t100-2010-2025-audit.json').read_text())['prospective_merged_cohort_candidate']
    report = run_exploratory_backtest(outcomes, exposure['exposure_rows'], exposure['monthly_exposure_rows'], spec['cohorts'], spec)
    assert report['status'] == 'EXPLORATORY_COMPLETE'
    assert report['fold_count'] >= 40
    assert report['event_bearing_fold_count'] == 3
    assert report['scientific_validation'] == 'BLOCKED_INSUFFICIENT_EVENT_FOLDS'
    assert report['minimum_event_bearing_folds'] == 10
