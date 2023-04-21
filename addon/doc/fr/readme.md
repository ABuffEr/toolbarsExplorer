# ToolbarsExplorer #

* Auteur : Alberto Buffolino
* Télécharger [version stable][1]
* Télécharger [version de développement][2]

Cette extension facilite l'utilisation des barres d'outils dans les
applications, fournissant un modèle d'exploration dérivé de la navigation
par objet, avec des gestes simplifiés.

## Touches de commandes

* Alt+applications : début de l'exploration des barres d'outils<br/>
(vous pouvez le réaffecter via le dialogue Gestes de commandes de NVDA, sous Navigation par objet).

Lors de l'exploration, les gestes suivants sont disponibles :

* Flèche gauche / droite : aller à la barre d'outils précédente / suivante ;
* Flèche haut / bas : fait défiler les éléments haut / bas dans la barre
  d'outils actuelle ;
* Entrée : active la barre d'outils ou son élément ;
* Espace : simule un clic gauche sur la barre d'outils ou son élément ;
* Applications / maj+F10 : simule un clic droit sur la barre d'outils ou son
  élément ;
* Échap : sort de l'exploration.

De plus, vous pouvez effectuer des actions sur les barres d'outils ou ses
éléments en utilisant n'importe quel geste fourni par NVDA, exactement comme
lorsque vous accéder à des objets avec la navigation par objet standard.

## Notes

L'exploration se termine explicitement en appuyant sur Échap et
implicitement:

* en exécutant une action sur la barre d'outils ou son élément (avec espace,
  applications / maj+F10, entrée) ;
* en appuyant sur le geste qui sort des objets de la barre d'outils actuelle
  (alt, windows, tab, NVDA+F1, gestes de navigation par objet, etc.).

D'autres gestes ne contenant pas alt, windows ou échap (comme h, 1, maj,
maj+h, contrôle+z) simplement ne fait rien.

## Suggestions

* L'extension peut échouer dans les applications Mozilla la première fois
  après l'installation / mise à jour de l'extension; Veuillez redémarrer les
  applications NVDA et Mozilla pour résoudre ;
* Dans LibreOffice, la meilleure configuration est probablement la barre
  d'outils par défaut ou unique, définissez-la dans le menu Affichage /
  Position des barre d'outils.


[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=tbx

[2]: https://www.nvaccess.org/addonStore/legacy?file=tbx-dev
