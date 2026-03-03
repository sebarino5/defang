from __future__ import annotations

import logging
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

from ctf_scanner.schemas.results import PortEntry, PortScanResult

LOGGER = logging.getLogger(__name__)


PROFILE_ARGS = {
    "quick": ["-T2", "--top-ports", "100"],
    "balanced": ["-T2", "-sV", "--top-ports", "1000"],
    "deep": ["-T3", "-sV", "-p-"],
}


PORT_MODE_ARGS = {
    "top100": ["--top-ports", "100"],
    "top1000": ["--top-ports", "1000"],
    "full": ["-p-"],
}


def ensure_nmap() -> None:
    if shutil.which("nmap") is None:
        raise RuntimeError("nmap ist nicht installiert oder nicht im PATH verfügbar.")


def parse_nmap_xml(xml_path: Path) -> list[PortEntry]:
    entries: list[PortEntry] = []
    tree = ET.parse(xml_path)
    root = tree.getroot()
    for host in root.findall("host"):
        ports = host.find("ports")
        if ports is None:
            continue
        for port in ports.findall("port"):
            state = port.find("state")
            service = port.find("service")
            state_name = state.get("state", "unknown") if state is not None else "unknown"
            if state_name != "open":
                continue
            entries.append(
                PortEntry(
                    port=int(port.get("portid", "0")),
                    protocol=port.get("protocol", "tcp"),
                    state=state_name,
                    service=service.get("name") if service is not None else None,
                    product=service.get("product") if service is not None else None,
                    version=service.get("version") if service is not None else None,
                )
            )
    return sorted(entries, key=lambda x: x.port)


def run_port_scan(
    target_host: str,
    profile: str,
    ports_mode: str,
    custom_ports: str | None,
    output_dir: Path,
) -> PortScanResult:
    ensure_nmap()
    output_dir.mkdir(parents=True, exist_ok=True)
    xml_path = output_dir / "nmap.xml"

    cmd = ["nmap", "-oX", str(xml_path)]
    if ports_mode == "custom":
        if not custom_ports:
            raise ValueError("custom_ports muss bei ports_mode=custom gesetzt sein")
        cmd.extend(["-p", custom_ports])
        if profile in {"balanced", "deep"}:
            cmd.append("-sV")
    else:
        if profile == "deep" and ports_mode != "full":
            cmd.extend(PROFILE_ARGS[profile])
        else:
            cmd.extend(PORT_MODE_ARGS.get(ports_mode, PROFILE_ARGS[profile]))
            if profile in {"balanced", "deep"} and "-sV" not in cmd:
                cmd.append("-sV")
            cmd.append("-T2")
    cmd.append(target_host)

    LOGGER.info("Starte Portscan: %s", " ".join(cmd))
    subprocess.run(cmd, check=True)

    ports = parse_nmap_xml(xml_path)
    return PortScanResult(profile=profile, command=" ".join(cmd), xml_path=str(xml_path), open_ports=ports)
