#!/usr/bin/env bash
set -euo pipefail
MDB=${1:?usage: extract_ntsb.sh path/to/avall.mdb [outdir]}
OUT=${2:-data/derived/ntsb}
mkdir -p "$OUT"
command -v mdb-tables >/dev/null
command -v mdb-export >/dev/null
mdb-tables -1 "$MDB" > "$OUT/tables.txt"
# Export research-relevant tables. NTSB_Admin/dt_* are included specifically to audit
# report/publication/change timing; they must never be treated as historical available_at
# merely because a timestamp exists. Sequence/findings tables enrich outcome labels only.
for table in events aircraft Occurrences Findings Events_Sequence seq_of_events dt_events dt_aircraft NTSB_Admin engines injury eADMSPUB_DataDictionary narratives; do
  if grep -Fxiq "$table" "$OUT/tables.txt"; then
    actual=$(grep -Fxi "$table" "$OUT/tables.txt" | head -1)
    mdb-export "$MDB" "$actual" > "$OUT/${table}.csv"
  fi
done
python - "$OUT" <<'PY'
import csv,json,hashlib,sys
from pathlib import Path
out=Path(sys.argv[1]); files={}
for p in sorted(out.glob('*.csv')):
    with p.open(errors='replace',newline='') as f:
        reader=csv.reader(f); header=next(reader,[]); rows=sum(1 for _ in reader)
    files[p.name]={'rows':rows,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'fields':header}
(out/'manifest.json').write_text(json.dumps({'schema':'bsfm.ntsb-extract.v2','files':files},indent=2,sort_keys=True)+'\n')
PY
