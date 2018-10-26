# ToolbarsExplorer #

* Autor: Alberto Buffolino
* Pobierz [wersja stabilna][1]
* Pobierz [wersja rozwojowa][2]

Ten dodatek ułatwia używanie pasków narzędzi w aplikacjach. W tym celu,
wykorzystuje sposób eksploracji pochodzący z nawigacji obiektowej z
uproszczonymi gestami.

## Polecenia

* Alt+klawisz kontekstowy: włącza eksplorację pasków narzędzi<br/>
(Można przemapować to w oknie zdarzeń wejścia, w kategorii nawigacja obiektowa).

Podczas eksploracji dostępne są następujące polecenia:

* Strzałka w lewo/w prawo: przemieszcza do poprzedniego/następnego paska
  narzędzi;
* Strzałka w górę/w dół: przewija w górę/w dół elementy aktualnego paska
  narzędzi;
* Enter: aktywuje pasek narzędzi lub jego element;
* Spacja: symuluje kliknięcie lewym przyciskiem myszy na pasku narzędzi lub
  jego elemencie;
* Klawisz kontekstowy/sift+F10: symuluje kliknięcie prawym przyciskiem myszy
  na pasku narzędzi lub jego elemencie;
* Escape: zamyka eksplorację.

Dodatkowo, można wykonywać czynności na paskach narzędzi lub ich elementach
za pomocą wszystkich gestów NVDA, dokładnie tak, jak podczas poruszania się
po obiektach przy użyciu standardowej nawigacji obiektowej.

## Uwagi

Eksplorację jawnie kończy naciśnięcie klawisza Escape, a także niejawnie.

* wykonywanie akcji na elemencie paska narzędzi oraz na samym pasku za
  pomocą spacji klawisza kontekstowego/shift+F10, oraz klawiszem enter);
* naciśmnięcie gestu wyprowadzającego z aktualnego paska narzędzi (alt,
  windows, tab, NVDA+F1, nawigacja objektowa itd).

Inne gesty włączając w to klawisze (takie jak h, 1, shift, shift+h,
control+z) po prostu nie robią nic.

## sugestie

* Dodatek może nie działać po pierwsze instalacji/aktualizacji aplikacji
  Mozilli; Aby rozwiązać problem, prosimy zrastartować NVDA i aplikacje
  Mozilla;
* W LibreOffice, prawdopodobnie najlepiej ustawić  domyślny lub pojedynczy
  pasek narzędzi. Można to zrobić w menu widok/pozycja paska narzędzi.


[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=tbx

[2]: https://addons.nvda-project.org/files/get.php?file=tbx-dev
