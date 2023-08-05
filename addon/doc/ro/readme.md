# ToolbarsExplorer #

* Author: Alberto Buffolino
* Descărcați [versiunea stabilă][1]
* Descărcați [versiunea în dezvoltare][2]

Acest supliment face mai ușoară utilizarea barelor de unelte din aplicații,
oferind un model de explorare derivat din navigarea obiectului cu gesturi
simplificate.

## Comenzi

* Alt+applications: pornește explorarea barelor de unelte<br/>
(Puteți să o modificați din administratorul de gesturi NVDA, aflat sub obiectul de navigare).

Pe durata explorării, sunt disponibile următoarele gesturi:

* Săgețile stânga și dreapta: deplasează cursorul la bara de unelte
  următoare sau la cea precedentă;
* Săgețile sus și jos: deplasează cursorul la elementele din bara de unelte
  curentă;
* Enter: activează bara de unelte sau elementul său;
* Spațiu: simulează click stânga pe bara de unelte sau pe elementul său;
* Aplicații/shift+F10: simulează click dreapta pe bara de unelte sau pe
  elementul său;
* Escape: iese din explorare.

În plus, puteți efectua acțiuni pe barele de unelte sau pe elementele lor
folosind orice gest oferit de NVDA, ca și cum v-ați deplasa la obiecte cu
navigarea standard a obiectului.

## Note

Explicit, explorarea se termină la apăsarea tastei Escape, iar implicit:

* efectuarea unei acțiuni pe bara de unelte sau pe elementul acesteia (cu
  spațiu, aplicații/shift+F10, enter);
* apăsarea unui gest care deplasează cursorul în afara obiectelor barei
  curente (alt, windows, tab, NVDA+F1, gesturi de navigare ale obiectelor
  etc).

Alte gesturi care nu conțin alt, windows sau escape (ca h, 1, shift,
shift+h, control+z) pur și simplu nu fac nimic.

## Sugestii

* Suplimentul poate eșua în aplicațiile Mozilla prima dată după
  instalarea/actualizarea suplimentului; vă rugăm să reporniți NVDA și
  aplicațiile Mozilla pentru a rezolva această problemă;
* În LibreOffice, cea mai bună configurație este probabil cea implicită sau
  bara singulară de unelte, setați-o din meniul vizualizare/poziția barei de
  unelte.


[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=tbx

[2]: https://www.nvaccess.org/addonStore/legacy?file=tbx-dev
