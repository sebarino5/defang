# Defanger

Eine einfache Webanwendung zum Hervorheben von Satzzeichen in Texten.

## Beschreibung

Defanger ist eine benutzerfreundliche Webanwendung mit dunklem Design, die es ermöglicht, Satzzeichen in Texten visuell hervorzuheben, indem sie in eckige Klammern gesetzt werden. Dies kann besonders nützlich sein für:
- Textanalyse
- Grammatikunterricht
- Textformatierung
- Dokumentenprüfung

## Funktionen

- Einfache Texteingabe
- Automatische Erkennung und Hervorhebung von Satzzeichen:
  - Punkt (.) → [.]
  - Komma (,) → [,]
  - Fragezeichen (?) → [?]
  - Ausrufezeichen (!) → [!]
  - Semikolon (;) → [;]
  - Doppelpunkt (:) → [:]
- Kopieren des verarbeiteten Textes in die Zwischenablage
- Responsive Design für alle Geräte
- Tastaturkürzel: Strg + Enter zum Verarbeiten
- Dunkles Design für bessere Lesbarkeit

## Technologien

- HTML5
- Tailwind CSS für das Styling
- Vanilla JavaScript für die Logik
- Inter Schriftart für optimale Lesbarkeit

## Verwendung

1. Öffnen Sie die `index.html` in einem modernen Webbrowser
2. Geben Sie Ihren Text in das Eingabefeld ein
3. Klicken Sie auf "Text verarbeiten" oder drücken Sie Strg + Enter
4. Der verarbeitete Text erscheint im Ausgabefeld
5. Klicken Sie auf "In Zwischenablage kopieren", um den Text zu kopieren

## Beispiel

Eingabe:
```
Hallo Welt. Ich teste diese Anwendung! Funktioniert es, wie ich es erwarte? Ich glaube schon; ja.
```

Ausgabe:
```
Hallo Welt[.] Ich teste diese Anwendung[!] Funktioniert es[,] wie ich es erwarte[?] Ich glaube schon[;] ja[.]
```

## Design

- Dunkles Farbschema für bessere Lesbarkeit
- Moderne, minimalistische Benutzeroberfläche
- Responsive Design für alle Bildschirmgrößen
- Optimierte Kontraste für bessere Zugänglichkeit

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. 