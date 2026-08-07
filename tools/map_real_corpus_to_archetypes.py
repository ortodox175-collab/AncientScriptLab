from pathlib import Path
import json
from collections import Counter

CORPUS_PATH = Path('datasets/egyptian/corpus/egyptian_corpus_sequence.json')
HIER_PATH = Path('reports/statistics/egyptian/hierarchical_archetypes.json')
OUT_DIR = Path('datasets/egyptian/sequences')
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / 'real_archetype_sequences.json'
MD_OUT = Path('reports/statistics/egyptian/real_archetype_sequence_report_v1.md')

corpus = json.loads(CORPUS_PATH.read_text())
hier = json.loads(HIER_PATH.read_text())

mapping = {}

for macro in hier['hierarchy']:
    ma = macro['macro_archetype']
    for meso in macro['meso_archetypes']:
        me = meso['meso_archetype']
        for micro in meso['micro_archetypes']:
            mi = micro['micro_archetype']
            for s in micro['sample_signs']:
                mapping[s] = {
                    'macro': ma,
                    'meso': me,
                    'micro': mi,
                }

macro_counter = Counter()
meso_counter = Counter()
micro_counter = Counter()

mapped_tokens = 0
unmapped_tokens = 0
unmapped_signs = Counter()

out = []

for ins in corpus['inscriptions']:
    macro_seq = []
    meso_seq = []
    micro_seq = []

    for sign in ins['signs']:
        a = mapping.get(sign)
        if a is None:
            macro_seq.append(None)
            meso_seq.append(None)
            micro_seq.append(None)
            unmapped_tokens += 1
            unmapped_signs[sign] += 1
        else:
            macro_seq.append(a['macro'])
            meso_seq.append(a['meso'])
            micro_seq.append(a['micro'])
            macro_counter[a['macro']] += 1
            meso_counter[a['meso']] += 1
            micro_counter[a['micro']] += 1
            mapped_tokens += 1

    out.append({
        'id': ins['id'],
        'sign_sequence': ins['signs'],
        'macro_sequence': macro_seq,
        'meso_sequence': meso_seq,
        'micro_sequence': micro_seq,
    })

coverage = mapped_tokens / (mapped_tokens + unmapped_tokens) if (mapped_tokens + unmapped_tokens) else 0

result = {
    'module': 'M11.2A Real Corpus Archetype Mapping',
    'inscriptions': len(out),
    'mapped_tokens': mapped_tokens,
    'unmapped_tokens': unmapped_tokens,
    'coverage': coverage,
    'macro_distribution': dict(macro_counter),
    'meso_distribution': dict(meso_counter),
    'micro_distribution': dict(micro_counter),
    'top_unmapped_signs': unmapped_signs.most_common(30),
    'archetype_sequences': out,
}

JSON_OUT.write_text(json.dumps(result, indent=2))

with open(MD_OUT, 'w', encoding='utf-8') as f:
    f.write('# Real archetype sequence report v1.0\\n\\n')
    f.write(f'Inscriptions: {len(out)}\\n')
    f.write(f'Mapped tokens: {mapped_tokens}\\n')
    f.write(f'Unmapped tokens: {unmapped_tokens}\\n')
    f.write(f'Coverage: {coverage:.3f}\\n\\n')
    f.write('## Top unmapped signs\\n\\n')
    for sign, count in unmapped_signs.most_common(20):
        f.write(f'- {sign}: {count}\\n')

print('M11.2A Real Corpus Archetype Mapping')
print('====================================')
print(f'Inscriptions      : {len(out)}')
print(f'Mapped tokens     : {mapped_tokens}')
print(f'Unmapped tokens   : {unmapped_tokens}')
print(f'Coverage          : {coverage:.3f}')
print()
print(f'JSON dataset      : {JSON_OUT}')
print(f'Markdown report   : {MD_OUT}')
