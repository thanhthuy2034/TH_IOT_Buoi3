
import asyncio
import json
import random
from datetime import datetime

from aiocoap import CONTENT, Context, Message
from aiocoap.numbers.contentformat import ContentFormat
from aiocoap import resource

HOST = "127.0.0.1"  # Doi thanh IP may chu khi chay Server/Client tren hai may
PORT = 5683
DEVICE_IDS = ["sensor01", "sensor02", "sensor03"]
UPDATE_INTERVAL = 3


class SensorResource(resource.Resource):
    def __init__(self, device_id):
        super().__init__()
        self.device_id = device_id
        self.data = None
        self.update()

    def update(self):
        """Sinh gia tri ngau nhien trong khoang hop ly."""
        self.data = {
            "device_id": self.device_id,
            "temperature": round(random.uniform(20.0, 40.0), 1),
            "humidity": round(random.uniform(30.0, 90.0), 1),
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }

    async def render_get(self, request):
        print(f"\nGET request received: /iot/lab/{self.device_id}/data")
        print(f"Payload: {json.dumps(self.data)}")

        # Tra ve gia tri moi nhat voi Content-Format application/json
        return Message(
            code=CONTENT,
            payload=json.dumps(self.data).encode("utf-8"),
            content_format=ContentFormat.JSON,
        )


async def update_sensors(sensors):
    while True:
        await asyncio.sleep(UPDATE_INTERVAL)
        for sensor in sensors:
            sensor.update()
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Sensor data updated")


async def main():
    site = resource.Site()
    sensors = []
    for device_id in DEVICE_IDS:
        sensor = SensorResource(device_id)
        site.add_resource(["iot", "lab", device_id, "data"], sensor)
        sensors.append(sensor)

    # Bind tuong minh: tren Windows aiocoap khong bind duoc dia chi any-address
    server = await Context.create_server_context(site, bind=(HOST, PORT))
    print(f"CoAP Sensor Server started on {HOST}:{PORT}")
    for device_id in DEVICE_IDS:
        print(f"Resource: coap://{HOST}:{PORT}/iot/lab/{device_id}/data")
    print(f"Du lieu cam bien cap nhat sau moi {UPDATE_INTERVAL} giay.")
    print("Nhan Ctrl+C de dung Server.")

    updater = asyncio.create_task(update_sensors(sensors))
    try:
        await asyncio.Event().wait()
    finally:
        updater.cancel()
        await server.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer da dung.")
