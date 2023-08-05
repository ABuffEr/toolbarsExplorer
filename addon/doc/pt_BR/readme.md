# Explorador de Barras de Ferramentas (ToolbarsExplorer) #

* Autor: Alberto Buffolino
* Baixe a [versão estável][1]
* Baixe a [versão em desenvolvimento][2]

Esse complemento facilita o uso das barras de ferramentas em aplicativos,
fornecendo um modelo de exploração derivado da navegação de objetos, com
comandos (gestos) simplificados.

## Comandos

* Alt+aplicações: inicia a exploração das barras de ferramentas<br/>
(pode remapear através do gerenciador de comandos do NVDA, em Navegação por objetos).

Durante a exploração, estão disponíveis os seguintes comandos:

* Seta esquerda/direita: move para a barra de ferramentas anterior/seguinte;
* Seta para cima/baixo: rola os itens para cima/baixo na barra de
  ferramentas atual;
* Enter: ativa a barra de ferramentas ou um de seus itens;
* Espaço: simula o clique esquerdo do mouse na barra de ferramentas ou em um
  de seus itens;
* Aplicações/shift+F10: simula o clique direito do mouse na barra de
  ferramentas ou em um de seus itens;
* Escape: sai da exploração.

Além disso, pode executar ações nas barras de ferramentas ou nos seus itens
usando qualquer comando (gesto) fornecido pelo NVDA, exatamente como quando
se move para objetos, na navegação de objetos padrão.

## Notas

A exploração é finalizada explicitamente pressionando escape e
implicitamente:

* executar uma ação na barra de ferramentas ou em seu item (com espaço,
  aplicações/shift+F10, enter);
* pressionando um comando (gesto) que sai dos objetos atuais da barra de
  ferramentas (alt, windows, tab, NVDA+F1, comandos de navegação por
  objetos, etc.).

Outros comandos (gestos) que não contêm alt, windows ou escape (como h, 1,
shift, shift+h, control+z) simplesmente não fazem nada.

## Sugestões

* O complemento pode falhar nos aplicativos da Mozilla na primeira vez após
  a instalação/atualização; por favor reinicie o NVDA e os aplicativos
  Mozilla para resolver;
* No LibreOffice, a melhor configuração é provavelmente a barra de
  ferramentas padrão ou única, configure-a no menu de visualização/posição
  da barra de ferramentas.


[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=tbx

[2]: https://www.nvaccess.org/addonStore/legacy?file=tbx-dev
