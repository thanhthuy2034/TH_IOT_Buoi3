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
├── Bai2/
│   ├── sensor_server_bai2.py
│   └── monitor_client_bai2.py
└── README.md
```

| Tệp | Chức năng |
| --- | --- |
| [Bai1/coap_server_bai1.py](Bai1/coap_server_bai1.py) | Khởi tạo CoAP server, xử lý GET/POST và lưu thông điệp mới nhất trong RAM. |
| [Bai1/coap_client_bai1.py](Bai1/coap_client_bai1.py) | Gửi yêu cầu đến server và cung cấp menu thử nghiệm. |
| [Bai2/sensor_server_bai2.py](Bai2/sensor_server_bai2.py) | Mô phỏng ba cảm biến nhiệt độ/độ ẩm, cập nhật dữ liệu mỗi 3 giây và trả JSON qua GET. |
| [Bai2/monitor_client_bai2.py](Bai2/monitor_client_bai2.py) | GET định kỳ mỗi 3 giây, hiển thị dữ liệu, cảnh báo và thống kê thời gian phản hồi. |
| [README.md](README.md) | Hướng dẫn cài đặt, chạy và kiểm tra chương trình. |

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

## Bài 2: Mô phỏng cảm biến nhiệt độ và độ ẩm bằng CoAP

### Môi trường

- Python `3.14.7`, thư viện `aiocoap` (cài như Bài 1); các mô-đun `asyncio`, `json`, `random`, `time`, `datetime` có sẵn trong Python.
- Server lắng nghe CoAP qua UDP tại `127.0.0.1:5683`. Client mặc định gửi tới `127.0.0.1`.
- Khi chạy trên hai máy, đổi `HOST` trong [Bai2/sensor_server_bai2.py](Bai2/sensor_server_bai2.py) và `SERVER_HOST` trong [Bai2/monitor_client_bai2.py](Bai2/monitor_client_bai2.py) thành IP của máy chạy server, và mở UDP cổng `5683` trên tường lửa.

| Tài nguyên | Phương thức | Content-Format |
| --- | --- | --- |
| `coap://127.0.0.1:5683/iot/lab/sensor01/data` | GET | `application/json` |
| `coap://127.0.0.1:5683/iot/lab/sensor02/data` | GET | `application/json` |
| `coap://127.0.0.1:5683/iot/lab/sensor03/data` | GET | `application/json` |

> **Lưu ý trên Windows:** `aiocoap` không bind được địa chỉ any-address trên Windows (lỗi `The transport can not be bound to any-address`), nên server bind tường minh vào `127.0.0.1`. Client dùng `127.0.0.1` thay cho `localhost` vì `localhost` có thể phân giải sang IPv6 `::1`, nơi server không lắng nghe.

### Cài đặt và chạy

Thực hiện các lệnh dưới đây từ thư mục gốc `TH_IOT_Buoi3`.

**1. Mở terminal thứ nhất và chạy server:**

```powershell
python Bai2/sensor_server_bai2.py
```

**2. Mở terminal thứ hai và chạy client:**

```powershell
python Bai2/monitor_client_bai2.py
```

Nhập mã thiết bị cần giám sát (`sensor01`, `sensor02` hoặc `sensor03`); bỏ trống sẽ chọn `sensor01`. Client gửi GET mỗi 3 giây cho đến khi nhấn `Ctrl+C`, sau đó in thống kê.

### Hoạt động

**Sensor CoAP Server**

- Mỗi cảm biến là một tài nguyên riêng. Khi khởi động và sau mỗi 3 giây, server sinh giá trị ngẫu nhiên: nhiệt độ `20.0–40.0 °C`, độ ẩm `30.0–90.0 %`.
- GET trả `2.05 Content` với giá trị mới nhất, Content-Format `application/json`:

```json
{"device_id": "sensor01", "temperature": 24.7, "humidity": 66.2, "timestamp": "2026-10-31T16:51:40"}
```

- Truy cập thiết bị không tồn tại (ví dụ `/iot/lab/khong_co/data`) nhận `4.04 Not Found`.

**Monitoring CoAP Client**

- Phân tích JSON và hiển thị mã thiết bị, nhiệt độ, độ ẩm, timestamp của server và thời điểm nhận.
- Nhiệt độ `> 35 °C` → `CANH BAO: Nhiet do cao`; độ ẩm `< 40 %` → `CANH BAO: Do am thap`; không có cảnh báo → `Trang thai: Binh thuong`.
- Server không phản hồi: chờ tối đa 5 giây rồi báo timeout, hoặc báo lỗi giao tiếp sớm hơn nếu hệ điều hành nhận được thông báo cổng không mở; client tiếp tục thử ở chu kỳ sau thay vì dừng.
- Payload không đúng JSON hoặc thiếu trường cũng được báo lỗi, không làm dừng chương trình.

