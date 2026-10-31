"""Bai 3 - Nguyen Doan Hop - B23DCCN350: Smart Light CoAP Server."""

import asyncio
import json

from aiocoap import BAD_REQUEST, CHANGED, CONTENT, UNSUPPORTED_CONTENT_FORMAT
from aiocoap import Context, Message, resource
from aiocoap.numbers.contentformat import ContentFormat

HOST = "127.0.0.1"  # Doi thanh IP may chu khi chay tren hai may.
PORT = 5683
DEVICE_ID = "light01"
RESOURCE_PATH = ["iot", "lab", DEVICE_ID, "status"]


class LightResource(resource.ObservableResource):
    def __init__(self):
        super().__init__()
        self.status = "OFF"
        self.observer_count = 0

    def status_response(self, code):
        return Message(
            code=code,
            payload=json.dumps({"device_id": DEVICE_ID, "status": self.status}).encode("utf-8"),
            content_format=ContentFormat.JSON,
        )

    def update_observation_count(self, newcount):
        if newcount > self.observer_count:
            print("New Observe registration received")
        self.observer_count = newcount
        print(f"Active observers: {newcount}")

    async def render_get(self, request):
        print(f"GET request received: /{'/'.join(RESOURCE_PATH)}")
        return self.status_response(CONTENT)

    async def render_put(self, request):
        # Chap nhan JSON khi khong khai bao Content-Format; tu choi dinh dang khac.
        if request.opt.content_format not in (None, ContentFormat.JSON):
            return Message(code=UNSUPPORTED_CONTENT_FORMAT,
                           payload=b"Payload phai la application/json")
        try:
            data = json.loads(request.payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return Message(code=BAD_REQUEST, payload=b"Payload phai la JSON UTF-8 hop le")
        if not isinstance(data, dict) or data.get("device_id") != DEVICE_ID:
            return Message(code=BAD_REQUEST, payload=b"device_id phai la light01")
        command = data.get("command")
        if command not in ("ON", "OFF"):
            return Message(code=BAD_REQUEST, payload=b"command phai la ON hoac OFF")

        print(f"\nPUT request received:\nDevice: {DEVICE_ID}\nCommand: {command}")
        previous = self.status
        self.status = command
        if previous != self.status:
            print(f"Light state changed: {previous} -> {self.status}")
            print(f"Notify observers: {self.status}")
            self.updated_state()
        else:
            print(f"Light state unchanged: {self.status}; khong gui thong bao Observe")
        return self.status_response(CHANGED)


async def main():
    site = resource.Site()
    site.add_resource(RESOURCE_PATH, LightResource())
    server = await Context.create_server_context(site, bind=(HOST, PORT))
    print(f"CoAP Smart Light Server started on {HOST}:{PORT}")
    print(f"Resource: coap://{HOST}:{PORT}/{'/'.join(RESOURCE_PATH)}")
    print("Initial state: OFF\nNhan Ctrl+C de dung Server.")
    try:
        await asyncio.Event().wait()
    finally:
        await server.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer da dung.")
    except Exception as exc:
        print(f"Khong chay duoc Server: {exc}")
        raise SystemExit(1)
