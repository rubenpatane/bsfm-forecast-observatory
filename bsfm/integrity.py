import hashlib,json
from pathlib import Path
def canonical_json(d): return json.dumps(d,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def digest(d): return "sha256:"+hashlib.sha256(canonical_json(d)).hexdigest()
def read_json(p:Path): return json.loads(p.read_text(encoding="utf-8"))
def write_json_atomic(p:Path,d):
 p.parent.mkdir(parents=True,exist_ok=True); t=p.with_suffix(p.suffix+".tmp"); t.write_text(json.dumps(d,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8"); t.replace(p)
