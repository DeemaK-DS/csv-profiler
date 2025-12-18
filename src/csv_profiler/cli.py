import json
import time
from pathlib import Path
import typer
from io import read_csv_rows
from profile import profile_rows
from render import render_markdown

app = typer.Typer()


@app.command()
def profile(
    input_path: Path = typer.Argument(...),
    out_dir: Path = typer.Option("out"),
    report_name: str = typer.Option("report"),
    preview: bool = typer.Option(False),
):
    start = time.perf_counter()

    rows = read_csv_rows(input_path)
    report = profile_rows(rows)

    duration = (time.perf_counter() - start) * 1000
    report["timing_ms"] = round(duration, 2)

    out_dir.mkdir(parents=True, exist_ok=True)

    json_path = out_dir / f"{report_name}.json"
    json_path.write_text(json.dumps(report, indent=2))

    md_path = out_dir / f"{report_name}.md"
    md_path.write_text(render_markdown(report))

    if preview:
        print(render_markdown(report))


if __name__ == "__main__":
    app()
