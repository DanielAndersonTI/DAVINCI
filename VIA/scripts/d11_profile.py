"""Profile the D11 findings written by the quick-check.

D11 flags a service when endpoints / max(1, responsibilities) < 0.5 or when
responsibilities > 3 and endpoints == 1. This script reads the evidence string
of each finding and counts the endpoint and responsibility pairs, so the
"interface is narrow, not absent" claim is traceable to the verdicts.

Run from the VIA directory:

    python scripts/d11_profile.py
"""

from __future__ import annotations

import csv
import json
import re
import statistics
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
LAUDOS = BASE / "reports" / "quick-check-v1" / "verdicts"
OUT = BASE / "reports" / "quick-check-v1" / "d11_profile.csv"

PATTERN = re.compile(r"(\d+) endpoint\(s\) para (\d+) responsabilidade\(s\)")


def main() -> None:
    pairs: Counter[tuple[int, int]] = Counter()
    ratios: list[float] = []
    missing = 0
    for path in sorted(LAUDOS.rglob("*.json")):
        laudo = json.loads(path.read_text(encoding="utf-8"))
        for finding in laudo.get("achados", []):
            if finding.get("codigo") != "D11":
                continue
            match = PATTERN.search(finding.get("evidencia", ""))
            if match is None:
                missing += 1
                continue
            endpoints, responsibilities = int(match.group(1)), int(match.group(2))
            pairs[(endpoints, responsibilities)] += 1
            ratios.append(endpoints / max(1, responsibilities))

    total = sum(pairs.values())
    zero = sum(count for (endpoints, _), count in pairs.items() if endpoints == 0)
    one = sum(count for (endpoints, _), count in pairs.items() if endpoints == 1)
    one_for_many = sum(
        count for (endpoints, responsibilities), count in pairs.items()
        if endpoints == 1 and responsibilities > 3
    )

    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["endpoints", "responsibilities", "findings"])
        for (endpoints, responsibilities), count in sorted(pairs.items()):
            writer.writerow([endpoints, responsibilities, count])

    print(f"findings: {total}")
    print(f"zero endpoints: {zero}")
    print(f"one endpoint: {one}")
    print(f"one endpoint and more than three responsibilities: {one_for_many}")
    print(f"median ratio: {statistics.median(ratios):.3f}")
    print(f"unparsed evidence: {missing}")
    print(f"profile: {OUT}")


if __name__ == "__main__":
    main()
