from pathlib import Path
import subprocess
import sys
import re

TOOLS_DIR = Path("tools")

CLI_REQUIRES_ARGS = {
    "analyze_corpus_frequency.py",
    "analyze_corpus_structure.py",
    "build_corpus_frequency_profile.py",
}

FAILURE_RE = re.compile(r"(^|[^A-Z])(FAIL|FAILED|ERROR)([^A-Z]|$)", re.I)


def run_tool(path: Path):
    proc = subprocess.run(
        [sys.executable, str(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return proc.returncode, proc.stdout


def main():
    counts = {
        "PASS": 0,
        "CLI_REQUIRES_ARGS": 0,
        "FAIL": 0,
        "PRINTED_FAILURE": 0,
    }

    details = []

    for path in sorted(TOOLS_DIR.glob("*.py")):
        if path.name == Path(__file__).name:
            continue

        rc, output = run_tool(path)

        if path.name in CLI_REQUIRES_ARGS:
            if rc != 0 and "Usage:" in output:
                status = "CLI_REQUIRES_ARGS"
            else:
                status = "FAIL"

        elif rc != 0:
            status = "FAIL"

        elif FAILURE_RE.search(output):
            status = "PRINTED_FAILURE"

        else:
            status = "PASS"

        counts[status] += 1
        details.append((path, status, rc, output))

    print("AncientScriptLab — Tools Regression")
    print("===================================")

    for path, status, rc, _ in details:
        print(f"{path}: {status} rc={rc}")

    print()
    print("=== SUMMARY ===")
    for key in ("PASS", "CLI_REQUIRES_ARGS", "FAIL", "PRINTED_FAILURE"):
        print(f"{key}={counts[key]}")

    genuine_failures = counts["FAIL"] + counts["PRINTED_FAILURE"]

    if genuine_failures:
        print()
        print("=== FAILURE DETAILS ===")

        for path, status, rc, output in details:
            if status in {"FAIL", "PRINTED_FAILURE"}:
                print()
                print(f"FILE: {path}")
                print(f"STATUS: {status}")
                print(f"RC: {rc}")
                print(output.rstrip())

        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
