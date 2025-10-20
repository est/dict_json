import json
import time
from pathlib import Path
from collections import Counter

import requests

whole: Counter[str] = Counter()
for p in Path('pub').rglob('*.txt'):
    with open(p) as f:
        for l in f:
            if w := l.strip():
                whole[w] += 1

for x in Path('out').rglob('*.json'):
    whole.pop(x.name.removesuffix('.json'), None)


sys_prompt="""
You are a linguistic expert providing dictionary and thesaurus service.
User inputs a WORD, fix misspelling, to lower case if possible, restore to base form i explain it and respond in strict raw JSON.
Do not wrap the JSON. Format is:
{
  "WORD": "", // the word to be explained
  "IPA": "/xxx/", // pronunciation in International Phonetic Alphabet. Make sure it's wrapped in double quotation marks
  "CONJUGATES": "", // inflections and such seprated by " | "
  "ETYMOLOGY": "", // example: "From Latin inspirare (in- 'into' + spirare 'breathe'), originally 'to breathe into, infuse spirit'"
  "SINCE": "", // approx. year or era the word first appeared
  "MEANINGS": [ // array of meanings
    {
      "PATTERN": "", // how to use WORD under this meaning, optionally applied with markers like [sb] [sth]. Example: if WORD is "inpure", one of the PATTERN is "inspire [sb]".
      "POS": "", // grammartically description of the PATTERN. example: "vtr + prep"
      "POS_TIP": "", // tooltip to explain like what is "vtr" and "prep"
      "TAGS": [], // core word, common/rare, old word? Be creative.
      "DEF_EN": "", // definition in simple, short English
      "DEF_ZH": "", // definition in simple, short Chinese (mainland)
      "SENT_EN": "", // example sentence in simple English
      "SENT_ZH": "", // example sentence in simple Chinese (mainland)
      "RELATED": [  // synonyms and antonyms under this meaning if any, also give "related" if similar or derivative word/brand/concept is more well known. Only list word itself in "V", no explain
        {"T": "synonyms", "V": ["encourage", "motivate"]},
        {"T": "antonyms", "V": ["defeat", "disinspire"]}
      ]
    }, {}, {}, ...  // other meanings, from most commonly used to least used
  ],
  "REGISTER": "", // where the word is commonly used
}"""

session  = requests.Session()
for i, w in enumerate(whole, start=1):
    if i < 1630: continue
    r = session.post('https://def.est.im/.lookup', params={'q': w})
    with open(f'out/{w}.json', 'w') as f:
        o = json.dumps(data, ensure_ascii=False, separators=',:', indent=2)
        b = f.write(o)
        print(f"{i}/{len(whole)}", w, b)
    i += 1
