from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime


def write_json(report, path):
    path = Path(path)

    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    content = json.dumps(report, indent=2)
    path.write_text(content)


from datetime import datetime


def render_markdown(report: dict) -> str:
    lines = []

    lines.append("# CSV Profiling Report")
    lines.append("")
    lines.append(
        f"Generated: {datetime.now().isoformat(timespec='seconds')}"
    )
    lines.append("")

    lines.append("## Summary")
    lines.append(f"- Rows: **{report['n_rows']}**")
    lines.append(f"- Columns: **{report['n_cols']}**")
    lines.append("")

    lines.append("## Columns")
    lines.append("")
    lines.append("| name | type | missing | missing_pct | unique |")
    lines.append("|------|------|---------|-------------|--------|")

    for c in report["columns"]:
        lines.append(
            f"| {c['name']} | {c['type']} | {c['missing']} | {c['missing_pct']:.1f}% | {c['unique']} |"
        )

    lines.append("")
    lines.append("## Notes")
    lines.append(
        "- Missing values are: '', 'na', 'n/a', 'null', 'none', 'nan' (case-insensitive)"
    )

    return "\n".join(lines)