### Gợi ý mở rộng đã thực hiện

| Gợi ý | Cách thực hiện |
| --- | --- |
| Trường `timestamp` trong JSON | Server thêm thời điểm sinh dữ liệu theo ISO 8601. |
| Nhiều cảm biến | Server cung cấp `sensor01`, `sensor02`, `sensor03`. |
| Chọn thiết bị giám sát | Client hỏi mã thiết bị khi khởi động và kiểm tra hợp lệ. |
| Đếm GET và thời gian phản hồi | Mỗi lần nhận in thời gian phản hồi, số GET và trung bình; khi dừng in tổng kết. |

### Kết quả

Toàn bộ log dưới đây là đầu ra thật của lần chạy ngày 31/10/2026, từ `16:51` đến `16:54`, trên Windows 11, Python `3.14.7`, `aiocoap 0.4.17`. Server và client chạy trên cùng một máy qua `127.0.0.1`, chưa thử trên hai máy.

Lần chạy được điều khiển tự động: mã thiết bị đưa vào qua stdin nên không hiện sau dòng nhắc nhập trong log, và client/server được dừng bằng tín hiệu `Ctrl+C` thật. Code/phản hồi và Content-Format được đọc bằng một script `aiocoap` riêng, vì client không in các thông tin này.

| Tiêu chí | Kết quả |
| --- | --- |
| Server cung cấp tài nguyên cảm biến qua URI | Đạt: GET `sensor01`, `sensor02`, `sensor03` đều trả `2.05 Content`; URI `/iot/lab/khong_co/data` trả `4.04 Not Found`. |
| Dữ liệu cập nhật định kỳ | Đạt: log server có 40 dòng `Sensor data updated`, các dòng liền nhau cách đúng 3 giây. |
| Payload đúng JSON, Content-Format `application/json` | Đạt: Content-Format đọc được là `JSON`; client phân tích được 38/38 payload. |
| Client GET và phân tích dữ liệu | Đạt: 38/38 GET thành công khi server chạy (xem bảng dưới). |
| Cảnh báo đúng điều kiện | Đạt: đối chiếu cả 38 lần nhận với ngưỡng, không có sai lệch. Riêng trường hợp có cả hai cảnh báo cùng lúc không xuất hiện trong lần chạy này. |
| Xử lý khi server không phản hồi | Đạt: client báo lỗi giao tiếp và timeout, vẫn chạy tiếp cho đến khi nhấn `Ctrl+C`. |

**Thống kê theo từng cảm biến:**

| Thiết bị | GET thành công | Phản hồi TB (ms) | Nhỏ nhất (ms) | Lớn nhất (ms) | Nhiệt độ cao | Độ ẩm thấp |
| --- | --- | --- | --- | --- | --- | --- |
| `sensor01` | 30/30 | 2.38 | 1.11 | 10.78 | 7 | 3 |
| `sensor02` | 4/4 | 3.17 | 1.23 | 7.56 | 0 | 0 |
| `sensor03` | 4/4 | 3.05 | 1.20 | 7.48 | 1 | 0 |

Trường hợp sát ngưỡng: GET thứ 16 của `sensor01` có nhiệt độ đúng `35.0 °C` và client báo `Trang thai: Binh thuong`, đúng với điều kiện `> 35 °C`.

**Log terminal server (trích 3 GET đầu):**

```text
CoAP Sensor Server started on 127.0.0.1:5683
Resource: coap://127.0.0.1:5683/iot/lab/sensor01/data
Resource: coap://127.0.0.1:5683/iot/lab/sensor02/data
Resource: coap://127.0.0.1:5683/iot/lab/sensor03/data
Du lieu cam bien cap nhat sau moi 3 giay.
Nhan Ctrl+C de dung Server.

GET request received: /iot/lab/sensor01/data
Payload: {"device_id": "sensor01", "temperature": 24.7, "humidity": 66.2, "timestamp": "2026-10-31T16:51:40"}

[16:51:44] Sensor data updated

GET request received: /iot/lab/sensor01/data
Payload: {"device_id": "sensor01", "temperature": 26.8, "humidity": 76.7, "timestamp": "2026-10-31T16:51:44"}

[16:51:47] Sensor data updated

GET request received: /iot/lab/sensor01/data
Payload: {"device_id": "sensor01", "temperature": 24.3, "humidity": 37.5, "timestamp": "2026-10-31T16:51:47"}
```

