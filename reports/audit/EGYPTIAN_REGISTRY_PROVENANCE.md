# AncientScriptLab — Egyptian Registry Legacy Provenance

Status: historical provenance record before removal of obsolete
Gardiner / UniKemet registry builders.

## Principle

These scripts document experimental attempts to construct Egyptian
sign registries. None of them is accepted as canonical Core.

External labels, descriptions, categories and functions are metadata.
They are not measurement features and must not influence geometric,
topological or other sign measurements.

The current canonical Egyptian dataset is isolated under:

datasets/egyptian_canonical/

Its declared sources are:

- Unicode Unikemet.txt
- Official JSeshFont.ttf

The old datasets/egyptian/ pipeline is legacy.

---

## 1. build_gardiner_reference_corpus.py

Historical role:

- downloaded Egyptian-hieroglyph SVG files from Wikimedia Commons;
- iterated over the first 200 Unicode code points beginning at U+13000;
- rasterized SVG to PNG;
- thresholded, cropped, resized and centered glyph images;
- stored Unicode/source metadata.

Important correction:

This was not a verified Gardiner corpus construction.
It was primarily a Unicode glyph-image acquisition experiment.

Do not preserve as canonical ingestion.

---

## 2. build_gardiner_registry.py

Historical role:

- scanned legacy Egyptian image filenames;
- attempted to infer Gardiner codes from filename syntax;
- classified filenames as recognized/unrecognized.

Limitation:

Filename pattern matching is not authoritative sign identity.

Do not migrate implementation.

---

## 3. build_canonical_gardiner_registry.py

Historical role:

- consumed franken_gardiner_mapping.csv;
- created one record per Gardiner code;
- attached Franken/GlyphReader image path;
- treated image as an attribute rather than identity.

Useful historical principle:

Image representation and sign identity are separate concepts.

Limitation:

The Franken/GlyphReader mapping belongs to the legacy experimental
pipeline and is not canonical evidence by itself.

Do not migrate implementation.

---

## 4. build_unikemet_registry.py

Experimental field interpretation:

- kEH_HG    -> gardiner_code
- kEH_UniK  -> unikemet_code
- kEH_JSesh -> jsesh_code
- kEH_Cat   -> category
- kEH_Desc  -> description
- kEH_Func  -> function
- kEH_Core  -> core

This was an experimental mapping, not canonical truth.

---

## 5. build_unikemet_registry_v31.py

Change from previous version:

- kEH_HG remained primary Gardiner mapping;
- kEH_JSesh became fallback Gardiner mapping when kEH_HG was absent;
- provenance field gardiner_source recorded HG versus JSesh.

This fallback policy was experimental.

---

## 6. build_unikemet_registry_v32.py

Changes:

- retained HG-first / JSesh-fallback policy;
- normalized codes beginning with AA to Aa;
- removed records lacking a Gardiner mapping.

The normalization and filtering rules were experimental
and must not be silently inherited.

---

## 7. build_unikemet_registry_v4.py

Change of identity model:

- first collected UniKemet properties by Unicode code point;
- then constructed a registry keyed by unique Gardiner code;
- preferred kEH_HG over kEH_JSesh where alternatives existed.

This demonstrates an experimental transition from Unicode-codepoint
identity toward Gardiner-code identity.

It is historical evidence of design exploration, not a canonical rule.

---

## 8. build_unikemet_registry_v5.py

Important conflicting interpretation:

- kEH_UniK was assigned to gardiner_code;
- kEH_HG was assigned to hieroglyphica_code;
- kEH_JSesh remained jsesh_code.

This differs materially from earlier builders.

Therefore no legacy version may be selected as canonical merely because
it is numerically later.

This conflict is one of the principal reasons the builders are being
removed rather than migrated unchanged.

---

## 9. build_unikemet_unicode_registry.py

Historical role:

- preserved Egyptian UniKemet records by Unicode code point;
- retained raw UniKemet tags;
- included the Egyptian Hieroglyphs and Extended-A ranges;
- exported machine-readable CSV/JSON.

Useful concept:

An immutable source-level registry keyed by source identifier can be
useful for provenance.

Scientific boundary:

Such a source registry is external metadata and must remain distinct
from epigraphic identity and measured sign features.

---

# Final decision

The nine legacy builders have served their historical/provenance role.

Their useful lessons are now preserved here:

1. source identity must be explicit;
2. Unicode identity, Gardiner identity, JSesh naming and image identity
   must not be silently conflated;
3. conflicting external mappings must retain provenance;
4. labels and semantic descriptions remain external metadata;
5. image representation does not define epigraphic identity;
6. experimental normalization/fallback rules are not canonical facts;
7. no legacy builder is accepted unchanged as canonical Core.

The implementations may now be removed.

Future Egyptian ingestion/registry work must use the canonical dataset
and the current AncientScriptLab identity/measurement architecture.
