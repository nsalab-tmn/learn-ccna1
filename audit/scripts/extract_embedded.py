"""Extract base64 rasters embedded in tracked SVGs, deduplicated by sha1. Usage: extract_embedded.py OUT_DIR"""
import re, hashlib, subprocess, base64, sys, os, json
REPO = os.environ.get('AUDIT_REPO') or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
files = subprocess.run(['git','ls-files','*.svg'],capture_output=True,text=True,cwd=REPO).stdout.split()
pat = re.compile(r'<image[^>]*?href="data:([^;]+);base64,([^"]+)"', re.S)
seen = {}
for f in files:
    s = open(os.path.join(REPO,f), encoding='utf-8', errors='replace').read()
    for m in pat.finditer(s):
        h = hashlib.sha1(m.group(2).encode()).hexdigest()[:10]
        if h not in seen:
            ext = 'png' if 'png' in m.group(1) else 'jpg'
            open(os.path.join(OUT, f'{h}.{ext}'),'wb').write(base64.b64decode(m.group(2)))
            seen[h] = {'mime': m.group(1), 'files': []}
        seen[h]['files'].append(f)
json.dump(seen, open(os.path.join(OUT,'index.json'),'w'), indent=1, ensure_ascii=False)
for h,v in sorted(seen.items(), key=lambda kv:-len(kv[1]['files'])):
    print(h, len(v['files']), v['files'][:3])
