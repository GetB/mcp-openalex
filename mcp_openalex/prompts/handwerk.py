from fastmcp.prompts import Message
from mcp_openalex import mcp


@mcp.prompt(
  name="handwerk_recherche",
  description=(
    "Startet eine vollständige, geführte Literaturrecherche für ein Handwerksgewerk. "
    "Führt den Assistenten durch den Pflicht-Workflow: Catalog → Profil → "
    "Semantische Translation → OpenAlex-Suche."
  ),
  tags=["Handwerk", "Recherche", "Workflow"],
)
def handwerk_recherche(gewerk: str, thema: str) -> list[Message]:
  """Geführter Recherche-Workflow: vom Handwerksbegriff zur wissenschaftlichen Literatur.

  Args:
    gewerk: Das Handwerksgewerk des Nutzers (z.B. "Fleischer", "Elektriker").
    thema:  Das konkrete Recherchethema (z.B. "Räuchern", "Energieeinsparung").
  """
  return [
    Message(
      role="user",
      content=f"""Ich bin Handwerker im Bereich **{gewerk}** und suche wissenschaftliche Literatur zum Thema: **{thema}**

Bitte führe die Recherche in folgenden Schritten durch:

**Schritt 1 – Gewerk identifizieren**
Lies `trade://catalog`. Finde den Slug, der "{gewerk}" (oder einem Alias davon) entspricht.

**Schritt 2 – Fachprofil laden**
Lies `trade://{{slug}}`. Nutze die dort hinterlegten `keywords` und `topics` als Basis.

**Schritt 3 – Semantische Translation**
Übersetze "{thema}" in präzise wissenschaftliche Suchbegriffe auf Englisch.
Handwerkliche Alltagsbegriffe existieren in akademischen Datenbanken oft nicht direkt –
verwende das Prompt `semantic_translation_guide` als Referenz für das Mapping.

**Schritt 4 – Booleschen Suchstring aufbauen**
Kombiniere die Fachbegriffe aus Schritt 2 und 3 zu einem präzisen Query.
Nutze bevorzugt `filter_works` mit Topic-Filtern (1 Credit).
Die semantische Suche (`/find/works`) ist 1.000× teurer – nur einsetzen wenn
Keyword-Suche keine ausreichenden Ergebnisse liefert.

**Schritt 5 – Ergebnisse aufbereiten**
Präsentiere die Treffer verständlich: Titel, Jahr, Kernaussage, und warum das
Ergebnis für einen **{gewerk}**-Betrieb relevant ist.
""",
    )
  ]


@mcp.prompt(
  name="semantic_translation_guide",
  description=(
    "Referenz-Prompt: Erklärt die semantische Lücke zwischen handwerklicher "
    "Alltagssprache und wissenschaftlicher Nomenklatur. Enthält Mapping-Beispiele "
    "und die Strategie zur Konstruktion präziser OpenAlex-Queries."
  ),
  tags=["Handwerk", "Semantik", "Translation", "OpenAlex"],
)
def semantic_translation_guide() -> list[Message]:
  """Leitfaden zur semantischen Übersetzung vom Handwerksbegriff zur wissenschaftlichen Ontologie."""
  return [
    Message(
      role="user",
      content="""## Semantische Translation: Handwerksbegriff → Wissenschaftliche Ontologie

### Das Problem
Handwerker verwenden Alltagssprache. Wissenschaftliche Datenbanken (OpenAlex, PubMed)
verwenden standardisierte, meist englischsprachige Fachterminologie. Ein direktes
Mapping existiert nicht – der Assistent muss diese Lücke schließen.

### Pflicht-Workflow vor jeder Suche
1. `trade://catalog` lesen → korrekten Slug finden
2. `trade://{slug}` lesen → domänenspezifische Keywords und Topics laden
3. Erst dann `search_works` oder `filter_works` aufrufen

### Bekannte Mappings (Beispiele)

| Handwerklicher Begriff        | Wissenschaftliches Äquivalent                                          |
|-------------------------------|------------------------------------------------------------------------|
| Fleischerei / Metzgerhandwerk | Meat Science · Meat Processing · Charcuterie                           |
| Räuchern / Haltbarmachen      | Thermal processing · Curing · Polycyclic aromatic hydrocarbons (PAH)   |
| Lebensmittelsicherheit        | Food Safety · Antimicrobial Resistance · Pathogens · HACCP             |
| Handwerksbetrieb / KMU        | SME · Small and Medium-sized Enterprises · Craft enterprise            |
| Funktionelle Wurstwaren       | Functional Foods · Probiotics · Omega-3 fatty acids · Bioactive compounds |
| Elektrische Installation      | Electrical safety · Wiring systems · Low-voltage installation          |
| Energieeinsparung (Betrieb)   | Energy efficiency · Building energy performance · Retrofit             |
| Holzschutz / Oberflächenbehandlung | Wood preservation · Surface coating · Biocides                  |
| Schimmel / Feuchteschäden     | Mold growth · Moisture damage · Building pathology · Mycotoxins        |
| Lärm / Schallschutz           | Noise exposure · Occupational hearing loss · Sound insulation          |
| Staubbelastung (Handwerk)     | Occupational dust exposure · Silica dust · Respiratory hazards         |
| Digitalisierung im Handwerk   | Digitalization · SME technology adoption · Industry 4.0                |
| Fachkräftemangel              | Skilled labour shortage · Vocational training · Apprenticeship         |

### Strategie für den Suchstring

**Bevorzugt: Keyword-Suche mit Topic-Filtern (1 Credit)**
```
filter_works(query="meat processing SME innovation", topic_id="T12345")
```
Kombiniere 2–4 präzise englische Fachbegriffe mit AND/OR-Logik.
Ergänze Topic-IDs aus dem Trade-Profil für domänenspezifische Filterung.

**Fallback: Semantische Suche (1.000 Credits)**
Nur wenn Keyword-Suche < 5 relevante Treffer liefert oder das Thema sehr
unspezifisch ist. Nutze `/find/works` mit einem vollständigen Satz als Query.

### Hinweise zur Qualität
- Immer auf Englisch suchen, auch wenn der Nutzer auf Deutsch fragt
- Akronyme ergänzen: „KMU" → auch „SME" und „small business" suchen
- Traditionelle Verfahren haben oft moderne wissenschaftliche Entsprechungen:
  „Räuchern" → nicht nur „smoking" (veraltet), sondern „PAH reduction", „smoke flavoring"
- Betriebswirtschaftliche Fragen → Management-Literatur mit SME-Filter kombinieren
""",
    )
  ]
