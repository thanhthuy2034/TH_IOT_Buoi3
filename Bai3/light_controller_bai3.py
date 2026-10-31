"""Bai 3 - Nguyen Doan Hop - B23DCCN350: dieu khien den bang GET/PUT."""

import asyncio
import json

from aiocoap import GET, PUT, Context, Message
from aiocoap.numbers.contentformat import ContentFormat

SERVER_HOST = "127.0.0.1"
URI = f"coap://{SERVER_HOST}:5683/iot/lab/light01/status"
TIMEOUT_SECONDS = 5


async def send_command(protocol, command):
    method = GET if command == "STATUS" else PUT
    request = Message(code=method, uri=URI)
    if method == PUT:
        request.payload = json.dumps({"device_id": "light01", "command": command}).encode("utf-8")
        request.opt.content_format = ContentFormat.JSON
    print(f"\nSending {method.name} request...")
    try:
        response = await asyncio.wait_for(protocol.request(request).response, TIMEOUT_SECONDS)
    except asyncio.TimeoutError:
        print(f"Loi timeout: Server khong phan hoi trong {TIMEOUT_SECONDS} giay.")
        return
    except Exception as exc:
        print(f"Loi giao tiep voi Server: {exc}")
        return
    print(f"Response Code: {response.code}")
    if not response.code.is_successful():
        print(f"Server tra ve loi: {response.payload.decode('utf-8', errors='replace')}")
        return
    try:
        data = json.loads(response.payload.decode("utf-8"))
        if not isinstance(data, dict) or data.get("device_id") != "light01" or data.get("status") not in ("ON", "OFF"):
            raise ValueError("Thieu hoac sai device_id/status")
    except (UnicodeDecodeError, ValueError) as exc:
        print(f"Payload trang thai khong hop le: {exc}")
        return
    print(json.dumps(data, ensure_ascii=False))
    if method == PUT:
        print(f"Da {'bat' if data['status'] == 'ON' else 'tat'} den light01")
    return response


async def main():
    print(f"Light Controller Client\nURI: {URI}")
    protocol = await Context.create_client_context()
    try:
        while True:
            command = input("\nNhap lenh (ON/OFF/STATUS/EXIT): ").strip().upper()
            if command == "EXIT":
                break
            if command not in ("ON", "OFF", "STATUS"):
                print("Lenh khong hop le. Hay nhap ON, OFF, STATUS hoac EXIT.")
                continue
            await send_command(protocol, command)
    finally:
        await protocol.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, EOFError):
        print("\nController da dung.")
    except Exception as exc:
        print(f"Khong chay duoc Controller: {exc}")
        raise SystemExit(1)
