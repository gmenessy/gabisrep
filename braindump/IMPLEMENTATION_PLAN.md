# BrainDump – Agentic Memory System v2: Umsetzungsplan

> Basierend auf der Spezifikation v2.1 (08. April 2026)
> Erstellt: 11. Mai 2026

## Ausgangslage

- **Ziel-Repository:** `gabisrep` auf Branch `claude/braindump-implementation-plan-SptrV`
- **Kernkonzept:** Dump → Dream → Brain – rohes Denken wird automatisch in strukturiertes Wissen verwandelt
- **Stack:** Python 3.12+, SQLite + sqlite-vss, pyfuse3, Ollama, Pydantic v2, Typer, Rich/Textual

---

## Phase 0: Fundament – Core + VFS Virtual-Modus (1–2 Tage)

### 0.1 Projekt-Scaffolding

- `braindump/` Verzeichnis mit `pyproject.toml` anlegen (Python 3.12+, alle Dependencies)
- `src/braindump/` Package-Struktur erstellen:
  ```
  src/braindump/{core, vfs, memory, dream, agent, retrieval, cli}/
  src/braindump/models/
  src/braindump/utils/
  ```
- `config.toml` mit Pydantic v2 Settings-Klasse
- `data/` Verzeichnisse: `CORE/`, `USER_WIKI/`, `SKILLS/`, `DUMPS/`, `META/`, `DYNAMIC/`, `TRASH/`

### 0.2 VFS Virtual-Modus (Kernmodul)

- `VFS` Protocol-Klasse implementieren (`ls`, `cat`, `write`, `mkdir`, `link`, `rm`, `search`)
- `VirtualVFS` Klasse als Standard-Implementation (reine Python, kein FUSE)
- `VFSEntry` Datenmodell (Pydantic)
- Dynamische Ordner-Handler: `VirtualFolderProtocol` + `RecentViewHandler`, `ConflictViewHandler`
- Dateien werden auf dem echten Dateisystem unter `data/` gespeichert, VFS abstrahiert den Zugriff

### 0.3 SQLite Metadaten-Layer

- SQLite-Datenbank `braindump.db` initialisieren
- `entries`-Tabelle gemäß Schema:
  ```sql
  CREATE TABLE entries (
      id TEXT PRIMARY KEY,
      vfs_path TEXT NOT NULL,
      layer TEXT NOT NULL,           -- core | wiki | skills | dump | meta
      content_hash TEXT,
      memory_score REAL,
      confidence REAL,
      recency REAL,
      usage_count INTEGER DEFAULT 0,
      last_used TIMESTAMP,
      embedding BLOB,               -- sqlite-vss
      tags TEXT,                     -- JSON array
      version INTEGER DEFAULT 1,
      created_at TIMESTAMP,
      updated_at TIMESTAMP
  );
  ```
- `aiosqlite` + SQLAlchemy 2.0 async Session Setup

**Abhängigkeiten:** Keine – dies ist die Basis für alles Weitere.

**Deliverables:**
- [ ] `pyproject.toml` mit allen Dependencies
- [ ] Lauffähiges VFS im Virtual-Modus (`vfs.ls()`, `vfs.cat()`, `vfs.write()`)
- [ ] SQLite-Datenbank mit `entries`-Tabelle
- [ ] `config.toml` Parser mit Pydantic-Validierung

---

## Phase 1: Memory-Schichten + Embeddings (3–5 Tage)

### 1.1 Pydantic-Datenmodelle

- `MemoryEntry` Basis-Klasse (alle Schichten erben davon)
- `DNABelief` Modell:
  ```python
  class DNABelief(BaseModel):
      id: str
      belief: str
      confidence: float = Field(ge=0.0, le=1.0)
      evidence_count: int = 0
      last_validated: datetime
      stability_score: float
      category: Literal["preference", "rule", "value", "trait"]
  ```
- Weitere Modelle: `CoreEntry`, `WikiEntry`, `SkillEntry`, `DumpEntry`, `MetaEntry`

### 1.2 Memory Dynamics

- `calculate_memory_score()` Funktion:
  ```python
  def calculate_memory_score(entry: MemoryEntry) -> float:
      return (
          entry.relevance * 0.35 +
          entry.recency * 0.25 +
          entry.usage * 0.20 +
          entry.confidence * 0.15 +
          entry.stability * 0.05
      )
  ```
