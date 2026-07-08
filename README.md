# Abschlussprojekt

# EKG- und Schlafanalyse

## Projektbeschreibung

Diese Anwendung wurde im Rahmen eines Abschlussprojekts entwickelt und dient zur Analyse von EKG- und Smartwatch-Daten.

Benutzer können sich registrieren und anmelden. Jeder Benutzer verwaltet ausschließlich seine eigenen Messdaten. Die Anwendung bietet verschiedene Analyse- und Visualisierungsmöglichkeiten für EKG- sowie Schlafdaten.

## Funktionen

### Benutzerverwaltung

- Registrierung neuer Benutzer
- Login mit verschlüsselten Passwörtern 
- Persönliches Benutzerprofil
- Bearbeiten der eigenen Daten
- Löschen des eigenen Kontos

### EKG-Analyse

- Auswahl verschiedener EKG-Messungen
- Darstellung des EKG-Signals
- Einstellbarer Zeitbereich
- Einstellbarer Peak-Schwellwert
- Einstellbarer Mindestabstand zwischen Peaks
- Automatische Peak-Erkennung
- Berechnung der durchschnittlichen Herzfrequenz
- Darstellung der Herzratenvariabilität (HRV)
- Darstellung der Herzrate als gleitender Durchschnitt

### Schlafanalyse

Auswertung von Smartwatch-Daten mit:

- Herzfrequenz
- Herzratenvariabilität (HRV)
- Sauerstoffsättigung (SpO₂)
- Atemfrequenz
- Bewegung

Zusätzlich werden berechnet:

- Schlafphasen
- Schlafdauer
- Schlafscore
- Hinweise auf mögliche Schlafapnoe

### Datenverwaltung

- Hochladen neuer EKG-Dateien
- Hochladen neuer Profilbilder
- Speicherung aller Benutzerdaten in einer JSON-Datenbank

---

## Projektstruktur

```
Abschlussprojekt/
│
├── app.py
├── app_pages/
├── src/
├── data/
│   ├── ekg_data/
│   ├── smartwatch_data/
│   ├── pictures/
│   └── person_db.json
├── requirements.txt
├── pyproject.toml
├── pdm.lock
└── README.md
```

---

## Benötigte Bibliotheken

- streamlit
- pandas
- matplotlib
- plotly
- bcrypt

Diese Bibliotheken werden automatisch über die Datei `pyproject.toml` installiert.

---

## Projekt starten

### Repository klonen

```bash
git clone https://github.com/jarnsteiner/Abschlussprojekt.git
```

### In das Projekt wechseln

```bash
cd Abschlussprojekt
```

### Abhängigkeiten installieren

Mit PDM:

```bash
pdm install
```

oder alternativ mit pip:

```bash
pip install -r requirements.txt
```

### Anwendung starten

```bash
streamlit run app.py
```

Danach öffnet sich die Anwendung automatisch im Browser.

---

## Hinweise

Beim ersten Start können neue Benutzer registriert werden.

Bestehende Benutzer können sich mit ihrem Benutzernamen und Passwort anmelden.

Für diese drei Benutzer sind jeweils als Benutzernamen deren Vorname und als Passwort 1234 zu verwenden.

Alle hochgeladenen Bilder und EKG-Dateien werden automatisch im Projekt gespeichert.

---

## Entwickler

Arnsteiner Jan

Bichlbauer Laurence

