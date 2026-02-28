# Importiere die zentrale MCP-Instanz und den Context aus der eigenen App
import json
from mcp_openalex import mcp
from mcp.types import Icon

TRADES: dict[str, dict] = {
  # ── Bauhauptgewerbe ────────────────────────────────────────────────────────
  "maurer_betonbauer": {
    "name": "Maurer und Betonbauer",
    "aliases": ["Maurer", "Betonbauer", "Maurerhandwerk", "Hochbau"],
    "gewerbe": "Bauhauptgewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "zimmerer": {
    "name": "Zimmerer",
    "aliases": ["Zimmermann", "Zimmerei", "Holzbau", "Dachstuhl"],
    "gewerbe": "Bauhauptgewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "dachdecker": {
    "name": "Dachdecker",
    "aliases": ["Dachdecker", "Dachdeckerhandwerk", "Bedachung", "Dach"],
    "gewerbe": "Bauhauptgewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "strassenbauer": {
    "name": "Strassenbauer",
    "aliases": ["Straßenbauer", "Tiefbau", "Pflasterer", "Wegebau"],
    "gewerbe": "Bauhauptgewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "waermekaelte": {
    "name": "Wärme- und Kälte- und Schalschutzisolierer",
    "aliases": ["Isolierer", "Wärmeschutzisolierer", "Kälteschutzisolierer", "Dämmung"],
    "gewerbe": "Bauhauptgewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "brunnenbauer": {
    "name": "Brunnenbauer",
    "aliases": ["Brunnenbauer", "Bohrbrunnen", "Brunnenbau"],
    "gewerbe": "Bauhauptgewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "geruestbauer": {
    "name": "Gerüstbauer",
    "aliases": ["Gerüstbauer", "Gerüstbau", "Einrüstung"],
    "gewerbe": "Bauhauptgewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "werkstein_terrazzo": {
    "name": "Werkstein- und Terrazzohersteller",
    "aliases": ["Werksteinmacher", "Terrazzoleger", "Betonwerkstein", "Terrazzo"],
    "gewerbe": "Bauhauptgewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "holz_bauenschuetzer": {
    "name": "Holz- und Bautenschützer",
    "aliases": ["Holzschützer", "Bautenschützer", "Korrosionsschutz", "Holzschutz"],
    "gewerbe": "Bauhauptgewerbe",
    "zulassungspflichtig": False,
    "description": ""
  },

  # ── Ausbaugewerbe ──────────────────────────────────────────────────────────
  "ofen_luftheizungsbauer": {
    "name": "Ofen- und Luftheizungsbauer",
    "aliases": ["Ofenbauer", "Kaminbauer", "Kachelofen", "Kaminofen"],
    "gewerbe": "Ausbaugewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "stuckatuer": {
    "name": "Stuckateure",
    "aliases": ["Stuckateur", "Verputzer", "Putzer", "Stuckarbeit"],
    "gewerbe": "Ausbaugewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "malerei_lackierer": {
    "name": "Maler und Lackierer",
    "aliases": ["Maler", "Lackierer", "Anstreicher", "Malerhandwerk"],
    "gewerbe": "Ausbaugewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "klempner": {
    "name": "Klempner",
    "aliases": ["Klempner", "Spengler", "Flaschner", "Dachklempner"],
    "gewerbe": "Ausbaugewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "installateur_heizungsbauer": {
    "name": "Installateur und Heizungsbauer",
    "aliases": ["Installateur", "Heizungsbauer", "Sanitärinstallateur", "SHK", "Gas-Wasser"],
    "gewerbe": "Ausbaugewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "elektrotechniker": {
    "name": "Elektrotechniker",
    "aliases": ["Elektriker", "Elektroinstallateur", "Elektrik", "Starkstrom"],
    "gewerbe": "Ausbaugewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "tischler": {
    "name": "Tischler",
    "aliases": ["Tischler", "Schreiner", "Möbeltischler", "Schreinerei"],
    "gewerbe": "Ausbaugewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "glaser": {
    "name": "Glaser",
    "aliases": ["Glaser", "Glaserei", "Verglasung", "Fensterbauer"],
    "gewerbe": "Ausbaugewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "fliesen_platten_mosaik_leger": {
    "name": "Fliesen-, Platten- und Mosaikleger",
    "aliases": ["Fliesenleger", "Plattenleger", "Mosaikleger", "Fliesen"],
    "gewerbe": "Ausbaugewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "estrich_leger": {
    "name": "Estrichleger",
    "aliases": ["Estrichleger", "Estrichbauer", "Bodenbelag", "Fußbodenheizung"],
    "gewerbe": "Ausbaugewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "parkettleger": {
    "name": "Parkettleger",
    "aliases": ["Parkettleger", "Bodenleger", "Parkettboden", "Parkett"],
    "gewerbe": "Ausbaugewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "rollladen_sonnen": {
    "name": "Rollladen- und Sonnenschutztechniker",
    "aliases": ["Rollladenbauer", "Sonnenschutztechniker", "Jalousie", "Markise"],
    "gewerbe": "Ausbaugewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "raumausstatter": {
    "name": "Raumausstatter",
    "aliases": ["Raumausstatter", "Raumgestalter", "Polsterer", "Tapezierer"],
    "gewerbe": "Ausbaugewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },

  # ── Handwerk für den gewerblichen Bedarf ───────────────────────────────────
  "metallbauer": {
    "name": "Metallbauer",
    "aliases": ["Metallbauer", "Schlosser", "Stahlbauer", "Schlosserei"],
    "gewerbe": "Handwerk für den gewerblichen Bedarf",
    "zulassungspflichtig": True,
    "description": ""
  },
  "chirurgiemechaniker": {
    "name": "Chirurgiemechaniker",
    "aliases": ["Chirurgiemechaniker", "Medizintechnik", "chirurgische Instrumente"],
    "gewerbe": "Handwerk für den gewerblichen Bedarf",
    "zulassungspflichtig": True,
    "description": ""
  },
  "feinwerkmechaniker": {
    "name": "Feinwerkmechaniker",
    "aliases": ["Feinwerkmechaniker", "Feinmechaniker", "Gerätebauer", "Mechatronik"],
    "gewerbe": "Handwerk für den gewerblichen Bedarf",
    "zulassungspflichtig": True,
    "description": ""
  },
  "kaelteanlagenbauer": {
    "name": "Kälteanlagenbauer",
    "aliases": ["Kälteanlagenbauer", "Kältetechniker", "Klimatechnik", "Kühlanlagen"],
    "gewerbe": "Handwerk für den gewerblichen Bedarf",
    "zulassungspflichtig": True,
    "description": ""
  },
  "informationstechniker": {
    "name": "Informationstechniker",
    "aliases": ["Informationstechniker", "IT-Techniker", "Netzwerktechniker", "EDV"],
    "gewerbe": "Handwerk für den gewerblichen Bedarf",
    "zulassungspflichtig": True,
    "description": ""
  },
  "land_baumaschinen_mechatroniker": {
    "name": "Land- und Baumaschinenmechatroniker",
    "aliases": ["Landmaschinenmechaniker", "Baumaschinenmechaniker", "Agrartechnik", "Landmaschinen"],
    "gewerbe": "Handwerk für den gewerblichen Bedarf",
    "zulassungspflichtig": True,
    "description": ""
  },
  "buchsenmacher": {
    "name": "Büchsenmacher",
    "aliases": ["Büchsenmacher", "Waffenmacher", "Waffenschmied"],
    "gewerbe": "Handwerk für den gewerblichen Bedarf",
    "zulassungspflichtig": True,
    "description": ""
  },
  "elektromaschinenbauer": {
    "name": "Elektromaschinenbauer",
    "aliases": ["Elektromaschinenbauer", "Motorenbauer", "Elektromotoren", "Generatoren"],
    "gewerbe": "Handwerk für den gewerblichen Bedarf",
    "zulassungspflichtig": True,
    "description": ""
  },
  "seiler": {
    "name": "Seiler",
    "aliases": ["Seiler", "Seilerei", "Seile", "Taue"],
    "gewerbe": "Handwerk für den gewerblichen Bedarf",
    "zulassungspflichtig": True,
    "description": ""
  },
  "glasblaser_glasapparatebauer": {
    "name": "Glasbläser und Glasapparatebauer",
    "aliases": ["Glasbläser", "Glasapparatebauer", "Laborglas", "Glasrohr"],
    "gewerbe": "Handwerk für den gewerblichen Bedarf",
    "zulassungspflichtig": True,
    "description": ""
  },
  "behalter_apparatebauer": {
    "name": "Behälter- und Apparatebauer",
    "aliases": ["Behälterbauer", "Apparatebauer", "Druckbehälter", "Kesselschmiede"],
    "gewerbe": "Handwerk für den gewerblichen Bedarf",
    "zulassungspflichtig": True,
    "description": ""
  },
  "bottcher": {
    "name": "Böttcher",
    "aliases": ["Böttcher", "Küfer", "Fassmacher", "Tonnenmacher"],
    "gewerbe": "Handwerk für den gewerblichen Bedarf",
    "zulassungspflichtig": True,
    "description": ""
  },
  "glasveredler": {
    "name": "Glasveredler",
    "aliases": ["Glasveredler", "Glasschleifer", "Glasätzer", "Glasbearbeitung"],
    "gewerbe": "Handwerk für den gewerblichen Bedarf",
    "zulassungspflichtig": True,
    "description": ""
  },
  "schilder_lichtreklamehersteller": {
    "name": "Schilder- und Lichtreklamehersteller",
    "aliases": ["Schildermacher", "Lichtreklamehersteller", "Werbetechnik", "Beschriftung"],
    "gewerbe": "Handwerk für den gewerblichen Bedarf",
    "zulassungspflichtig": True,
    "description": ""
  },
  "metallbildner": {
    "name": "Metallbildner",
    "aliases": ["Metallbildner", "Kunstschlosser", "Kunstschmied", "Zierschmiede"],
    "gewerbe": "Handwerk für den gewerblichen Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "galvaniseure": {
    "name": "Galvaniseure",
    "aliases": ["Galvaniseur", "Galvanisierung", "Oberflächentechnik", "Eloxierung"],
    "gewerbe": "Handwerk für den gewerblichen Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "praezisionswerkzeugmechaniker": {
    "name": "Präzisionswerkzeugmechaniker",
    "aliases": ["Werkzeugmacher", "Präzisionsmechaniker", "Werkzeugbau", "Formenbau"],
    "gewerbe": "Handwerk für den gewerblichen Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "modellbauer": {
    "name": "Modellbauer",
    "aliases": ["Modellbauer", "Prototypenbau", "Formenbauer", "Musterbauer"],
    "gewerbe": "Handwerk für den gewerblichen Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "gebaudereiniger": {
    "name": "Gebäudereiniger",
    "aliases": ["Gebäudereiniger", "Reinigungskraft", "Unterhaltsreinigung", "Fensterreinigung"],
    "gewerbe": "Handwerk für den gewerblichen Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "feinoptiker": {
    "name": "Feinoptiker",
    "aliases": ["Feinoptiker", "Optikmechaniker", "Linsen", "optische Instrumente"],
    "gewerbe": "Handwerk für den gewerblichen Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "glas_und_porzellanmaler": {
    "name": "Glas- und Porzellanmaler",
    "aliases": ["Glasmaler", "Porzellanmaler", "Emailmaler", "Kirchenfenster"],
    "gewerbe": "Handwerk für den gewerblichen Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "edelsteinschleifer": {
    "name": "Edelsteinschleifer",
    "aliases": ["Edelsteinschleifer", "Juwelier", "Schmuckstein", "Diamantschleifer"],
    "gewerbe": "Handwerk für den gewerblichen Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "buchbinder": {
    "name": "Buchbinder",
    "aliases": ["Buchbinder", "Buchbinderei", "Buchrestaurator", "Einbandgestalter"],
    "gewerbe": "Handwerk für den gewerblichen Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "print_und_medientechnologen": {
    "name": "Print- und Medientechnologen",
    "aliases": ["Drucker", "Medientechniker", "Offsetdruck", "Printmedien", "Druckerei"],
    "gewerbe": "Handwerk für den gewerblichen Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },

  # ── Kraftfahrzeuggewerbe ───────────────────────────────────────────────────
  "karosserie_und_fahrzeugbauer": {
    "name": "Karosserie- und Fahrzeugbauer",
    "aliases": ["Karosseriebauer", "Fahrzeugbauer", "Karosserieschlosser", "Autobau"],
    "gewerbe": "Kraftfahrzeuggewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "zweiradmechaniker": {
    "name": "Zweiradmechaniker",
    "aliases": ["Zweiradmechaniker", "Motorradmechaniker", "Fahrradmechaniker", "Motorrad"],
    "gewerbe": "Kraftfahrzeuggewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "kraftfahrzeugtechniker": {
    "name": "Kraftfahrzeugtechniker",
    "aliases": ["KFZ-Mechaniker", "KFZ-Techniker", "Automechaniker", "KFZ", "Auto"],
    "gewerbe": "Kraftfahrzeuggewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "mechaniker_reifen_vulkanisation": {
    "name": "Mechaniker für Reifen- und Vulkanisationstechnik",
    "aliases": ["Reifenmonteur", "Vulkaniseur", "Reifenhandwerk", "Reifenservice"],
    "gewerbe": "Kraftfahrzeuggewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },

  # ── Gesundheitsgewerbe ─────────────────────────────────────────────────────
  "augenoptiker": {
    "name": "Augenoptiker",
    "aliases": ["Augenoptiker", "Optiker", "Brillenmacher", "Kontaktlinsen"],
    "gewerbe": "Gesundheitsgewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "hoerakustiker": {
    "name": "Hörakustiker",
    "aliases": ["Hörakustiker", "Hörgeräteakustiker", "Hörgeräte", "Akustiker"],
    "gewerbe": "Gesundheitsgewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "orthopaeditechniker": {
    "name": "Orthopädietechniker",
    "aliases": ["Orthopädietechniker", "Orthopädiemechaniker", "Prothesenbauer", "Orthesen"],
    "gewerbe": "Gesundheitsgewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "orthopaedieschuhmacher": {
    "name": "Orthopädieschuhmacher",
    "aliases": ["Orthopädieschuhmacher", "Orthopädieschuhe", "Einlagen", "Maßschuhe"],
    "gewerbe": "Gesundheitsgewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "zahntechniker": {
    "name": "Zahntechniker",
    "aliases": ["Zahntechniker", "Zahntechnik", "Dentalhandwerk", "Zahnprothesen"],
    "gewerbe": "Gesundheitsgewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },

  # ── Lebensmittelgewerbe ────────────────────────────────────────────────────
  "baecker": {
    "name": "Bäcker",
    "aliases": ["Bäcker", "Bäckerei", "Backhandwerk", "Brot", "Konditorei"],
    "gewerbe": "Lebensmittelgewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "konditoren": {
    "name": "Konditoren",
    "aliases": ["Konditor", "Konditorei", "Patisserie", "Confiserie", "Törtchen"],
    "gewerbe": "Lebensmittelgewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "fleischer": {
    "name": "Fleischer",
    "aliases": ["Fleischer", "Metzger", "Schlachter", "Metzgerei", "Fleischerei"],
    "gewerbe": "Lebensmittelgewerbe",
    "zulassungspflichtig": True,
    "description": ""
  },
  "mueller": {
    "name": "Müller",
    "aliases": ["Müller", "Mühle", "Mehl", "Getreideverarbeitung"],
    "gewerbe": "Lebensmittelgewerbe",
    "zulassungspflichtig": False,
    "description": ""
  },
  "brauer_maelzer": {
    "name": "Brauer und Mälzer",
    "aliases": ["Brauer", "Mälzer", "Brauerei", "Bierbrauer", "Bier"],
    "gewerbe": "Lebensmittelgewerbe",
    "zulassungspflichtig": False,
    "description": ""
  },
  "weinkuefer": {
    "name": "Weinküfer",
    "aliases": ["Weinküfer", "Küfer", "Fassbinder", "Weinfass", "Wein"],
    "gewerbe": "Lebensmittelgewerbe",
    "zulassungspflichtig": False,
    "description": ""
  },

  # ── Handwerke für den privaten Bedarf ─────────────────────────────────────
  "steinmetz_bildhauer": {
    "name": "Steinmetzen und Bildhauer",
    "aliases": ["Steinmetz", "Bildhauer", "Grabstein", "Naturstein", "Steinbearbeitung"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": True,
    "description": ""
  },
  "schornsteinfeger": {
    "name": "Schornsteinfeger",
    "aliases": ["Schornsteinfeger", "Kaminkehrer", "Kaminfeger", "Schornstein"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": True,
    "description": ""
  },
  "bootbauer_schiffbauer": {
    "name": "Boots- und Schiffbauer",
    "aliases": ["Bootsbauer", "Schiffbauer", "Bootsbau", "Yacht", "Segelboot"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": True,
    "description": ""
  },
  "friseur": {
    "name": "Friseure",
    "aliases": ["Friseur", "Frisör", "Haarstylist", "Coiffeur", "Haare"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": True,
    "description": ""
  },
  "drechsler": {
    "name": "Drechsler (Elfenbeinschnitzer) und Holzspielzeugmacher",
    "aliases": ["Drechsler", "Elfenbeinschnitzer", "Holzspielzeugmacher", "Holzdrehen"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": True,
    "description": ""
  },
  "orgel_und_harmoniumbauer": {
    "name": "Orgel- und Harmoniumbauer",
    "aliases": ["Orgelbauer", "Harmoniumbauer", "Kirchenorgel", "Orgel"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": True,
    "description": ""
  },
  "uhrenmacher": {
    "name": "Uhrenmacher",
    "aliases": ["Uhrmacher", "Uhrenreparatur", "Zeitmessung", "Uhren"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "graveure": {
    "name": "Graveure",
    "aliases": ["Graveur", "Gravieren", "Stempelschneider", "Siegelstecher"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "gold_und_silberschmiede": {
    "name": "Gold- und Silberschmiede",
    "aliases": ["Goldschmied", "Silberschmied", "Juwelier", "Schmuck"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "holzbildhauer": {
    "name": "Holzbildhauer",
    "aliases": ["Holzbildhauer", "Holzschnitzer", "Schnitzerei", "Bildschnitzer"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "korb_und_flechtwerkgestalter": {
    "name": "Korb- und Flechtwerkgestalter",
    "aliases": ["Korbmacher", "Flechtwerkgestalter", "Korbflechter", "Weidenkorb"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "maesschneider": {
    "name": "Maßschneider",
    "aliases": ["Maßschneider", "Schneider", "Schneiderei", "Herrenmaßschneider"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "textilgestalter": {
    "name": "Textilgestalter (Sticker, Weber, Klöppler, Posamentierer, Stricker)",
    "aliases": ["Textilgestalter", "Sticker", "Weber", "Stricker", "Klöppler"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "modisten": {
    "name": "Modisten",
    "aliases": ["Modistin", "Hutmacher", "Hutmacherin", "Modisterei"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "segelmacher": {
    "name": "Segelmacher",
    "aliases": ["Segelmacher", "Segelbau", "Segel", "Persenning"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "kuerschner": {
    "name": "Kürschner",
    "aliases": ["Kürschner", "Pelzmacher", "Pelzverarbeitung", "Fell"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "schuhmacher": {
    "name": "Schuhmacher",
    "aliases": ["Schuhmacher", "Schuster", "Schuhreparatur", "Schuhhandwerk"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "sattler_und_feintascher": {
    "name": "Sattler und Feintascher",
    "aliases": ["Sattler", "Feintascher", "Lederwaren", "Riemer"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "textilreiniger": {
    "name": "Textilreiniger",
    "aliases": ["Textilreiniger", "Reinigung", "Chemischreinigung", "Wäscherei"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "wachszieher": {
    "name": "Wachszieher",
    "aliases": ["Wachszieher", "Kerzenmacher", "Kerzen", "Wachs"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "fotografen": {
    "name": "Fotografen",
    "aliases": ["Fotograf", "Fotografin", "Fotostudio", "Fotografie"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "keramiker": {
    "name": "Keramiker",
    "aliases": ["Keramiker", "Töpfer", "Töpferei", "Steinzeug"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "klavier_und_cembalobauer": {
    "name": "Klavier- und Cembalobauer",
    "aliases": ["Klavierbauer", "Cembalobauer", "Pianoforte", "Klavierstimmer"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "handzuginstrumentenmacher": {
    "name": "Handzuginstrumentenmacher",
    "aliases": ["Akkordeonbauer", "Ziehharmonika", "Handzuginstrument", "Harmonika"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "geigenbauer": {
    "name": "Geigenbauer",
    "aliases": ["Geigenbauer", "Violinbauer", "Streichinstrumentenbauer", "Viola"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "bogenmacher": {
    "name": "Bogenmacher",
    "aliases": ["Bogenmacher", "Streichbogen", "Geigenbogen", "Bogenbau"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "metallblasinstrumentenmacher": {
    "name": "Metallblasinstrumentenmacher",
    "aliases": ["Trompetenbauer", "Hornbauer", "Blechblasinstrument", "Tuba"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "holzblasinstrumentenmacher": {
    "name": "Holzblasinstrumentenmacher",
    "aliases": ["Flötenbauer", "Klarinettenbauer", "Holzblasinstrument", "Oboe"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "zupfinstrumentenmacher": {
    "name": "Zupfinstrumentenmacher",
    "aliases": ["Gitarrenbauer", "Lautenbauer", "Zupfinstrumentenbauer", "Harfenbauer"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "vergoldner": {
    "name": "Vergoldner",
    "aliases": ["Vergolder", "Blattgold", "Vergoldung", "Goldauflage"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "bestatter": {
    "name": "Bestatter",
    "aliases": ["Bestatter", "Bestattungsunternehmer", "Beerdigung", "Beerdigungsinstitut"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  },
  "kosmetiker": {
    "name": "Kosmetiker",
    "aliases": ["Kosmetiker", "Kosmetikerin", "Kosmetiksalon", "Schönheitspflege"],
    "gewerbe": "Handwerke für den privaten Bedarf",
    "zulassungspflichtig": False,
    "description": ""
  }
}

# ── Lookup helpers ─────────────────────────────────────────────────────────────

def _find_trade(slug: str) -> tuple[str, dict] | tuple[None, None]:
  """Return (canonical_slug, trade_data) for a slug or alias, or (None, None)."""
  key = slug.lower().strip()
  if key in TRADES:
      return key, TRADES[key]
  for canonical, data in TRADES.items():
      if key in data.get("aliases", []):
          return canonical, data
  return None, None


@mcp.resource(
  uri="trade://catalog",
  name="Trade Catalog",
  description="List all available trade profiles with their slugs and a short description.",
  mime_type="application/json",
  tags=["Handwerke", "Trade Profiles"],
  meta={
    "version": "1.0.0",
    "author": "Alex"
  },
  icons=[Icon(src="https://files.svgcdn.io/streamline/business-profession-home-office.svg")]
)
def trade_catalog() -> str:
  """List all available trade profiles with their slugs and a short description.

  Read this first to find the correct slug before fetching a full trade profile.
  """
  groups: dict[str, list] = {}
  for slug, data in TRADES.items():
    gewerbe = data["gewerbe"]
    groups.setdefault(gewerbe, []).append({
      "slug": slug,
      "name": data["name"],
      "aliases": data.get("aliases", []),
    })
  return json.dumps(
    {"usage": "trade://{slug}", "groups": groups},
    ensure_ascii=False,
    indent=2,
  )

@mcp.resource("trade://{slug}")
def trade_profile(slug: str) -> str:
  """Full profile for a specific trade: description, research topics, and OpenAlex search keywords.

  Read this before calling search_works or filter_works for a trade-specific query.
  The 'keywords' field contains ready-to-use search terms for OpenAlex.
  The 'topics' field lists relevant research areas for understanding the domain.
  The 'related_trades' field lists slugs of trades with overlapping interests.

  Args:
      slug: Trade identifier. Check trade://catalog for available slugs and aliases.
  """
  canonical, data = _find_trade(slug)
  if data is None:
    available = ", ".join(TRADES.keys())
    return (
      f"Unknown trade slug: '{slug}'.\n"
      f"Available slugs: {available}\n"
      f"Tip: Also try aliases — see trade://catalog for details."
    )

  return (
    f"# {data['name']}\n"
    f"## Description: {data['description']}"
  )