- `ForgettingState` Enum: `ACTIVE → COOLING → ARCHIVED → DELETED`
- Zustandsübergänge: Timer-basiert + Score-basiert
- `usage_count` Tracking bei jedem `vfs.cat()` Zugriff

### 1.3 Embedding-Pipeline

- `sentence-transformers/all-MiniLM-L6-v2` als lokales Modell (80MB, 384 Dim)
- Embedding bei jedem `vfs.write()` automatisch berechnen
- Speicherung als BLOB in SQLite
- `sqlite-vss` Extension für Vector-Search (FAISS als Fallback)

### 1.4 Schicht-spezifische Logik

| Schicht | Pfad | Schreibzugriff | Stabilität |
|---|---|---|---|
| CORE/DNA | `CORE/` | Nur Nightdream | Hoch |
| DUMPS | `DUMPS/` | Jeder | Niedrig (initial) |
| USER_WIKI | `USER_WIKI/` | Manuell editierbar | Mittel |
| SKILLS | `SKILLS/` | Dream + manuell | Mittel-Hoch |
| META | `META/` | System | Intern |

**Abhängigkeit:** Phase 0 (VFS + SQLite müssen stehen)

**Deliverables:**
- [ ] Alle Pydantic-Modelle für jede Memory-Schicht
- [ ] `calculate_memory_score()` + Forgetting-State-Machine
- [ ] Embedding-Pipeline mit automatischer Berechnung bei Write
- [ ] Vector-Search über sqlite-vss oder FAISS

---

## Phase 2: Dream Engine + Scheduler (4–7 Tage)

### 2.1 Daydream (leichtgewichtig, häufig)

- **Trigger:** Alle 10 Min. ODER nach >10 neuen Dumps
- **Aufgaben:** Tags extrahieren, Duplikate erkennen, einfache Verlinkungen
- **Kein LLM nötig** – regelbasiert + Embedding-Ähnlichkeit

### 2.2 Nightdream (tiefgehend, täglich)

- **Trigger:** Täglich 03:00 Uhr ODER `braindump dream now --type nightdream`
- **LLM-gestützt** (Ollama / llama.cpp):
  - Wissen konsolidieren
  - Widersprüche erkennen
  - DNA-Beliefs aktualisieren
- **Darf in `CORE/` schreiben** (einziger Prozess mit dieser Berechtigung)
- Confidence- und Stability-Scores neu berechnen

### 2.3 Deepdream (manuell, selten)

- **Trigger:** Nur manuell oder bei >2h Idle-Time
- Tiefe Reorganisation: Cluster bilden, Meta-Wissen generieren
- Graph-Analyse über alle Verlinkungen

### 2.4 Scheduler-Infrastruktur

- `asyncio.TaskGroup` für Background-Tasks
- Konfigurierbare Intervalle über `config.toml`:
  ```toml
  [dream]
  daydream_interval_minutes = 10
  nightdream_time = "03:00"
  deepdream_min_idle_hours = 2
  ```
- Trigger-Registry: Events → Dream-Typen zuordnen
- Micro-Processing nach jeder Interaktion

**Abhängigkeit:** Phase 0 + Phase 1

**Deliverables:**
- [ ] Daydream-Prozessor (regelbasiert)
- [ ] Nightdream-Prozessor (LLM-gestützt)
- [ ] Deepdream-Prozessor (Graph-Analyse)
- [ ] Async-Scheduler mit konfigurierbaren Triggern

---

## Phase 3: Retrieval Engine + Agent Loop (3 Tage)

### 3.1 Retrieval Engine

- Semantische Suche via sqlite-vss / FAISS
- Keyword-Suche als Fallback
- Hybrid-Ranking: Embedding-Similarität + Memory-Score
- `build_working_memory(query)`: relevanteste Einträge für einen Query zusammenstellen

### 3.2 Agent Loop

```python
async def agent_loop(input_text: str):
    working_memory = await vfs.build_working_memory(input_text)
    response = await llm.generate(working_memory, dna_injected=True)
    await vfs.dump_raw_interaction(input_text, response)
    await dream_engine.trigger_micro_processing()
    return response
```

- LLM-Abstraktionsschicht (Ollama Client, ggf. llama-cpp-python Bindings)
- DNA-Injection: Persönlichkeit/Präferenzen aus CORE/ in jeden Prompt

