# Araç çubuğu gezgini #

* Yazar: Alberto Buffolino
* [Kararlı sürümü][1] indir
* [geliştirme sürümünü][2] indir

Bu eklenti, basitleştirilmiş hareketlerle nesne navigasyonundan türetilen
bir keşif modeli sağlayarak uygulamalarda araç çubuklarının kullanımını
kolaylaştırır.

## Komutlar

* Alt+uygulama tuşu: araç çubuklarının keşfini başlatır<br/>
(NVDA girdi hareketleri iletişim kutusunda Nesne dolaşımı altından yeniden atayabilirsiniz.).

Keşif sırasında aşağıdaki hareketler kullanılabilir:

* Sol/sağ ok: önceki/sonraki araç çubuğuna gider;
* Yukarı/aşağı ok: mevcut araç çubuğundaki öğeler arasında yukarı/aşağı
  gider;
* Enter: araç çubuğunu veya öğesini etkinleştirir;
* Boşluk: araç çubuğuna veya öğesine sol fare tıklamasını simüle eder;
* Uygulama tuşu/shift+F10: Araç çubuğuna veya öğesine sağ tıklamayı simüle
  eder;
* Esc tuşu: keşiften çıkar.

Ek olarak, tıpkı standart nesne navigasyonu ile nesnelere hareket
ettiğinizde olduğu gibi, NVDA tarafından sağlanan herhangi bir hareketi
kullanarak araç çubukları veya öğeleri üzerinde eylemler
gerçekleştirebilirsiniz.

## Notlar

Keşif, esc tuşuna basılarak doğrudan sonlandırılır ve dolaylı olarak:

* araç çubuğunda veya öğesinde bir eylem gerçekleştirme (boşluk,
  uygulamalar/shift+F10, enter ile);
* mevcut araç çubuğu nesnelerinden ayrılmaya neden olan bir harekete basarak
  (alt, windows, tab, NVDA+F1, nesne dolaşım hareketleri vb.).

Alt, windows veya escape içermeyen diğer hareketler (h, 1, shift, shift+h,
control+z gibi) hiçbir şey yapmaz.

## Öneriler

* Eklenti yüklemesi/güncellemesinden sonra ilk kez kullanıldığında Mozilla
  uygulamalarında eklenti başarısız olabilir; çözmek için lütfen NVDA ve
  Mozilla uygulamalarını yeniden başlatın;
* LibreOffice'de, en iyi yapılandırma muhtemelen varsayılan veya tek araç
  çubuğudur, bunu görünüm menüsü/araç çubuğu konumlarında ayarlayın.


[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=toolbarsExplorer

[2]: https://www.nvaccess.org/addonStore/legacy?file=toolbarsExplorer-dev
