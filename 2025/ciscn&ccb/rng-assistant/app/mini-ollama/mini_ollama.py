import socket
import random
from threading import Thread


def handle_client(conn, addr, word_list):
    word_list_size = len(word_list)
    with conn:
        print(f"Receive connection from {addr}")
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                N_STOP_WORDS = 4
                selected = ["Start", ]
                random.seed(data)
                tmp = random.randint(0, word_list_size + N_STOP_WORDS - 1)
                while tmp < word_list_size:
                    selected.append(word_list[tmp])
                    tmp = random.randint(0, word_list_size + N_STOP_WORDS - 1)
                response = " ".join(selected)
                
                conn.sendall(response.encode('utf-8'))
                print(f"[sent to {addr}] {response}")
        except ConnectionResetError:
            print(f"Connection reset by peer: {addr}")
        except Exception as e:
            print(f"Error handling connection from {addr}: {e}")
        finally:
            print(f"Connection to {addr} closed")

def start_server(host, port, word_list):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(5)
        print(f"Listening on {host}:{port}...")

        while True:
            conn, addr = s.accept()
            client_thread = Thread(target=handle_client, args=(conn, addr, word_list))
            client_thread.start()

