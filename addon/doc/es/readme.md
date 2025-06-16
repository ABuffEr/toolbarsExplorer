# ToolbarsExplorer #

* Autor: Alberto Buffolino
* Descargar [versión estable][1]
* Descargar [versión de desarrollo][2]

Este complemento facilita el uso de barras de herramientas en las
aplicaciones, proporcionando un modelo de exploración derivado de la
navegación de objetos, con gestos simplificados.

## Atajos

* Alt+aplicaciones: Iniciar exploración de barras de herramientas<br>
(puedes reasignarlo mediante el Administrador de Gestos de NVDA; bajo Navegación de objetos).

Durante la exploración, están disponibles los siguientes gestos:

* Flecha izquierda/derecha: se mueve a la anterior/siguiente barra de
  herramientas;
* Flecha arriba/abajo: se desplaza arriba/abajo por los elementos de la
  barra de herramientas actual;
* Enter: activa la barra de herramientas o su elemento;
* Espacio: simula un click izquierdo del ratón en la barra de herramientas o
  su elemento;
* Aplicaciones / shift+f10: simula un click derecho del ratón en la barra de
  herramientas o su elemento;
* Escape: salir de la exploración.

Además, puedes realizar acciones en barras de herramientas o sus elementos
utilizando cualquier gesto proporcionado por NVDA, exactamente como al
moverse a objetos con la navegación de objetos estándar.

## Notas

La exploración termina de forma explícita al presionar escape, e
implíccitamente:

* realizando una acción en una barra de herramientas o en su elemento (con
  espacio, aplicaciones / shift+f10, pulsar intro);
* pulsando un gesto que te lleve fuera de los objetos de una barra de
  herramientas (alt, Windows, tabulador, NVDA+f1, gestos de navegación por
  objetos, etc).

Otros gestos que no contengan alt, Windows o escape (como h, 1, shift,
shift+h, ctrl+z) simplemente no hacen nada.

## Sugerencias

* La primera vez después de la instalación / actualización del complemento,
  este puede fallar en las aplicaciones de Mozilla; por favor, reinicia
  tanto NVDA como las aplicaciones de Mozilla para resolver este fallo;
* En LibreOffice, la mejor configuración es probablemente la barra de
  herramientas por defecto o una sola, establécelo en el menú ver/posición
  de barra de herramientas.


[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=toolbarsExplorer

[2]: https://www.nvaccess.org/addonStore/legacy?file=toolbarsExplorer-dev
