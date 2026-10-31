"""Bai 3 - Nguyen Doan Hop - B23DCCN350: CoAP Observe, khong polling."""

import asyncio
import json
from datetime import datetime

from aiocoap import GET, Context, Message

SERVER_HOST = "127.0.0.1"
URI = f"coap://{SERVER_HOST}:5683/iot/lab/light01/status"
TIMEOUT_SECONDS = 5


def show_state(response, initial=False):
    if not response.code.is_successful():
        print(f"Server tra ve loi: {response.code}")
        return False
    try:
        data = json.loads(response.payload.decode("utf-8"))
        if not isinstance(data, dict) or data.get("device_id") != "light01" or data.get("status") not in ("ON", "OFF"):
            raise ValueError("Thieu hoac sai device_id/status")
    except (UnicodeDecodeError, ValueError) as exc:
        print(f"Payload trang thai khong hop le: {exc}")
        return False
    title = "Initial State" if initial else "State Updated"
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] {title}")
    print(f"Device: {data['device_id']}\nStatus: {data['status']}")
    return True


async def main():
    protocol = await Context.create_client_context()
    observation = None
    try:
        print(f"Registering CoAP Observe...\nURI: {URI}")
        # Chi mot GET dang ky Observe=0; cac cap nhat den tu server.
        request = protocol.request(Message(code=GET, uri=URI, observe=0))
        observation = request.observation
        response = await asyncio.wait_for(request.response, TIMEOUT_SECONDS)
        if not response.code.is_successful():
            print(f"Dang ky Observe that bai: {response.code}")
            return
        if response.opt.observe is None:
            print("Server khong chap nhan CoAP Observe.")
            return
        print("Observe registration successful\nNhan Ctrl+C de dung.")
        if not show_state(response, initial=True):
            return
        async for notification in observation:
            show_state(notification)
        print("Server da ket thuc Observe. Chay lai Monitor de dang ky lai.")
    except asyncio.TimeoutError:
        print(f"Loi timeout: Server khong phan hoi trong {TIMEOUT_SECONDS} giay.")
    except Exception as exc:
        print(f"Loi giao tiep Observe: {exc}")
    finally:
        if observation is not None and not observation.cancelled:
            observation.cancel()
        await protocol.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMonitor da dung.")
    except Exception as exc:
        print(f"Khong chay duoc Monitor: {exc}")
        raise SystemExit(1)
