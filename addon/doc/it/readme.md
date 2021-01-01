# ToolbarsExplorer #

* Autore: Alberto Buffolino
* Scarica la [versione stabile][1]
* Scarica la [versione in sviluppo][2]

Questo componente aggiuntivo rende più semplice l'utilizzo delle barre degli
strumenti nelle applicazioni, fornendo un modello di esplorazione derivato
dalla navigazione ad oggetti, con comandi semplificati.

## Comandi

* Alt+tasto applicazioni: entra in modalità esplorazione barre strumenti<br/>
(è possibile rimappare la combinazione attraverso la gestione gesti e tasti d'immissione di NVDA, categoria Navigazione oggetti).

Durante la modalità esplorazione barre strumenti, sono attivi i seguenti
tasti:

* Freccia sinistra/destra: si sposta alla barra strumenti
  precedente/successiva;
* Freccia su/giù: scorre su/giù gli elementi nella barra strumenti attuale;
* Invio: attiva la barra strumenti o un suo elemento;
* Barra spaziatrice: simula il click del tasto sinistro del mouse sulla
  barra strumenti o su un suo elemento;
* Tasto applicazioni/shift+F10: simula il click del tasto destro del mouse
  sulla barra strumenti o su un suo elemento;
* Esc: esce dalla modalità esplorazione barra strumenti.

In aggiunta, è possibile eseguire azioni sulle barre strumenti o sui loro
elementi utilizzando un qualsiasi comando fornito da NVDA, esattamente come
quando ci si muove sugli oggetti con la navigazione oggetti standard.

## Note

La modalità esplorazione termina esplicitamente premendo esc, e
implicitamente:

* eseguendo un'azione sulla barra strumenti o su un suo elemento (con barra
  spaziatrice, tasto applicazioni/shift+F10, invio);
* eseguendo un comando che si sposta al di fuori degli oggetti della barra
  strumenti attuale (alt, windows, tab, NVDA+F1, comandi di navigazione
  oggetti, etc).

Altri comandi non contenenti alt, windows o esc (come h, 1, shift, shift+h,
control+z) semplicemente non producono alcun effetto.

## Suggerimenti

* Il componente aggiuntivo potrebbe inizialmente non funzionare nelle
  applicazioni Mozilla dopo l'installazione/aggiornamento del componente
  stesso; per favore, riavviare NVDA e le applicazioni Mozilla per
  risolvere;
* In LibreOffice, la miglior configurazione è probabilmente quella di
  default o a barra strumenti singola, da impostare nel menu
  visualizza/interfaccia utente.


[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=tbx

[2]: https://addons.nvda-project.org/files/get.php?file=tbx-dev
