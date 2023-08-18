# Symbolleisten erkunden #

* Autor: Alberto Buffolino
* [Stabile Version herunterladen][1]
* [Entwicklerversion herunterladen][2]

Diese NVDA-Erweiterung erleichtert die Verwendung von Symbolleisten in
Anwendungen und bietet ein Erkundungsmodell, das durch Objektnavigation mit
vereinfachten Tastenbefehlen abgeleitet wird.

## Befehle

* Alt+Anwendungstaste: Startet die Erkundung der Symbolleisten<br/>
(Den Tastenbefehl können Sie unter dem Dialog "Eingaben" unter Objekt-Navigation neu zuordnen).

Während der Erkundung stehen folgende Gesten zur Verfügung:

* Pfeil nach links/rechts: Zur nächsten/vorherigen Symbolleiste bewegen;
* Pfeil nach oben/unten: navigiert zwischen den Einträgen in der aktuellen
  Symbolleiste;
* Eingabetaste: Aktiviert die Symbolleiste oder den Eintrag;
* Leertaste: Simuliert einen linken Mausklick auf der Symbolleiste oder auf
  dem Element;
* Anwendung(kontextmenü)/Umschalt+F10: Simuliert den rechten Mausklick auf
  die Symbolleiste oder dem Element;
* Escape: Beendet das Erkunden der Symbolleisten.

Darüber hinaus können Sie Aktionen auf Symbolleisten oder deren Elementen
mit jeder von NVDA bereit gestellten Geste ausführen, genau so wie beim
Bewegen zu Objekten mit Objekt-Navigation.

## Anmerkungen

Die Erkundung wird explizit durch Drücken von escape beendet. Außerdem
beenden folgende Aktionen implizit die Erkundung:

* Ausführen einer Aktion auf der Symbolleiste oder einem Element (mit
  Leerzeichen, Anwendungstaste/Umschalt+F10, Eingabetaste);
* Drücken einer Geste, die den fokus vom aktuellen Objekten der Symbolleiste
  wegbewegt (z.B. alt, Windows-Taste, Tab-Taste, NVDA+F1,
  Objektnavigationsgesten etc.).

Andere Gesten, die keine Alt- oder Windows-taste enthalten (wie z.B. H, 1,
Umschalt, Umschalt+H, Strg+Z) führen zu keiner Aktion.

## Vorschläge für Problemlösungen

* Die Erweiterung kann möglicherweise in Mozilla-Anwendungen beim ersten Mal
  nach der Installation/Aktualisierung fehlschlagen; bitte starten Sie NVDA-
  und die Mozilla-Anwendungen neu, um das Problem zu lösen;
* In LibreOffice ist die beste Konfiguration wahrscheinlich die Standard-
  oder klassische Symbolleiste. Stellen Sie dies im Menü Ansicht /
  Werkzeugleisten ein.


[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=toolbarsExplorer

[2]: https://www.nvaccess.org/addonStore/legacy?file=toolbarsExplorer-dev
