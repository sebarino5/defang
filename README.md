# Automatisierter CTF Scanner (nur Enumeration)

Ein Portfolio-Projekt für autorisierte Recon-Scans auf CTF-Zielen oder eigenen Systemen.

> ⚠️ **Nur auf autorisierten Targets verwenden.**
> Keine Exploits, kein Brute Force, keine Passwort-Angriffe.

## Features
- Target Normalization (IP, Domain, URL, CIDR)
- Portscan via `nmap` Wrapper (Quick / Balanced / Deep)
- Optionaler Directory Scan via `ffuf`
- Strukturierte Projekt-Ausgabe (raw + parsed)
- Export als JSON und Markdown Report
- CLI mit Typer
- Lokales Browser-HUD mit Streamlit

## Projektstruktur

```text
ctf_scanner/
  cli.py
  core/
  modules/
  schemas/
  hud/
projects/
  <project_name>/
    raw/
      nmap/
      dirscan/
    results/
      normalized.json
      scan_results.json
    report/
      report.md
```

## Installation

### Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

### Windows (PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -U pip
pip install -e .
```

## Externe Tools
- `nmap` (erforderlich für Portscan)
- `ffuf` (optional für Directory Scan)

Wenn ein Tool fehlt, wird ein klarer Fehler bzw. eine Warnung ausgegeben.

## CLI Nutzung

### Quick Scan
```bash
ctf-scanner run \
  --target scanme.nmap.org \
  --project-name demo_quick \
  --profile quick \
  --ports-mode top100
```

### Balanced + Directory Scan
```bash
ctf-scanner run \
  --target http://example.local \
  --project-name demo_balanced \
  --profile balanced \
  --ports-mode top1000 \
  --directory-scan \
  --wordlist /usr/share/seclists/Discovery/Web-Content/common.txt \
  --extensions php,txt,html \
  --recursion-depth 1
```

## Streamlit HUD
```bash
streamlit run ctf_scanner/hud/app.py
```

HUD unterstützt:
- Target-Eingabe (IP/Domain/URL/CIDR)
- Scan-Profil
- Port-Modus inkl. Custom Ports
- Directory-Scan Toggle + Parameter
- Live Logs und Ergebnis-Tabellen
- JSON/Markdown Download

## Beispiel Report (Ausschnitt)

```md
# Recon Report: demo_quick

**Target:** `scanme.nmap.org` (domain)

## Offene Ports
| Port | Proto | Service | Product | Version |
|---:|---|---|---|---|
| 22 | tcp | ssh | OpenSSH | 8.9p1 |

## Verwendete Commands
- `nmap -oX projects/demo_quick/raw/nmap/nmap.xml --top-ports 100 -T2 scanme.nmap.org`
```

## Entwicklung
Technische Spezifikation: `TECHNICAL_SPEC.md`
