# pool.py
import socket
import threading
import json

POOL_HOST = '0.0.0.0'
POOL_PORT = 8888  # 젯슨이 여기에 연결

latest_data = {
    "image_url": "https://via.placeholder.com/300",
    "coordinates": "(0, 0)",
    "message": "초기 상태"
}

def handle_jetson(conn, addr):
    print(f'[POOL] 젯슨 접속됨: {addr}')
    try:
        buffer = ""
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            buffer += data
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                try:
                    json_data = json.loads(line)
                    latest_data.update(json_data)
                    print(f'[POOL] 수신 데이터: {json_data}')
                except json.JSONDecodeError:
                    print('[POOL] JSON 파싱 실패')
    except ConnectionResetError:
        print(f'[POOL] 연결 종료됨: {addr}')
    finally:
        conn.close()

def start_pool_listener():
    def server_thread():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((POOL_HOST, POOL_PORT))
            s.listen()
            print(f'[POOL] 젯슨 수신 서버 시작됨 (port {POOL_PORT})')
            while True:
                conn, addr = s.accept()
                threading.Thread(target=handle_jetson, args=(conn, addr), daemon=True).start()

    threading.Thread(target=server_thread, daemon=True).start()
