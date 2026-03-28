from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ScannerConfig(BaseModel):
    project_name: str
    output_dir: Path = Field(default=Path("projects"))
    target: str
    profile: Literal["quick", "balanced", "deep"] = "balanced"
    ports_mode: Literal["top100", "top1000", "full", "custom"] = "top1000"
    custom_ports: str | None = None
    run_directory_scan: bool = False
    wordlist: str = "/usr/share/seclists/Discovery/Web-Content/common.txt"
    extensions: str = "php,txt,html"
    recursion_depth: int = 1

    @field_validator("project_name")
    @classmethod
    def project_name_safe(cls, value: str) -> str:
        trimmed = value.strip().replace(" ", "_")
        if not trimmed:
            raise ValueError("project_name darf nicht leer sein")
        return trimmed

    def project_root(self) -> Path:
        return self.output_dir / self.project_name
