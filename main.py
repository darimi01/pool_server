from pool import start_pool_listener
from user import start_user_server

if __name__ == '__main__':
    # 젯슨 쪽 수신 서버 (Pool → 중앙서버)
    start_pool_listener()

    # 사용자 쪽 전송 서버 (중앙서버 → 사용자 UI)
    start_user_server()
