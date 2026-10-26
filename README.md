# Thực hành IoT – Buổi 3

## Thông tin sinh viên

- **Họ và tên:** Lê Thanh Thủy
- **Mã sinh viên:** B23DCCN809

## Cấu trúc thư mục

```text
TH_IOT_Buoi3/
├── Bai1/
│   ├── coap_server_bai1.py
│   └── coap_client_bai1.py
└── Readme.md
```

| Tệp | Chức năng |
| --- | --- |
| [Bai1/coap_server_bai1.py](Bai1/coap_server_bai1.py) | Khởi tạo CoAP server, xử lý GET/POST và lưu thông điệp mới nhất trong RAM. |
| [Bai1/coap_client_bai1.py](Bai1/coap_client_bai1.py) | Gửi yêu cầu đến server và cung cấp menu thử nghiệm. |
| [Readme.md](Readme.md) | Hướng dẫn cài đặt, chạy và kiểm tra chương trình. |

## Bài 1: Gửi và nhận thông điệp CoAP cơ bản

### Môi trường

- Python và pip, với phiên bản Python tương thích với thư viện `aiocoap` được cài đặt.
- Thư viện `aiocoap`; các mô-đun `asyncio` và `datetime` có sẵn trong Python.
- Server và client chạy trên cùng một máy, giao tiếp bằng CoAP qua UDP tại cổng `5683`.
- URI tài nguyên: `coap://localhost:5683/iot/lab/message`.

### Cài đặt và chạy

Thực hiện các lệnh dưới đây từ thư mục gốc `TH_IOT_Buoi3`.

**1. Cài đặt thư viện:**

```powershell
python -m pip install aiocoap
```

**2. Mở terminal thứ nhất và chạy server:**

```powershell
python Bai1/coap_server_bai1.py
```

Server hiển thị cổng và URI tài nguyên khi khởi động. Giữ terminal này chạy trong lúc sử dụng client.

**3. Mở terminal thứ hai và chạy client:**

```powershell
python Bai1/coap_client_bai1.py
```

Nhập mã sinh viên `B23DCCN809` và họ tên `Lê Thanh Thủy`. Nếu bỏ trống, chương trình dùng giá trị mặc định trong mã nguồn là `B23DCCN001` và `Nguyen Van A`.

Client tự gửi một yêu cầu GET, sau đó gửi POST với nội dung:

```text
Xin chao tu CoAP Client - B23DCCN809 - Lê Thanh Thủy
```

Sau hai yêu cầu ban đầu, client hiển thị menu:

| Lựa chọn | Chức năng |
| --- | --- |
| `1` | GET thông điệp hiện tại từ server. |
| `2` | Nhập nội dung và gửi thêm POST, kèm mã sinh viên và họ tên. |
| `3` | GET tài nguyên không tồn tại để kiểm tra phản hồi `4.04 Not Found`. |
| `0` | Thoát client. |

Nếu Windows không nhận lệnh `python` nhưng đã có Python Launcher, thay `python` bằng `py` trong các lệnh trên. Nhấn `Ctrl+C` để dừng server hoặc client.

### Hành vi và kết quả mong đợi

| Tình huống | Kết quả |
| --- | --- |
| GET khi server chưa nhận POST hợp lệ | Trả `2.05 Content`, payload `Xin chao tu CoAP Server`. |
| POST thông điệp hợp lệ | Server in nội dung và giờ nhận, lưu thông điệp rồi trả `2.04 Changed`, payload `Server da nhan thong diep`. |
| GET sau POST hợp lệ | Trả `2.05 Content` với nội dung POST hợp lệ mới nhất. |
| POST rỗng hoặc chỉ chứa khoảng trắng | Trả `4.00 Bad Request`, payload `Thong diep khong duoc de trong`. |
| POST chứa dữ liệu không giải mã được bằng UTF-8 | Trả `4.00 Bad Request`, payload `Payload phai duoc ma hoa UTF-8`. |
| Chọn menu `3` | Gửi GET đến `coap://localhost:5683/iot/lab/khong_ton_tai`, nhận `4.04 Not Found`. |
| Server không phản hồi | Client chờ tối đa 5 giây rồi báo timeout; lỗi giao tiếp có thể được báo sớm hơn tùy hệ điều hành và mạng. |

Server loại bỏ khoảng trắng ở hai đầu thông điệp trước khi kiểm tra và lưu. Dữ liệu chỉ được giữ trong RAM, nên khởi động lại server sẽ xóa thông điệp đã lưu.

Menu client luôn tạo nội dung POST kèm thông tin sinh viên; nếu bỏ trống phần lời chào ở lựa chọn `2`, client dùng `Xin chao tu CoAP Client`. Vì vậy, cần gửi yêu cầu riêng để kiểm tra POST rỗng hoặc dữ liệu UTF-8 không hợp lệ.

### Kiểm tra các chức năng mở rộng

1. Khởi động server và client để quan sát phản hồi GET/POST ban đầu.
2. Chọn `2` nhiều lần để gửi các thông điệp khác nhau; kiểm tra nội dung và thời gian nhận trong terminal server.
3. Chọn `1` để xác nhận server trả lại thông điệp POST mới nhất.
4. Chọn `3` để kiểm tra tài nguyên không tồn tại.
5. Dừng server, sau đó chọn `1` hoặc `2` trên client để kiểm tra xử lý timeout hoặc lỗi giao tiếp.
6. Khởi động lại server, chọn `1` trên client để kiểm tra thông điệp trở về lời chào ban đầu.
