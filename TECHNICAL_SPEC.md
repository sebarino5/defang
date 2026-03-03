# Technische Spezifikation – Automatisierter CTF Scanner

## Zielsetzung
Ein lokales Recon- und Enumeration-Tool für **autorisierte CTF-Targets oder eigene Systeme**. Fokus liegt auf sicherer und konservativer Informationsgewinnung ohne Exploit-/Bruteforce-Funktionen.

## Kernanforderungen
- Eingaben: IP, Domain, URL, CIDR
- Scan-Profile: Quick, Balanced, Deep
- Optionale Directory Enumeration
- Strukturierte Artefakte (raw + parsed)
- Exporte: JSON + Markdown
- CLI (Typer) und lokales HUD (Streamlit)

## Architektur
- **Core**: Konfiguration, Logging, Orchestrierung
- **Module 1**: Target-Normalisierung und Validierung
- **Module 2**: Portscan (nmap Wrapper + XML Parsing)
- **Module 3**: Directory Scan (ffuf Wrapper + JSON Parsing)
- **Module 4**: Reporting (JSON Aggregation + Markdown Bericht)

## Projektstruktur
- `ctf_scanner/cli.py` – Typer CLI Entry
- `ctf_scanner/modules/*` – funktionale Scan- und Report-Module
- `ctf_scanner/schemas/results.py` – Pydantic Datenmodelle
- `ctf_scanner/hud/app.py` – Streamlit HUD
- `projects/<projektname>/...` – erzeugte Ergebnisse

## Sicherheits- und Compliance-Guardrails
- Keine Exploit- oder Login-Angriffe
- Keine Bruteforce-Funktionalität
- Konservative Defaults (`-T2`, moderate Rate Limits)
- Fehlerbehandlung bei fehlenden externen Tools (nmap/ffuf)

## Ausgabeformat
- `raw/nmap/nmap.xml`
- `raw/dirscan/ffuf.json`
- `results/normalized.json`
- `results/scan_results.json`
- `report/report.md`
