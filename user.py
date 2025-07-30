# user.py
import socket
import threading
import json
import time
from pool import latest_data  # 공유 데이터 사용

USER_HOST = '0.0.0.0'
USER_PORT = 9999

clients = []

def handle_user(conn, addr):
    print(f'[USER] 사용자 접속: {addr}')
    clients.append(conn)
    try:
        while True:
            time.sleep(1)
            # 최신 데이터를 주기적으로 클라이언트에 전송
            message = json.dumps(latest_data).encode('utf-8')
            conn.sendall(message + b'\n')
    except (ConnectionResetError, BrokenPipeError):
        print(f'[USER] 사용자 연결 종료: {addr}')
    finally:
        clients.remove(conn)
        conn.close()

def start_user_server():
    def server_thread():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((USER_HOST, USER_PORT))
            s.listen()
            print(f'[USER] 사용자 전송 서버 시작됨 (port {USER_PORT})')
            while True:
                conn, addr = s.accept()
                threading.Thread(target=handle_user, args=(conn, addr), daemon=True).start()

    threading.Thread(target=server_thread, daemon=True).start()
