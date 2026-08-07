from pathlib import Path
import json
import re
from collections import Counter

RAW_PATH = Path('datasets/egyptian/raw/mdc_corpus.txt')
OUT_DIR = Path('datasets/egyptian/corpus')
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / 'egyptian_corpus_sequence.json'
MD_OUT = Path('reports/statistics/egyptian/egyptian_corpus_sequence_report_v2.md')

TOKEN_RE = re.compile(r'(?:Aa|[A-Z][a-z]?)[0-9]+[A-Z]?')

if not RAW_PATH.exists():
    print('M11.1B v2.0 Manuel de Codage import engine')
    print('==========================================')
    print('Source file not found:')
    print(RAW_PATH)
    raise SystemExit(1)

inscriptions = []
sign_counter = Counter()
lengths = []

for line in RAW_PATH.read_text(encoding='utf-8').splitlines():
    line = line.strip()
    if not line or line.startswith('#'):
        continue

    if ':' in line:
        ins_id, text = line.split(':', 1)
        ins_id = ins_id.strip()
    else:
        ins_id = f'E{len(inscriptions)+1:05d}'
        text = line

    clean = text.replace('\\\\', '')
    signs = TOKEN_RE.findall(clean)

    inscriptions.append({
        'id': ins_id,
        'signs': signs,
        'source': 'MdC',
        'confidence': 1.0
    })

    sign_counter.update(signs)
    lengths.append(len(signs))

corpus = {
    'corpus': 'Egyptian',
    'version': '2.0',
    'format': 'Manuel de Codage',
    'inscriptions': inscriptions,
    'statistics': {
        'inscription_count': len(inscriptions),
        'total_sign_tokens': sum(lengths),
        'unique_signs': len(sign_counter),
        'mean_length': round(sum(lengths)/len(lengths), 3) if lengths else 0,
        'max_length': max(lengths) if lengths else 0,
        'min_length': min(lengths) if lengths else 0,
    }
}

JSON_OUT.write_text(json.dumps(corpus, indent=2))

with open(MD_OUT, 'w', encoding='utf-8') as f:
    f.write('# Egyptian CorpusSequence Report v2.0\\n\\n')
    f.write(f'Format: Manuel de Codage (MdC)\\n')
    f.write(f'Inscriptions: {len(inscriptions)}\\n')
    f.write(f'Total sign tokens: {sum(lengths)}\\n')
    f.write(f'Unique signs: {len(sign_counter)}\\n')
    if lengths:
        f.write(f'Mean length: {sum(lengths)/len(lengths):.3f}\\n')

print('M11.1B v2.0 Manuel de Codage import engine')
print('==========================================')
print(f'Inscriptions      : {len(inscriptions)}')
print(f'Total sign tokens : {sum(lengths)}')
print(f'Unique signs      : {len(sign_counter)}')
print()
print(f'JSON corpus       : {JSON_OUT}')
print(f'Markdown report   : {MD_OUT}')
