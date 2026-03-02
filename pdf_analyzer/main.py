import argparse
import sys
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import jsbeautifier

from extractor import extract_js
from analyzer import HeapSprayAnalyzer

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Malicious PDF Analyzer - Extract JS and detect Heap Sprays")
    parser.add_argument("--file", required=True, help="Path to the suspicious PDF file")
    parser.add_argument("--dump-js", action="store_true", help="Save extracted JavaScript to a file")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        console.print(f"[bold red]Error:[/bold red] File '{args.file}' not found.")
        sys.exit(1)

    console.print(f"[bold blue]Scanning:[/bold blue] {args.file}...")

    # Step 1: Extract JS
    js_payload = extract_js(args.file)
    
    if not js_payload:
        console.print("[bold green]Result:[/bold green] Clean. No JavaScript found in the document.")
        return

    # Step 2: Beautify JS for better analysis/dumping
    beautified_js = jsbeautifier.beautify(js_payload)

    # Step 3: Analyze
    analyzer = HeapSprayAnalyzer()
    results = analyzer.analyze(beautified_js)

    # Step 4: Display Results
    console.print(Panel(f"Found [bold yellow]{len(beautified_js)}[/bold yellow] bytes of JavaScript payloads."))

    table = Table(title="Heap Spray Analysis Findings")
    table.add_column("Category", style="cyan")
    table.add_column("Matches Found", style="magenta")

    for finding in results["findings"]:
        table.add_row(finding["category"], str(finding["count"]))

    console.print(table)

    if results["confidence"] == "CLEAN":
        console.print("\n[bold green]Verdict: CLEAN — No Heap Spray Indicators Found.[/bold green]")
    else:
        color = "red" if results["confidence"] == "HIGH" else "yellow" if results["confidence"] == "MEDIUM" else "cyan"
        console.print(f"\n[bold {color}]Verdict: {results['confidence']} CONFIDENCE — Heap Spray Detected.[/bold {color}]")

    # Optional: Dump JS
    if args.dump_js:
        dump_path = f"{os.path.basename(args.file)}_extracted.js"
        with open(dump_path, "w", encoding="utf-8") as f:
            f.write(beautified_js)
        console.print(f"\n[bold white]JS Dumped to:[/bold white] {dump_path}")

if __name__ == "__main__":
    main()
