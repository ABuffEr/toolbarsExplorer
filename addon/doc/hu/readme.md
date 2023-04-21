# Eszköztár Felfedező #

* Készítő: Alberto Buffolino
* [Stabil verzió][1] letöltése
* [Fejlesztői verzió][2] letöltése

Ez a kiegészítő megkönnyíti bizonyos programok eszköztárainak
elérését. Elemnavigáción alapul, csak leegyszerűsített parancsokkal.

## Billentyűparancsok

* Alt+menügomb: Az eszköztár felfedezésének elindítása<br/>
A parancsot bármikor megváltoztathatja az NVDA beviteli parancsok között az elemnavigáció kategóriában.

Az eszköztár felfedezése közben az alábbi parancsok használhatók:

* Balnyíl és jobbnyíl: az előző és a következő eszköztárra lép.
* Felnyíl és lenyíl: Lépked az aktuális eszköztár elemein.
* Enter: aktiválja az eszköztárat vagy annak egy elemét.
* Szóköz: Bal egérgomb lenyomásának emulálása az eszköztáron vagy annak egy
  elemén.
* menügomb vagy Shift+F10: jobb egérgomb lenyomásának emulálása az
  eszköztáron vagy annak egy elemén.
* Esc: kilép az eszköztár felfedezéséből

Ezen kívül az eszköztáron használhatja az NVDA által biztosított
elemnavigációs parancsokat is.

## Megjegyzések

Az eszköztár felfedezése az Esc gomb lenyomásával véget ér, de akkor is
ha...

* az eszköztáron műveletet hajt végre a szóköz a menügomb vagy az enter
  segítségével;
* olyan parancs használatakor, ami elveszi a fókuszt az eszköztárról
  például: Windows, Alt, Tab billentyű, NVDA+F1 parancs vagy az
  elemnavigációs parancsok, stb.

A Windows gombot, az Alt és az Esc billentyűket nem tartalmazó parancsok
hatására ilyenkor nem történik semmi. (pl.: Shift+H, Ctrl+Z).

## Javaslatok:

* Mozilla alkalmazásokban közvetlenül a telepítés vagy frissítés után
  előfordulhat, hogy nem működik megfelelően. Az NVDA és a kérdéses Mozilla
  alkalmazás újraindítása megoldja a problémát.
* Libre Office esetén az eszköztárat alapértelmezett vagy egyszerű nézetben
  lehet megfelelően használni a bővítménnyel. Az eszköztár nézetét a Libre
  Office alkalmazások Nézet menüjében lehet beállítani.


[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=tbx

[2]: https://www.nvaccess.org/addonStore/legacy?file=tbx-dev
