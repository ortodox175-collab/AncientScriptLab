from pathlib import Path
import json
import re
from collections import Counter

IN_PATH = Path('datasets/egyptian/corpus/egyptian_corpus_sequence.json')
OUT_PATH = Path('datasets/egyptian/corpus/egyptian_corpus_sequence_clean.json')

data = json.loads(IN_PATH.read_text())

# Допустимые Gardiner-коды: A1, A5A, Aa16, NL5, NU3 и т.д.
TOKEN_RE = re.compile(r'^(Aa|NL|NU|[A-Z])(\d+)([A-Z]?)$')

removed = 0
normalized = 0
all_signs = []

for ins in data['inscriptions']:
    cleaned = []

    for token in ins['signs']:
        token = token.strip()

        # удалить внутренние технические токены
        if token.startswith('Ff'):
            removed += 1
            continue

        m = TOKEN_RE.match(token)
        if not m:
            removed += 1
            continue

        prefix, number, suffix = m.groups()
        norm = f'{prefix}{int(number)}{suffix}'

        if norm != token:
            normalized += 1

        cleaned.append(norm)
        all_signs.append(norm)

    ins['signs'] = cleaned

counter = Counter(all_signs)

data['statistics'] = {
    'inscriptions': len(data['inscriptions']),
    'total_sign_tokens': len(all_signs),
    'unique_signs': len(counter),
    'average_length': (
        sum(len(i['signs']) for i in data['inscriptions']) /
        len(data['inscriptions'])
        if data['inscriptions'] else 0
    )
}

OUT_PATH.write_text(json.dumps(data, indent=2))

print('M11.1B Corpus normalization')
print('===========================')
print('Inscriptions :', len(data['inscriptions']))
print('Removed      :', removed)
print('Normalized   :', normalized)
print('Unique signs :', len(counter))
print('Output       :', OUT_PATH)
