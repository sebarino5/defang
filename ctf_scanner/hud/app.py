from __future__ import annotations

import json
import subprocess
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="CTF Recon HUD", layout="wide")
st.title("Automatisierter CTF Scanner (Nur Enumeration)")
st.caption("Nur für autorisierte CTF Ziele oder eigene Systeme")

with st.form("scan_form"):
    target = st.text_input("Target (IP / Domain / URL / CIDR)")
    project_name = st.text_input("Projektname", value="ctf_project")
    output_dir = st.text_input("Output Ordner", value="projects")

    col1, col2, col3 = st.columns(3)
    with col1:
        profile = st.selectbox("Scan Profil", ["quick", "balanced", "deep"], index=1)
    with col2:
        ports_mode = st.selectbox("Ports", ["top100", "top1000", "full", "custom"], index=1)
    with col3:
        custom_ports = st.text_input("Custom Ports", value="")

    directory_scan = st.toggle("Directory Scan", value=False)
    wordlist = st.text_input("Wordlist", value="/usr/share/seclists/Discovery/Web-Content/common.txt")
    extensions = st.text_input("Extensions", value="php,txt,html")
    recursion_depth = st.number_input("Recursion Depth", min_value=0, max_value=5, value=1)

    submitted = st.form_submit_button("Start Scan")

if submitted:
    if not target.strip():
        st.error("Bitte Target eingeben.")
    else:
        cmd = [
            "python",
            "-m",
            "ctf_scanner.cli",
            "run",
            "--target",
            target,
            "--project-name",
            project_name,
            "--profile",
            profile,
            "--ports-mode",
            ports_mode,
            "--output-dir",
            output_dir,
            "--extensions",
            extensions,
            "--recursion-depth",
            str(recursion_depth),
        ]
        if custom_ports.strip():
            cmd.extend(["--custom-ports", custom_ports])
        if directory_scan:
            cmd.extend(["--directory-scan", "--wordlist", wordlist])

        st.code(" ".join(cmd), language="bash")
        proc = subprocess.run(cmd, capture_output=True, text=True)

        st.subheader("Live Status / Logs")
        st.code((proc.stdout or "") + "\n" + (proc.stderr or ""))

        project_root = Path(output_dir) / project_name
        result_json = project_root / "results" / "scan_results.json"
        report_md = project_root / "report" / "report.md"

        if proc.returncode == 0 and result_json.exists():
            data = json.loads(result_json.read_text(encoding="utf-8"))
            st.success("Scan abgeschlossen")

            ports = data.get("port_scan", {}).get("open_ports", [])
            st.subheader("Offene Ports & Services")
            st.dataframe(ports, use_container_width=True)

            directories = (data.get("directory_scan") or {}).get("entries", [])
            st.subheader("Gefundene Directories")
            st.dataframe(directories, use_container_width=True)

            st.download_button("Export JSON", result_json.read_text(encoding="utf-8"), "scan_results.json")
            if report_md.exists():
                st.download_button("Export Markdown", report_md.read_text(encoding="utf-8"), "report.md")
        else:
            st.error("Scan fehlgeschlagen. Details siehe Logs.")
