# Udforsk Værktøjslinjer #

* Forfatter: Alberto Buffolino
* Download [stabil version][1]
* Download [udviklingsversion][2]

Denne tilføjelse gør det nemmere at bruge værktøjslinjer i applikationer,
der giver en udforskningsmodel, der er inspireret af objektnavigation, med
forenklede bevægelser.

## Kommandoer

* Alt+Applikationstast: Starter udforskning af værktøjslinjer.
( Du kan tildele en anden kommando til denne funktion ved brug af NVDA-dialogen "Inputbevægelser" under kategorien "Objektnavigation".

Under udforskningen er følgende kommandoer tilgængelige:

* Venstre/højre pil: Flytter til forrige/næste værktøjslinje;
* Pil op og ned: Går op og ned i aktuelle emner i den pågældende
  værktøjslinje;
* Enter: Aktiverer værktøjslinjen eller dens element;
* Mellemrum: Simulerer venstre museklik på værktøjslinjen eller dens
  element;
* Applikationstast/skift+F10: Simulerer højre museklik på værktøjslinjen
  eller dens element;
* Escape: Lukker udforskning.

Derudover kan du udføre handlinger på værktøjslinjer eller dens elementer
ved hjælp af enhver kommando, der leveres af NVDA, lige nøjagtigt som når du
flytter til objekter med objektnavigation.

## Bemærkninger

Udforskningen afsluttes udtrykkeligt ved at trykke på Escape og yderligere:

* Ved at udføre en handling på værktøjslinjen eller dens element (mellemrum,
  applikationstast/skift+F10, enter);
* Ved at trykke en kommando der flytter fokus fra det aktuelle objekt på en
  værktøjslinje (Alt, Windows, Tab, NVDA+F1, kommandoer til
  objektnavigation, osv.)

Andre kommandoer, der ikke indeholder Alt, Windows eller Escape (som h, 1,
skift, skift+h, Ctrl+z) gør ingenting.

## Forslag

* Tilføjelsen kan fejle i Mozilla-applikationer første gang efter
  tilføjelsesinstallation/opdatering; Genstart NVDA- og
  Mozilla-applikationerne for at løse det;
* I LibreOffice er den bedste konfiguration formentlig standard eller enkelt
  værktøjslinje, indstil dette i menuen Vis/værktøjslinjeposition.


[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=toolbarsExplorer

[2]: https://www.nvaccess.org/addonStore/legacy?file=toolbarsExplorer-dev
