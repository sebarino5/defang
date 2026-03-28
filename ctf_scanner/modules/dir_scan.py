from __future__ import annotations

import json
import logging
import shutil
import subprocess
from pathlib import Path

from ctf_scanner.schemas.results import DirectoryEntry, DirectoryScanResult

LOGGER = logging.getLogger(__name__)


def ensure_ffuf() -> None:
    if shutil.which("ffuf") is None:
        raise RuntimeError("ffuf ist nicht installiert oder nicht im PATH verfügbar.")


def run_directory_scan(
    target_url: str,
    wordlist: str,
    extensions: str,
    recursion_depth: int,
    output_dir: Path,
) -> DirectoryScanResult:
    ensure_ffuf()
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "ffuf.json"

    cmd = [
        "ffuf",
        "-u",
        f"{target_url.rstrip('/')}/FUZZ",
        "-w",
        wordlist,
        "-recursion",
        "-recursion-depth",
        str(recursion_depth),
        "-mc",
        "200,204,301,302,307,401,403",
        "-t",
        "20",
        "-rate",
        "50",
        "-of",
        "json",
        "-o",
        str(out_path),
    ]

    normalized_extensions = ",".join(f".{ext.strip().lstrip('.')}" for ext in extensions.split(",") if ext.strip())
    if normalized_extensions:
        cmd.extend(["-e", normalized_extensions])

    LOGGER.info("Starte Directory Scan: %s", " ".join(cmd))
    subprocess.run(cmd, check=True)

    data = json.loads(out_path.read_text(encoding="utf-8"))
    entries = [
        DirectoryEntry(
            path=item.get("url", ""),
            status=item.get("status", 0),
            size=item.get("length"),
            words=item.get("words"),
            lines=item.get("lines"),
        )
        for item in data.get("results", [])
    ]

    return DirectoryScanResult(command=" ".join(cmd), output_path=str(out_path), entries=entries)
