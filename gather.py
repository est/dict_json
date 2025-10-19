import json
from pathlib import Path
from collections import Counter

import requests

whole = Counter()
for p in Path('pub').rglob('*.txt'):
    with open(p) as f:
        for l in f:
            if w := l.strip():
                whole[w] += 1

session  = requests.Session()
for i, w in enumerate(whole, start=1):
    r = session.post('https://def.est.im/.lookup', params={'q': w})
    with open(f'out/{w}.json', 'w') as f:
        o = json.dumps(r.json().get('result'), ensure_ascii=False, separators=',:', indent=2)
        b = f.write(o)
        print(f"{i}/{len(whole)}", w, b)
