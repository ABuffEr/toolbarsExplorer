# Symbolleisten erkunden #

* Autor: Alberto Buffolino
* [Stabile Version herunterladen][1]
* [Testversion herunterladen][2]

Diese Erweiterung erleichtert die Verwendung von Symbolleisten in
Anwendungen und bietet ein Erkundungsmodell, das durch Objektnavigation mit
vereinfachten Gesten abgeleitet wird.

## Befehle

Alt+Anwendungen: Startet die Erkundung der Symbolleisten<br/>.
(Sie können es über die NVDA-Gesten, unter Objekt-Navigation, neu zuordnen).

Während der Erkundung stehen folgende Gesten zur Verfügung:

* Pfeil nach links/rechts: Zur nächsten/vorherigen Symbolleiste bewegen.
* Pfeil nach oben/unten: Geht durch die Einträge in der aktuellen
  Symbolleiste.
* Eingabetaste: Aktiviert die Symbolleiste oder den Eintrag.
* Leertaste: Simuliert einen Mausklick mit der linken Taste auf der
  Symbolleiste oder auf dem Element.
* Anwendung/Umschalt+F10: Simuliert den rechten Mausklick auf die
  Symbolleiste oder deren Element.
* Escape: Beendet das Erkunden der Symbolleisten.

Darüber hinaus können Sie Aktionen auf Symbolleisten oder deren Elementen
mit jeder von NVDA bereit gestellten Geste ausführen, genau so wie beim
Bewegen zu Objekten mit Objekt-Navigation.

## Anmerkungen

Die Erkundung wird explizit durch Drücken von escape beendet.

* Ausführen einer Aktion auf der Symbolleiste oder einem Element (mit
  Leerzeichen, Anwendungen/Umschalt+F10, Enter).
* Drücken einer Geste, die sich aus den aktuellen Objekten der Symbolleiste
  herausbewegt (alt, Fenster, Registerkarte, NVDA+F1,
  Objektnavigationsgesten, etc.).

Andere Gesten, die keine Alt- oder Fenster enthalten (wie H, 1, Umschalt,
Umschalt, Umschalt+H, Strg+Z), tun einfach nichts.

## Vorschläge

* Die Erweiterung kann in Mozilla-Anwendungen beim ersten Mal nach der
  Installation/Aktualisierung des Add-ons fehlschlagen; bitte starten Sie
  NVDA- und Mozilla-Anwendungen neu, um die Lösung zu finden.
* In LibreOffice ist die beste Konfiguration wahrscheinlich die Standard-
  oder klassische Symbolleiste, setzen Sie sie im Menü Ansicht /
  Werkzeugleisten.


[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=tbx

[2]: https://addons.nvda-project.org/files/get.php?file=tbx-dev
