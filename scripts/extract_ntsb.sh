#!/usr/bin/env bash
set -euo pipefail
MDB=${1:?usage: extract_ntsb.sh path/to/avall.mdb [outdir]}
OUT=${2:-data/derived/ntsb}
mkdir -p "$OUT"
command -v mdb-tables >/dev/null
command -v mdb-export >/dev/null
mdb-tables -1 "$MDB" > "$OUT/tables.txt"
for table in events aircraft Occurrences findings; do
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
    with p.open(errors='replace',newline='') as f: rows=sum(1 for _ in csv.reader(f))-1
    files[p.name]={'rows':max(rows,0),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
(out/'manifest.json').write_text(json.dumps({'schema':'bsfm.ntsb-extract.v1','files':files},indent=2,sort_keys=True)+'\n')
PY
