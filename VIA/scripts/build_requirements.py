"""Write one JSONL index per system and a summary CSV.

The loader reads ``requirements.txt`` on demand; this script materializes the
same reading for auditability. It does not modify the inputs.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))

from via.io.loader import find_input_dir, load_requirements, sha256_file

INPUTS = BASE.parent / "Experimento_Multiagente" / "Dates" / "davinci_inputs"
OUT = BASE / "data" / "requirements"

SYSTEMS = [
    "7ep",
    "AcmeAir",
    "Cargo-Tracker",
    "DayTrader7",
    "JPetStore",
    "Jokul",
    "PetClinic",
    "TNTConcept",
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for system in SYSTEMS:
        folder = find_input_dir(INPUTS, system)
        requirements, warnings = load_requirements(folder)
        target = OUT / f"{system.lower().replace('-', '_')}.jsonl"
        with target.open("w", encoding="utf-8") as handle:
            for requirement in requirements:
                handle.write(json.dumps(requirement, ensure_ascii=False, sort_keys=True) + "\n")
        source = folder / "requirements.txt"
        rows.append(
            {
                "system": system,
                "requirements": str(len(requirements)),
                "source": str(source),
                "source_sha256": sha256_file(source),
                "warnings": "; ".join(warnings),
            }
        )
    summary = OUT / "_summary.csv"
    with summary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"systems: {len(rows)}")
    print(f"summary: {summary}")
    for row in rows:
        print(f"{row['system']}: {row['requirements']}")


if __name__ == "__main__":
    main()
