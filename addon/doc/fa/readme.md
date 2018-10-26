# مرورگر نوارهای ابزار (ToolbarsExplorer) #

* نویسنده: Alberto Buffolino
* Download [stable version][1]
* دانلود [نسخه‌ی در دست توسعه][2]

این افزونه، استفاده از نوارهای ابزار در برنامه‌ها را، با فراهم آوردن مدلی از
گشت زدن که از پیمایش اشیا برگرفته شده و فرمان‌های ساده‌شده، آسانتر میسازد.

## فرمان‌ها

* Alt+applications: گشت زدن در نوارهای ابزار را آغاز میکند.<br/>
(میتوانید این کلید را از مدیریت فرمان‌های ورودی، شاخه‌ی پیمایش اشیا، تغییر دهید.).

در خلال گشت‌زنی، فرمان‌های زیر موجود اند:

* جهت‌نمای چپ یا راست: برای رفتن به نوار ابزار قبلی یا بعدی؛
* جهت‌نمای بالا یا پایین: مرور گزینه‌های موجود در نوار ابزار جاری؛
* اینتر: نوار ابزار یا گزینه‌ای از آن‌را فعال میکند؛
* فاصله: چپ‌کلیک موس را روی نوار ابزار یا گزینه‌ای از آن شبیه‌سازی میکند؛
* Applications/shift+F10: simulates right mouse click on toolbar or its
  item;
* Escape: از گشت‌زنی خارج میشود.

افزون بر این، میتوانید با استفاده از فرمان‌های NVDA روی نوارهای ابزار و
گزینه‌هایشان عملیات مربوط را انجام دهید؛ دقیقا مثل وقتی که با استفاده از
فرمان‌های استاندارد پیمایش اشیا، روی اشیا حرکت میکنید.

## Notes

Exploration is terminated explicitly pressing escape, and implicitly:

* performing an action on toolbar or its item (with space,
  applications/shift+F10, enter);
* pressing a gesture that moves out of current toolbar objects (alt,
  windows, tab, NVDA+F1, object navigation gestures, etc).

Other gestures not containing alt or windows (as h, 1, shift, shift+h,
control+z) simply does nothing.

## Suggestions

* The add-on may fail in Mozilla applications the first time after add-on
  installation/update; please restart NVDA and Mozilla applications to
  resolve;
* در برنامه‌ی LibreOffice، بهترین تنظیم، احتمالا تنظیم پیش‌فرض یا نوار ابزار
  تکی است. میتوانید از گزینه‌ی Toolbar Position در منوی View، این تنظیم را
  انجام دهید.


[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=tbx

[2]: https://addons.nvda-project.org/files/get.php?file=tbx-dev
