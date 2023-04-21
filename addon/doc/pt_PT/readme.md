# exploradorBarrasFerramentas #

* Autor: Alberto Buffolino
* Baixar [versão estável][1]
* Baixar [versão de desenvolvimento][2]

Este extra facilita o uso das barras de ferramentas em aplicações em que
elas existam, fornecendo um modelo de exploração derivado da navegação de
objectos, com comandos simplificados.

## Comandos:

* Alt+tecla de aplicações: Inicia a exploração das barras de ferramentas<br/>
(Pode redefinir através do menu de entrada de comandos, navegação por objectos).

Durante a exploração, estão disponíveis os seguintes comandos:

* Seta esquerda/direita: move entre barra de ferramentas anterior/seguinte
* Seta para cima/baixo: desloca para cima/para baixo na barra de ferramentas
  actual;
* Enter: activa a barra de ferramentas ou um de seus itens;
* Espaço: simula o clique esquerdo do rato na barra de ferramentas ou em um
  de seus itens;
* Tecla de aplicações/sift+f10: simula o clique direito do rato na barra de
  ferramentas ou em um de seus itens;
* Escape: sai da exploração.

Além disso, pode executar acções nas barras de ferramentas ou nos seus itens
usando qualquer comando fornecido pelo NVDA, exactamente como quando se move
para objectos, na navegação de objectos padrão.

## Notas

A exploração termina, explicitamente, ao pressionar a tecla  escape ou ao
executar implicitamente uma acção na barra de ferramentas ou em qualquer de
seus itens;

* executa uma acção na barra de ferramentas ou seu item (com espaço,
  aplicativos / shift + F10, enter);
* Pressionar um comando que sai da barra de ferramentas actual (alt, tecla
  windows, tab, NVDA+F1, comandos de navegação por objectos, etc).

outros comandos que não contenham alt ou a tecla windows ou escape (como h,
1, shift, shift+h, control+z) não fazem nada.

## Sugestões:

* O extra pode falhar nas aplicações da Mozilla na primeira vez após a
  instalação / actualização; por favor reinicie o NVDA e o Mozilla para
  resolver;
* No LibreOffice, a melhor configuração é provavelmente a barra de
  ferramentas padrão ou única, configurada no menu de visualização / posição
  da barra de ferramentas.


[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=tbx

[2]: https://www.nvaccess.org/addonStore/legacy?file=tbx-dev
