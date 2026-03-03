from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

import typer
from rich.console import Console

from ctf_scanner.core.config import ScannerConfig
from ctf_scanner.core.logging import setup_logging
from ctf_scanner.modules.dir_scan import run_directory_scan
from ctf_scanner.modules.port_scan import run_port_scan
from ctf_scanner.modules.reporting import (
    write_markdown_report,
    write_normalized_target,
    write_results_json,
)
from ctf_scanner.modules.target_normalization import normalize_target
from ctf_scanner.schemas.results import ScanResults

app = typer.Typer(help="Autorisierter CTF Recon Scanner (nur Enumeration)")
console = Console()
LOGGER = logging.getLogger(__name__)


@app.command()
def run(
    target: str = typer.Option(..., help="Target als IP/Domain/URL/CIDR"),
    project_name: str = typer.Option(..., help="Projektname"),
    profile: str = typer.Option("balanced", help="quick|balanced|deep"),
    ports_mode: str = typer.Option("top1000", help="top100|top1000|full|custom"),
    custom_ports: str | None = typer.Option(None, help="z.B. 80,443,8080"),
    directory_scan: bool = typer.Option(False, help="Directory Scan aktivieren"),
    wordlist: str = typer.Option(
        "/usr/share/seclists/Discovery/Web-Content/common.txt", help="Wordlist für ffuf"
    ),
    extensions: str = typer.Option("php,txt,html", help="Dateiendungen"),
    recursion_depth: int = typer.Option(1, help="Recursion Depth"),
    output_dir: Path = typer.Option(Path("projects"), help="Output Ordner"),
) -> None:
    """Startet einen autorisierten Recon Scan."""
    setup_logging()

    config = ScannerConfig(
        project_name=project_name,
        output_dir=output_dir,
        target=target,
        profile=profile,
        ports_mode=ports_mode,
        custom_ports=custom_ports,
        run_directory_scan=directory_scan,
        wordlist=wordlist,
        extensions=extensions,
        recursion_depth=recursion_depth,
    )

    project_root = config.project_root()
    raw_nmap = project_root / "raw" / "nmap"
    raw_dir = project_root / "raw" / "dirscan"
    results_dir = project_root / "results"
    report_dir = project_root / "report"

    normalized_target = normalize_target(config.target)
    write_normalized_target(normalized_target.model_dump(), results_dir / "normalized.json")

    port_result = run_port_scan(
        target_host=normalized_target.host,
        profile=config.profile,
        ports_mode=config.ports_mode,
        custom_ports=config.custom_ports,
        output_dir=raw_nmap,
    )

    dir_result = None
    if config.run_directory_scan:
        base_url = (
            f"{normalized_target.scheme or 'http'}://{normalized_target.host}"
            if normalized_target.target_type in {"domain", "ip", "cidr"}
            else normalized_target.raw
        )
        try:
            dir_result = run_directory_scan(
                target_url=base_url,
                wordlist=config.wordlist,
                extensions=config.extensions,
                recursion_depth=config.recursion_depth,
                output_dir=raw_dir,
            )
        except RuntimeError as err:
            LOGGER.warning("Directory Scan übersprungen: %s", err)

    aggregated = ScanResults(
        project_name=config.project_name,
        timestamp=datetime.utcnow(),
        target=normalized_target,
        port_scan=port_result,
        directory_scan=dir_result,
    )

    write_results_json(aggregated, results_dir / "scan_results.json")
    write_markdown_report(aggregated, report_dir / "report.md")
    console.print(f"[green]Scan abgeschlossen. Ergebnisse in {project_root}[/green]")


if __name__ == "__main__":
    app()
