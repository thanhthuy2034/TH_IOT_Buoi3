
import asyncio

from aiocoap import GET, POST, Context, Message
from aiocoap.error import TimeoutError as CoAPTimeoutError

URI = "coap://localhost:5683/iot/lab/message"
INVALID_URI = "coap://localhost:5683/iot/lab/khong_ton_tai"
TIMEOUT_SECONDS = 5


async def send_request(protocol, method, uri, text=None):
    """Gui mot yeu cau va hien thi phan hoi; tra ve None neu that bai."""
    request = Message(
        code=method,
        uri=uri,
        payload=text.encode("utf-8") if text is not None else b"",
    )

    print(f"\nSending {method.name} request...")
    print(f"URI: {uri}")
    if text is not None:
        print(f"Payload: {text}")

    try:
        response = await asyncio.wait_for(
            protocol.request(request).response,
            timeout=TIMEOUT_SECONDS,
        )
    except (asyncio.TimeoutError, CoAPTimeoutError):
        print("Loi timeout: Server khong phan hoi trong 5 giay.")
        print("Hay kiem tra Server va cong UDP 5683.")
        return None
    except Exception as exc:
        print(f"Loi giao tiep voi Server: {exc}")
        return None

    print("\nResponse:")
    print(f"Code: {response.code}")
    print(f"Payload: {response.payload.decode('utf-8', errors='replace')}")
    return response


async def main():
    print("CoAP Client")
    student_id = input("Nhap ma sinh vien: ").strip() or "B23DCCN001"
    student_name = input("Nhap ho ten: ").strip() or "Nguyen Van A"

    try:
        protocol = await Context.create_client_context()
    except Exception as exc:
        print(f"Khong khoi tao duoc CoAP Client: {exc}")
        return

    try:
        await send_request(protocol, GET, URI)
        greeting = f"Xin chao tu CoAP Client - {student_id} - {student_name}"
        await send_request(protocol, POST, URI, greeting)

        # Menu giup thu nghiem 4 goi y mo rong
        while True:
            print("\n===== MENU BAI 1 =====")
            print("1. GET thong diep (sau POST se la thong diep moi nhat)")
            print("2. Gui them thong diep POST")
            print("3. GET tai nguyen khong ton tai (kiem tra 4.04)")
            print("0. Thoat")
            choice = input("Chon: ").strip()

            if choice == "1":
                await send_request(protocol, GET, URI)
            elif choice == "2":
                welcome = input("Nhap noi dung chao: ").strip()
                if not welcome:
                    welcome = "Xin chao tu CoAP Client"
                new_message = f"{welcome} - {student_id} - {student_name}"
                await send_request(protocol, POST, URI, new_message)
            elif choice == "3":
                await send_request(protocol, GET, INVALID_URI)
            elif choice == "0":
                print("Da thoat CoAP Client.")
                break
            else:
                print("Lua chon khong hop le. Hay nhap 0, 1, 2 hoac 3.")
    finally:
        await protocol.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, EOFError):
        print("\nClient da dung.")
