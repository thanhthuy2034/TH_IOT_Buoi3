
import asyncio
from datetime import datetime

from aiocoap import CHANGED, CONTENT, BAD_REQUEST, Context, Message
from aiocoap.numbers.contentformat import ContentFormat
from aiocoap import resource


class MessageResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.last_message = None

    async def render_get(self, request):
        print("\nGET request received: /iot/lab/message")

        # Lan dau: chao tu Server. Sau POST: tra ve thong diep moi nhat
        text = self.last_message or "Xin chao tu CoAP Server"
        return Message(
            code=CONTENT,
            payload=text.encode("utf-8"),
            content_format=ContentFormat.TEXT,
        )

    async def render_post(self, request):
        try:
            text = request.payload.decode("utf-8").strip()
        except UnicodeDecodeError:
            return Message(
                code=BAD_REQUEST,
                payload=b"Payload phai duoc ma hoa UTF-8",
                content_format=ContentFormat.TEXT,
            )

        if not text:
            return Message(
                code=BAD_REQUEST,
                payload=b"Thong diep khong duoc de trong",
                content_format=ContentFormat.TEXT,
            )

        self.last_message = text
        print("\nPOST request received:")
        print(f"Payload: {text}")
        print(f"Time: {datetime.now().strftime('%H:%M:%S')}")

        return Message(
            code=CHANGED,
            payload="Server da nhan thong diep".encode("utf-8"),
            content_format=ContentFormat.TEXT,
        )


async def main():
    site = resource.Site()
    site.add_resource(["iot", "lab", "message"], MessageResource())

    # Aiocoap mac dinh lang nghe UDP cong 5683
    server = await Context.create_server_context(site)
    print("CoAP Server started on port 5683")
    print("Resource: coap://localhost:5683/iot/lab/message")
    print("Nhan Ctrl+C de dung Server.")

    try:
        await asyncio.Event().wait() 
    finally:
        await server.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer da dung.")

