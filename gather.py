from pathlib import Path
from collections import Counter

whole = Counter()
for p in Path('pub').rglob('*.txt'):
    with open(p) as f:
        for l in f:
            if w := l.strip():
                whole[w] += 1
