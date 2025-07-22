import socket
from globals import gb
import time

def running_TCP_server():
    """開啟TCPServer"""
    bind_ip = "127.0.0.1"
    bind_port = gb.save_data["TCP_port"]
    OCR_id = gb.save_data["OCR_ID"]
    
    try:
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((bind_ip, bind_port))
        server.listen(1024)
    except OSError as e:
        print(f"無法綁定 TCP 端口 {bind_port}: {e}")
        return

    print ("[*] Listening on %s:%d " % (bind_ip,bind_port))

    while not gb.stop_event.is_set():
        client,addr = server.accept()
        print ('Connected by ', addr)
        while not gb.stop_event.is_set():
            try:
                if gb.send_message_to_kvm:
                    message = f"auto{OCR_id}"
                    client.send((message).encode('utf-8'))
                    time.sleep(30)
            except Exception as e:
                print(f"發送訊息至客戶端失敗:{e}")
            time.sleep(0.1)
        time.sleep(0.1)