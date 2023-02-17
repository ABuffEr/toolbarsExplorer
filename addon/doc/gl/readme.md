# ToolbarsExplorer #

* Autor: Alberto Buffolino
* Descargar [versión estable][1]
* Descargar [versión de desenvolvemento][2]

Este complemento facilita utilizar barras de ferramentas nas aplicacións,
proporcionando un modelo de exploración derivado da navegación de obxectos,
con xestos simplificados.

## Atallos

* Alt+aplicacións: iniciar exploración de barras de ferramentas<br>
(podes reasignalo mediante o administrador de xestos do NVDA; baixo Navegación de obxectos).

Durante a exploración, están dispoñibles os seguintes xestos:

* Frecha esquerda/dereita: móvese á anterior/seguinte barra de ferramentas;
* Frecha arriba/abaixo: desprázase cara arriba/abaixo polos elementos da
  barra de ferramentas actual;
* Enter: activa a barar de ferramentas ou o seu elemento;
* Espazo: simula un click esquerdo do rato na barra de ferramentas ou o seu
  elemento;
* Aplicacións/shift+f10: simula un click dereito do rato na barra de
  ferramentas ou o seu elemento;
* Escape: sae da exploración.

Ademais, podes realizar accións en barras de ferramentas ou os seus
elementos usando calquera xesto proporcionado polo NVDA, exactamente como ao
moverte a obxectos coa navegación de obxectos estándar.

## Notas

A exploración remata de maneira explícita premendo escape, e implícita:

* Realizando unha acción sobre a barra de ferramentas ou o seu elemento (con
  espazo, aplicacións / shift+f10, enter);
* premendo un xesto que se mova fóra do obxecto actual da barra de
  ferramentas (alt, Windows, tab, NVDA+F1, xestos de navegación por
  obxectos, etc.).

Outros xestos que non conteñan alt, Windows ou escape (como h, 1, shift,
shift+h, control+z) simplemente non fan nada.

## Suxestións

* O complemento pode fallar nas aplicacións de Mozilla a primeira vez trala
  instalación/actualización do complemento; por favor reinicia NVDA e as
  aplicacións de Mozilla para resolvelo;
* No LibreOffice, a mellor configuración é probablemente a barra de
  ferramentas predeterminada ou unha soa, establéceo no menú ver/posición de
  barra de ferramentas.


[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=tbx

[2]: https://addons.nvda-project.org/files/get.php?file=tbx-dev
