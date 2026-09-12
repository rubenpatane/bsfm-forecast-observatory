#!/usr/bin/env python3
"""Issue or retain the active BSFM-PD 1.4 prospective research forecast."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bsfm.public_data_forecast import execute_public_data_forecast, evaluate_public_data_forecasts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--issued-at")
    args = parser.parse_args()
    forecast = execute_public_data_forecast(ROOT, args.issued_at)
    evaluation = evaluate_public_data_forecasts(ROOT, args.issued_at)
    print(json.dumps({"forecast": forecast, "prospective_evaluation": evaluation}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
