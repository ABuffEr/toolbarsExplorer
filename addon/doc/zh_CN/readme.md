# ToolbarsExplorer工具栏快速导航插件 #

* 作者: Alberto Buffolino
* 下载[稳定版][1]
* 下载 [开发板][2]

此插件可以使应用程序中的工具栏更易于使用，提供了由对象导航派生的探索模型，并具有简化的手势。

## 快捷键

* Alt+applications: 启动工具栏探索（您可以通过NVDA手势管理器在对象导航下重新设置此快捷手饰

在探索期间，可以使用以下手势：

* Left/right arrow: 移动到上一个/下一个工具栏;
* Up/down arrow: 在当前工具栏中向上/向下滚动项目;
* Enter: 激活工具栏或其项目;
* Space: 模拟鼠标左键单击工具栏或其项目;
* Applications/shift+F10: 模拟鼠标右键单击工具栏或其项目;
* Escape: 退出探索。

此外，您可以使用NVDA提供的任何手势对工具栏或其项目执行操作，就像移动到具有标准对象导航的对象一样。

## 注意

探索终止显式按下escape，并在工具栏或其项目上隐式执行操作：

* 在工具栏或其项目上执行操作（请使用 space, applications/shift+F10, enter)快捷键;
* 按下移出当前工具栏对象的手势可用以下快捷键 (alt, windows, tab, NVDA+F1, 对象导航手势等）。

其他不包含alt，windows或转义的手势（如h，1，shift，shift + h，control + z）按下以上首饰后将无效。

## 使用建议

* 插件安装/更新后，插件可能在Mozilla浏览器中首次使用无效;请重启NVDA和Mozilla浏览器来解决此问题;
* 在LibreOffice中，最佳配置可能是默认或单个工具栏，将其设置在视图菜单/工具栏位置。


[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=tbx

[2]: https://www.nvaccess.org/addonStore/legacy?file=tbx-dev
