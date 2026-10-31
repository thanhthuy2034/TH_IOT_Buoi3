
import asyncio
import json
import time
from datetime import datetime

from aiocoap import GET, Context, Message
from aiocoap.error import TimeoutError as CoAPTimeoutError

DEVICE_IDS = ["sensor01", "sensor02", "sensor03"]
# Dung 127.0.0.1 thay cho localhost: tren Windows localhost co the phan giai sang ::1
SERVER_HOST = "127.0.0.1"  # Doi thanh IP may chu khi chay tren hai may
URI_TEMPLATE = "coap://" + SERVER_HOST + ":5683/iot/lab/{}/data"
POLL_INTERVAL = 3
TIMEOUT_SECONDS = 5
TEMP_THRESHOLD = 35
HUMIDITY_THRESHOLD = 40


class Stats:
    def __init__(self):
        self.requests = 0
        self.successes = 0
        self.total_ms = 0.0

    def average_ms(self):
        return self.total_ms / self.successes if self.successes else 0.0


def choose_device():
    print("Cac thiet bi: " + ", ".join(DEVICE_IDS))
    while True:
        device_id = input("Nhap ma thiet bi can giam sat (mac dinh sensor01): ").strip()
        if not device_id:
            return "sensor01"
        if device_id in DEVICE_IDS:
            return device_id
        print("Ma thiet bi khong hop le.")


def show_data(data, received_at):
    print(f"[{received_at}] Received sensor data\n")
    print(f"Device: {data['device_id']}")
    print(f"Temperature: {data['temperature']} C")
    print(f"Humidity: {data['humidity']} %")
    if "timestamp" in data:
        print(f"Timestamp: {data['timestamp']}")
    print()

    warnings = []
    if data["temperature"] > TEMP_THRESHOLD:
        warnings.append("CANH BAO: Nhiet do cao")
    if data["humidity"] < HUMIDITY_THRESHOLD:
        warnings.append("CANH BAO: Do am thap")
    print("\n".join(warnings) if warnings else "Trang thai: Binh thuong")


async def poll_once(protocol, uri, stats):
    stats.requests += 1
    request = Message(code=GET, uri=uri)
    start = time.perf_counter()

    try:
        response = await asyncio.wait_for(
            protocol.request(request).response,
            timeout=TIMEOUT_SECONDS,
        )
    except (asyncio.TimeoutError, CoAPTimeoutError):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Loi timeout: "
              f"Server khong phan hoi trong {TIMEOUT_SECONDS} giay.")
        return
    except Exception as exc:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Loi giao tiep voi Server: {exc}")
        return

    elapsed_ms = (time.perf_counter() - start) * 1000
    received_at = datetime.now().strftime("%H:%M:%S")

    if not response.code.is_successful():
        print(f"[{received_at}] Server tra ve loi: {response.code}")
        return

    try:
        data = json.loads(response.payload.decode("utf-8"))
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])
    except (UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError, ValueError):
        print(f"[{received_at}] Payload khong dung dinh dang JSON cam bien: {response.payload!r}")
        return

    stats.successes += 1
    stats.total_ms += elapsed_ms

    show_data(data, received_at)
    print(f"Response time: {elapsed_ms:.2f} ms | "
          f"GET: {stats.requests} | Avg: {stats.average_ms():.2f} ms")


async def main():
    print("CoAP Monitoring Client")
    device_id = choose_device()
    uri = URI_TEMPLATE.format(device_id)

    try:
        protocol = await Context.create_client_context()
    except Exception as exc:
        print(f"Khong khoi tao duoc CoAP Client: {exc}")
        return

    stats = Stats()
    print(f"\nGiam sat: {uri}")
    print("Nhan Ctrl+C de dung.\n")

    try:
        while True:
            await poll_once(protocol, uri, stats)
            print("\n" + "-" * 30 + "\n")
            await asyncio.sleep(POLL_INTERVAL)
    finally:
        print("\n===== THONG KE =====")
        print(f"Tong so GET: {stats.requests}")
        print(f"So phan hoi thanh cong: {stats.successes}")
        print(f"Thoi gian phan hoi trung binh: {stats.average_ms():.2f} ms")
        await protocol.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, EOFError):
        print("\nClient da dung.")