**Abhängigkeit:** Phase 0–2

**Deliverables:**
- [ ] Retrieval Engine mit Hybrid-Ranking
- [ ] Working-Memory-Builder
- [ ] Agent Loop mit LLM-Integration
- [ ] DNA-Injection-Mechanismus

---

## Phase 4: CLI + Sicherheit (2–3 Tage)

### 4.1 CLI mit Typer

| Befehl | Beschreibung |
|---|---|
| `braindump vfs ls <path>` | VFS durchsuchen |
| `braindump vfs cat <path>` | Datei lesen |
| `braindump dream now --type <type>` | Dream manuell triggern |
| `braindump memory review dna` | DNA-Beliefs prüfen |
| `braindump search "<query>" --semantic` | Semantische Suche |
| `braindump config set <key> <value>` | Konfiguration ändern |
| `braindump backup --full` | ZIP + SQLite-Dump |

- Rich für Terminal-Ausgabe, Marko für Markdown-Rendering

### 4.2 Sicherheit

- **SecurityScanner:** Prompt-Injection-Guard beim Lesen von Dateien
- **Namespace-Isolation:** `CORE/` nur für Nightdream schreibbar (enforced im VFS)
- **Audit-Log:** Alle VFS-Operationen → `META/audit.log`
- **Backup:** `braindump backup --full` → ZIP + SQLite-Dump

**Abhängigkeit:** Phase 0–3

**Deliverables:**
- [ ] Vollständige CLI mit allen Befehlen
- [ ] SecurityScanner für Prompt-Injection
- [ ] Audit-Log-System
- [ ] Backup-Mechanismus

---

## Phase 5: FUSE Mount + TUI (optional, nach MVP)

### 5.1 pyfuse3 Mount-Modus

- `FuseVFS` Klasse die `VFS` Protocol implementiert
- Mount unter `/mnt/braindump`
- Read/Write-Operationen an VirtualVFS delegieren

### 5.2 TUI (Textual)

- Dashboard mit Memory-Übersicht
- Dream-Status-Anzeige
- Interaktive Suche

**Abhängigkeit:** Phase 0–4

---

## Phase 6: Tests + Release

### 6.1 Testing-Strategie

- **Unit-Tests:** VFS-Handler, Memory-Score-Berechnung, Forgetting-States
- **Integration-Tests:** SQLite + Embeddings, Dream-Pipeline (`pytest-asyncio`)
- **E2E-Tests:** Volle Agent-Loop mit Ollama

### 6.2 Dokumentation

- README.md mit Setup-Anleitung
- Architektur-Diagramm
- Config-Referenz

---

## Abhängigkeits-Graph

```
Phase 0 (Core + VFS)
    ↓
Phase 1 (Memory + Embeddings)
    ↓
Phase 2 (Dream Engine)
    ↓
Phase 3 (Retrieval + Agent)
    ↓
Phase 4 (CLI + Security)
    ↓
Phase 5 (FUSE + TUI)  ←  optional
    ↓
Phase 6 (Tests + Release)
```

---

## Kritische Entscheidungen

| Entscheidung | Empfehlung | Grund |
|---|---|---|
| Embedding-Modell | `all-MiniLM-L6-v2` zuerst | Kleiner (80MB), schnell, gut genug für MVP |
| Vector-DB | `sqlite-vss` mit FAISS-Fallback | Alles in einer DB, einfacher |
| LLM | Ollama mit `llama3` oder `mistral` | Einfachstes lokales Setup |
| VFS Start | Virtual-Modus zuerst | FUSE braucht Root, ist komplexer |
| Async Framework | `asyncio` nativ | Kein extra Framework nötig |

---

## Geschätzter Gesamtaufwand

| Phase | Dauer | Kumulativ |
|---|---|---|
| Phase 0 | 1–2 Tage | 1–2 Tage |
| Phase 1 | 3–5 Tage | 4–7 Tage |
| Phase 2 | 4–7 Tage | 8–14 Tage |
| Phase 3 | 3 Tage | 11–17 Tage |
| Phase 4 | 2–3 Tage | 13–20 Tage |
| Phase 5 | 3–5 Tage | 16–25 Tage (optional) |
| Phase 6 | 3–5 Tage | 19–30 Tage |

**MVP (Phase 0–3): ca. 2–3 Wochen**
**Vollständig (Phase 0–6): ca. 4–5 Wochen**
