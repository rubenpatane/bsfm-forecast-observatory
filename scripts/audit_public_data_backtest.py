#!/usr/bin/env python3
"""Execute the versioned BSFM-PD 1.3 exploratory backtest."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bsfm.public_data_backtest import run_exploratory_backtest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output')
    args = parser.parse_args()
    spec = json.loads((ROOT / 'config/model-public-data-v1.3.json').read_text())
    outcomes = json.loads((ROOT / 'data/census/public-data-v1.3-outcomes.json').read_text())['events']
    exposure = json.loads((ROOT / 'data/exposure/bts-t100-2010-2025-audit.json').read_text())['prospective_merged_cohort_candidate']
    report = run_exploratory_backtest(outcomes, exposure['exposure_rows'], exposure['monthly_exposure_rows'], spec['cohorts'], spec)
    rendered = json.dumps(report, indent=2, sort_keys=True) + '\n'
    if args.output:
        Path(args.output).write_text(rendered, encoding='utf-8')
    else:
        print(rendered, end='')


if __name__ == '__main__':
    main()
