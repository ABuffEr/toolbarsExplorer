# ToolbarsExplorer #

* Tác giả: Alberto Buffolino
* Tải về [phiên bản chính thức][1]
* Tải về [phiên bản thử nghiệm][2]

Add-on này giúp việc sử dụng các thanh công cụ trong các ứng dụng trở nên dễ
dàng hơn, cung cấp phương thức khám phá dựa trên điều hướng đối tượng với
các thao tác đơn giản.

## Lệnh

* Alt+applications: bắt đầu khám phá các thanh công cụ<br/>
(bạn có thể gán lại trong Quản lý cử chỉ của NVDA, trong phần Duyệt các đối tượng

Trong khi khám phá, có các thao tác sau:

* Mũi tên trái / phải: di chuyển đến thanh công cụ trước / kế;
* Mũi tên lên / xuống: cuộn lên / xuống ở thanh công cụ hiện tại;
* Enter: kích hoạt thanh công cụ hay thành phần của nó;
* Khoảng trắng: tương tự bấm chuột trái trên thanh công cụ hay thành phần
  của nó;
* Applications/shift+F10: tương tự bấm chuột phải trên thanh công cụ hay
  thành phần của nó;
* Escape: thoát khỏi chế độ khám phá.

Thêm nữa, bạn có thể thực hiện các thao tác trên thanh công cụ hay các thành
phần của nó bằng bất cứ thao tác nào của NVDA, giống như khi bạn di chuyển
đến các đối tượng vớu các lệnh điều hướng chuẩn.

## Lưu ý

Chế độ khám phá sẽ ngầm bị tắt ngay khi bấm escape:

* thực hiện một hoạt động trên thanh công cụ hay thành phần của nó (với
  khoảng trắng, applications/shift+F10, enter);
* thực hiện một thao tác chuyển ra khỏi các đối tượng của thanh công cụ hiện
  tại (alt, windows, tab, NVDA+F1, các thao tác duyệt đối tượng, v...v...).

Các thao tác khác không có phím alt, windows hay escape (như là h, 1, shift,
shift+h, control+z) thì đơn giản không làm gì cả.

## Các đề xuất

* Add-on có thể gặp lỗi trong các ứng dụng của Mozilla ở lần đầu sau khi cài
  đặt / cập nhật add-on; vui lòng khởi động lại NVDA và các ứng dụng của
  Mozillađể khắc phục;
* Trong LibreOffice, cấu hình tốt nhất là default hay single toolbar, chỉnh
  trong trình đơn view/toolbar position.


[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=tbx

[2]: https://www.nvaccess.org/addonStore/legacy?file=tbx-dev
