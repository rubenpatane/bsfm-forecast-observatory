"""Development training entry point for the expanded Model 1.5 candidate."""
import json
from datetime import date
from pathlib import Path
from .cohorts import boeing_cohort, cohort_from_icao_equipment
from .evidence_bundle import build_development_bundle
from .estimator import fit_shrunk_hazard, predict_cohort
from .feature_model import fit_feature_distributions
from .g1_census import load_integrated_candidates
from .model_features import build_snapshot, build_unified_feature_table
from .time_to_event import predict_time_to_event


def train(root=Path("."), cutoff="2026-09-06"):
    root = Path(root); c = date.fromisoformat(cutoff)
    candidates = load_integrated_candidates(root)["rows"]
    ledger = {x["event_id"]: x for x in json.loads((root / "data/pit/g1-outcome-publication-ledger.json").read_text())["events"]}
    raw = [dict(e, available_at=ledger.get(e["event_id"], {}).get("available_at")) for e in candidates
           if e.get("decision") == "include" and ledger.get(e["event_id"], {}).get("available_at")
           and str(e["event_date"])[:10] <= cutoff and str(ledger[e["event_id"]]["available_at"])[:10] <= cutoff]
    snapshot = build_snapshot(raw, cutoff)
    unified = build_unified_feature_table(root, cutoff)
    if unified:
        snapshot = unified
    cohorts = ["727", "737-all-variants", "747", "757", "767", "777", "787"]
    exposure = json.loads((root / "data/exposure/g2-scoped-baseline-candidate-v1.json").read_text())
    exp = [{"cohort": r["cohort"], "departures": r["sectors"]} for r in exposure["rows"]]
    prior = []
    for row in raw:
        fam = boeing_cohort(row.get("model"))
        if fam: prior.append({"cohort": "737-all-variants" if fam.startswith("737-") else fam})
    hazard = fit_shrunk_hazard(prior, exp, cohorts)
    family = predict_cohort(hazard, {r["cohort"]: r["departures"] for r in exp})
    bundle = build_development_bundle(root)
    daily = []
    for d, values in bundle["euronova_daily_boeing"].items():
        agg = {c: 0 for c in cohorts}
        for typ, n in values.items():
            fam = cohort_from_icao_equipment(typ)
            if fam: agg["737-all-variants" if fam.startswith("737-") else fam] += n
        daily.append({"date": d, **agg})
    tte = predict_time_to_event(hazard, daily, daily[0]["date"], len(daily))
    out = {"schema":"bsfm.model-1.5-trained-development.v2", "model_version":"1.5-scoped",
           "training_cutoff":cutoff, "training_rows":len(snapshot), "status":"development_trained",
           "family_prediction":family, "time_to_event":{k:tte[k] for k in ("start_date","horizon_days","horizon_end","modal_date","event_probability","no_event_probability")},
           "feature_distributions":fit_feature_distributions(snapshot), "daily_exposure_source":"EuroNOVA 2022 regional sensitivity", "global_denominator":False,
           "development_sources":{"opdi_daily_rows": bundle.get("sources", {}).get("opdi_daily", {}).get("rows", 0),
                                  "opdi_global_denominator": bundle.get("sources", {}).get("opdi_daily", {}).get("global_denominator", False),
                                  "iata_context_reports": len((bundle.get("iata_safety_context") or {}).get("reports", [])),
                                  "iata_event_level_join": (bundle.get("iata_safety_context") or {}).get("event_level_join", False)},
           "promotion_allowed":False, "frozen_forecasts_unchanged":True}
    (root / "data/model").mkdir(exist_ok=True); (root / "data/model/model-1.5-trained-development-v2.json").write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
    return out


if __name__ == "__main__":
    print(json.dumps(train(), indent=2))
