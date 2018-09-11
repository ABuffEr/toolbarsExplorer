# ToolbarsExplorer #

* Author: Alberto Buffolino
* Download [development version][2]

This add-on makes easier to use toolbars in applications, providing an exploration model derived by object navigation, with simplified gestures.

## Commands

* Alt+applications: starts toolbars exploration<br/>
(you can remap it via NVDA gesture manager, under Object navigation).

During exploration, following gestures are available:

* Left/right arrow: moves to previous/next toolbar;
* Up/down arrow: scrolls up/down items in current toolbar;
* Enter: activates toolbar or its item;
* Space: simulates left mouse click on toolbar or its item;
* Applications/shift+F10: simulates right mouse click on toolbar or its item;
* Escape: exits from exploration.

Additionally, you can perform actions on toolbars or its items using any gesture provided by NVDA, as exactly as when you move to objects with standard object navigation.

## Notes and suggestions

* Exploration terminates implicitly performing an action on toolbar or its item, or pressing a non-mapped gesture (exceptions below), and explicitly pressing escape;
* Character (h, 1, shift+h, etc) or modifier-only (shift, control) gestures are ignored and don't disable the exploration;
* The add-on may fail in Mozilla applications the first time after add-on installation/update; please restart NVDA and Mozilla applications to resolve;
* In LibreOffice, best configuration is probably default or single toolbar, set it on view menu/toolbar position.


[2]: https://addons.nvda-project.org/files/get.php?file=tbx
