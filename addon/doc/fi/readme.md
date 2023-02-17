# Työkalupalkkien selain #

* Tekijä: Alberto Buffolino
* Lataa [vakaa versio][1]
* Lataa [kehitysversio][2]

Tämä lisäosa helpottaa sovellusten työkalupalkkien käyttöä tarjoten
objektinavigoinnista lähtöisin olevan selausmallin yksinkertaistetuilla
näppäinkomennoilla.

## Komennot

* Alt+Sovellusnäppäin: aloittaa työkalupalkkien selauksen<br/>
(näppäinkomennon uudelleenmäärittäminen on mahdollista NVDA:n Näppäinkomennot-valintaikkunan Objektinavigointi-kategoriasta).

Seuraavat näppäinkomennot ovat käytettävissä:

* Nuoli vasemmalle/oikealle: siirtää edelliseen/seuraavaan työkalupalkkiin;
* Nuoli ylös/alas: vierittää nykyisen työkalupalkin kohteita ylös/alas;
* Enter: aktivoi työkalupalkin tai sen kohteen;
* Väli-näppäin: simuloi vasenta hiiripainikkeen napsautusta työkalupalkissa
  tai sen kohteessa;
* Sovellusnäppäin/Vaihto+F10: simuloi oikean hiiripainikkeen napsautusta
  työkalupalkissa tai sen kohteessa;
* Esc: poistuu työkalupalkkien selaustilasta.

Työkalupalkeille tai niiden kohteille on lisäksi mahdollista suorittaa
toimintoja millä tahansa NVDA:n tarjoamilla näppäinkomennoilla, aivan kuten
siirryttäessä objekteihin objektinavigointia käyttäen.

## Huomautuksia

Työkalupalkkien selaustilasta poistutaan painamalla Esc-näppäintä,
suoritettaessa toimintoa työkalupalkille tai sen kohteelle sekä:

* suorittamalla toiminnon työkalupalkille tai sen kohteelle (Väli- tai
  sovellusnäppäimellä/Vaihto+F10-näppäinyhdistelmällä tai Enterillä);
* käyttämällä työkalupalkeista pois siirtävää komentoa (Alt-, Windows- tai
  Sarkain-näppäimen ja NVDA+F1-yhdistelmän painaminen,
  objektinavigointikomennot jne.).

Muut komennot, joihin ei sisälly Alt-, Windows- tai Esc-näppäintä (kuten H,
1, Vaihto, Vaihto+H, Ctrl+Z) eivät tee mitään.

## Ehdotuksia

* Lisäosa ei välttämättä toimi asentamisen/päivittämisen jälkeen
  Mozilla-sovelluksissa. Ongelma ratkeaa käynnistämällä NVDA ja
  Mozilla-sovellukset uudelleen;
* LibreOfficessa paras työkalupalkkien asetus on Oletus tai Yksi
  työkalurivi. Se määritetään Näytä-valikon kohdasta Työkalupalkin asettelu.


[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=tbx

[2]: https://addons.nvda-project.org/files/get.php?file=tbx-dev
