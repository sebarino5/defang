from __future__ import annotations

import json
from pathlib import Path

from ctf_scanner.schemas.results import ScanResults


def write_results_json(scan_results: ScanResults, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(scan_results.model_dump_json(indent=2), encoding="utf-8")


def build_markdown_report(scan_results: ScanResults) -> str:
    lines: list[str] = [
        f"# Recon Report: {scan_results.project_name}",
        "",
        f"**Timestamp:** {scan_results.timestamp.isoformat()}",
        f"**Target:** `{scan_results.target.raw}` ({scan_results.target.target_type})",
        f"**Host:** `{scan_results.target.host}`",
        "",
        "## Offene Ports",
        "",
        "| Port | Proto | Service | Product | Version |",
        "|---:|---|---|---|---|",
    ]

    for entry in scan_results.port_scan.open_ports:
        lines.append(
            f"| {entry.port} | {entry.protocol} | {entry.service or '-'} | {entry.product or '-'} | {entry.version or '-'} |"
        )

    if not scan_results.port_scan.open_ports:
        lines.append("| - | - | - | - | - |")

    lines.extend(["", "## Directories", "", "| Path | Status | Size |", "|---|---:|---:|"])
    if scan_results.directory_scan and scan_results.directory_scan.entries:
        for entry in scan_results.directory_scan.entries:
            lines.append(f"| `{entry.path}` | {entry.status} | {entry.size or '-'} |")
    else:
        lines.append("| - | - | - |")

    lines.extend(
        [
            "",
            "## Verwendete Commands",
            "",
            f"- `{scan_results.port_scan.command}`",
        ]
    )

    if scan_results.directory_scan:
        lines.append(f"- `{scan_results.directory_scan.command}`")

    return "\n".join(lines) + "\n"


def write_markdown_report(scan_results: ScanResults, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(build_markdown_report(scan_results), encoding="utf-8")


def write_normalized_target(target_data: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(target_data, indent=2), encoding="utf-8")