**Log terminal client giám sát `sensor01` (trích GET 1, 3, 6 và thống kê cuối):**

```text
CoAP Monitoring Client
Cac thiet bi: sensor01, sensor02, sensor03
Nhap ma thiet bi can giam sat (mac dinh sensor01): 
Giam sat: coap://127.0.0.1:5683/iot/lab/sensor01/data
Nhan Ctrl+C de dung.

[16:51:43] Received sensor data

Device: sensor01
Temperature: 24.7 C
Humidity: 66.2 %
Timestamp: 2026-10-31T16:51:40

Trang thai: Binh thuong
Response time: 3.86 ms | GET: 1 | Avg: 3.86 ms

------------------------------

...

[16:51:49] Received sensor data

Device: sensor01
Temperature: 24.3 C
Humidity: 37.5 %
Timestamp: 2026-10-31T16:51:47

CANH BAO: Do am thap
Response time: 4.40 ms | GET: 3 | Avg: 3.64 ms

------------------------------

...

[16:51:58] Received sensor data

Device: sensor01
Temperature: 39.6 C
Humidity: 80.4 %
Timestamp: 2026-10-31T16:51:56

CANH BAO: Nhiet do cao
Response time: 10.78 ms | GET: 6 | Avg: 4.68 ms

------------------------------

...

===== THONG KE =====
Tong so GET: 30
So phan hoi thanh cong: 30
Thoi gian phan hoi trung binh: 2.38 ms

Client da dung.
```

**Phản hồi của từng tài nguyên, gồm cả URI không tồn tại:**

```text
GET coap://127.0.0.1:5683/iot/lab/sensor01/data
Code: 2.05 Content
Content-Format: JSON
Payload: {"device_id": "sensor01", "temperature": 20.9, "humidity": 38.2, "timestamp": "2026-10-31T16:53:41"}

GET coap://127.0.0.1:5683/iot/lab/sensor02/data
Code: 2.05 Content
Content-Format: JSON
Payload: {"device_id": "sensor02", "temperature": 33.1, "humidity": 55.1, "timestamp": "2026-10-31T16:53:41"}

GET coap://127.0.0.1:5683/iot/lab/sensor03/data
Code: 2.05 Content
Content-Format: JSON
Payload: {"device_id": "sensor03", "temperature": 20.6, "humidity": 81.9, "timestamp": "2026-10-31T16:53:41"}

GET coap://127.0.0.1:5683/iot/lab/khong_co/data
Code: 4.04 Not Found
Content-Format: None
Payload: 
```

**Log khi server không hoạt động:**

Thống kê đếm 4 GET nhưng chỉ có 3 dòng lỗi vì `Ctrl+C` đến khi GET thứ 4 còn đang chờ phản hồi.

```text
Giam sat: coap://127.0.0.1:5683/iot/lab/sensor02/data
Nhan Ctrl+C de dung.

[16:53:46] Loi giao tiep voi Server: Network error: NetworkError

------------------------------

[16:53:54] Loi timeout: Server khong phan hoi trong 5 giay.

------------------------------

[16:54:02] Loi timeout: Server khong phan hoi trong 5 giay.

------------------------------


===== THONG KE =====
Tong so GET: 4
So phan hoi thanh cong: 0
Thoi gian phan hoi trung binh: 0.00 ms

Client da dung.
```

**Dữ liệu nhận được (trích, tổng cộng 38 lần nhận):**

Cột `received_at` được lấy sau khi client in kết quả nên có thể lệch 1 giây so với log terminal, như ở GET thứ 6 (`16:51:58` và `16:51:59`).

```text
received_at,device_id,temperature,humidity,timestamp,response_ms
2026-10-31T16:51:43,sensor01,24.7,66.2,2026-10-31T16:51:40,3.86
2026-10-31T16:51:46,sensor01,26.8,76.7,2026-10-31T16:51:44,2.68
2026-10-31T16:51:49,sensor01,24.3,37.5,2026-10-31T16:51:47,4.4
2026-10-31T16:51:52,sensor01,29.6,45.4,2026-10-31T16:51:50,4.26
2026-10-31T16:51:55,sensor01,33.4,34.2,2026-10-31T16:51:53,2.08
2026-10-31T16:51:59,sensor01,39.6,80.4,2026-10-31T16:51:56,10.78
2026-10-31T16:53:16,sensor02,28.6,67.8,2026-10-31T16:53:14,2.05
2026-10-31T16:53:39,sensor03,37.5,46.9,2026-10-31T16:53:38,7.48
```
