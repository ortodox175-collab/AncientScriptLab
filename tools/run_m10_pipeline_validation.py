from pathlib import Path
import json

OUT_DIR = Path("reports/validation")
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / "m10_pipeline_validation.json"
MD_OUT = OUT_DIR / "M10_PIPELINE_VALIDATION_REPORT.md"

checks = []

def check_json(path, description):
    p = Path(path)
    result = {
        "module": description,
        "path": str(p),
        "exists": p.exists(),
        "valid_json": False,
        "record_count": None,
    }

    if p.exists():
        try:
            data = json.loads(p.read_text())

            if isinstance(data, dict):
                result["valid_json"] = True

                if "graphs" in data:
                    result["record_count"] = len(data["graphs"])
                elif "clusters" in data:
                    result["record_count"] = len(data["clusters"])
                elif "hierarchy" in data:
                    result["record_count"] = len(data["hierarchy"])

        except Exception:
            result["valid_json"] = False

    checks.append(result)

check_json(
    "datasets/egyptian/signatures/structural_signatures.json",
    "M10.1A Structural Signatures"
)

check_json(
    "datasets/egyptian/signatures/structural_signatures_v1_1.json",
    "M10.1C Spatial Signatures"
)

check_json(
    "datasets/egyptian/component_graphs/component_relation_graphs.json",
    "M10.1D Component Graphs"
)

check_json(
    "datasets/egyptian/primitive_graphs/primitive_graphs.json",
    "M10.1E Primitive Graphs"
)

check_json(
    "reports/statistics/egyptian/graph_signature_clusters.json",
    "M10.1G Graph Clusters"
)

check_json(
    "reports/statistics/egyptian/archetype_number_estimation.json",
    "M10.1H Archetype Number Estimation"
)

check_json(
    "reports/statistics/egyptian/archetype_stability_validation_v2.json",
    "M10.1I Archetype Stability Validation"
)

check_json(
    "reports/statistics/egyptian/hierarchical_archetypes.json",
    "M10.1J Hierarchical Archetypes"
)

pipeline_ok = True
counts = []

for c in checks:
    if not c["exists"] or not c["valid_json"]:
        pipeline_ok = False
    if c["record_count"] is not None:
        counts.append(c["record_count"])

count_consistency = len(set(counts)) <= 3 if counts else False

hierarchy_ok = False

hierarchy_path = Path(
    "reports/statistics/egyptian/hierarchical_archetypes.json"
)

if hierarchy_path.exists():
    try:
        h = json.loads(hierarchy_path.read_text())
        hierarchy_ok = (
            h.get("macro_count") == 3 and
            h.get("meso_count") == 10 and
            h.get("micro_count") == 27
        )
    except Exception:
        hierarchy_ok = False

report = {
    "module": "M10.2 Integrated Structural Pipeline Validation",
    "pipeline_status": "PASS" if pipeline_ok else "FAIL",
    "count_consistency": count_consistency,
    "hierarchy_consistency": hierarchy_ok,
    "modules": checks,
}

JSON_OUT.write_text(json.dumps(report, indent=2))

with open(MD_OUT, "w") as f:
    f.write("# M10.2 integrated structural pipeline validation\\n\\n")
    f.write(f"Pipeline status: {report['pipeline_status']}\\n\\n")
    f.write(f"Count consistency: {count_consistency}\\n")
    f.write(f"Hierarchy consistency: {hierarchy_ok}\\n\\n")

    for c in checks:
        f.write(f"## {c['module']}\\n")
        f.write(f"- Exists: {c['exists']}\\n")
        f.write(f"- Valid JSON: {c['valid_json']}\\n")
        f.write(f"- Record count: {c['record_count']}\\n\\n")

print("M10.2 Integrated Structural Pipeline Validation")
print("===============================================")
print(f"Pipeline status      : {report['pipeline_status']}")
print(f"Count consistency    : {count_consistency}")
print(f"Hierarchy consistency: {hierarchy_ok}")
print()
print(f"JSON report          : {JSON_OUT}")
print(f"Markdown report      : {MD_OUT}")
