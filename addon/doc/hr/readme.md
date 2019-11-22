# Istraživanje alatnih traka (ToolbarsExplorer) #

* Author: Alberto Buffolino
* Preuzmi [stabilnu verziju][1]
* Preuzmi [razvojnu verziju][2]

Ovaj dodatak olakšava upotrebu alatnih traka u aplikacijama, pružajući model
istraživanja (izveden iz objektne navigacije) s pojednostavljenim gestama.

## Naredbe

* Alt+aplikacije: pokreće istraživanje alatnih traka<br/>
(prečac je moguće promijeniti putem NVDA upravljača gesta, pod Objektna navigacija).

TIjekom istraživanja su dostupne sljedeće geste:

* Strelica lijevo/desno: premješta se na prethodnu/sljedeću alatnu traku;
* Strelica gore/dolje: kliže gore/dolje po stavkama u trenutačnoj alatnoj
  traci;
* Enter: aktivira alatnu traku ili njenu stavku;
* Razmaknica: simulira klik lijevom tipkom miša na alatnu traku ili njenu
  stavku;
* Aplikacije/shift+F10: simulira klik lijevom tipkom miša na alatnu traku
  ili njenu stavku;
* Escape: izlazi iz istraživanja.

Dodatno tome je moguće izvršavati radnje na alatnim trakama ili njenim
stavkama pomoću bilo koje geste koju pruža NVDA, točno onako, kako se
korisnik kreće po objektima sa standardnom navigacijom po objekatima.

## Napomene

Istraživanje se prekida direktnim pritiskom tipke escape, a inače:

* izvršavanjem radnje na alatnoj traci ili njenoj stavci (s razmaknicom,
  aplikacije/shift+F10, enter);
* pritiskom geste, kojom se premješta izvan trenutačnih objekata alatne
  trake (alt, windows, tabulator, NVDA+F1, geste za navigaciju po objektima
  itd.).

Druge geste koje ne sadrže tipke alt, windows ili escape (kao h, 1, shift,
shift+h, control+z) jednostavno ne rade ništa.

## Prijedlozi

* Dodatak možda neće raditi u Mozilla aplikacijama prilikom prvog pokretanja
  dodatka nakon instaliranja/ažuriranja. Ponovo pokreni NVDA i Mozilla
  aplikacije, kako bi se problem riješio;
* U LibreOfficeu je vjerojatno najbolje koristiti standardnu konfiguraciju
  ili pojedinačnu alatnu traku. Postavi je u izbornik prikaza/na položaj
  alatne trake.


[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=tbx

[2]: https://addons.nvda-project.org/files/get.php?file=tbx-dev
