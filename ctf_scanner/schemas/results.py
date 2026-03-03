from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class NormalizedTarget(BaseModel):
    raw: str
    target_type: Literal["ip", "domain", "url", "cidr"]
    host: str
    port: int | None = None
    scheme: str | None = None


class PortEntry(BaseModel):
    port: int
    protocol: str
    state: str
    service: str | None = None
    product: str | None = None
    version: str | None = None


class PortScanResult(BaseModel):
    profile: Literal["quick", "balanced", "deep"]
    command: str
    xml_path: str
    open_ports: list[PortEntry] = Field(default_factory=list)


class DirectoryEntry(BaseModel):
    path: str
    status: int
    size: int | None = None
    words: int | None = None
    lines: int | None = None


class DirectoryScanResult(BaseModel):
    command: str
    output_path: str
    entries: list[DirectoryEntry] = Field(default_factory=list)


class ScanResults(BaseModel):
    project_name: str
    timestamp: datetime
    target: NormalizedTarget
    port_scan: PortScanResult
    directory_scan: DirectoryScanResult | None = None
