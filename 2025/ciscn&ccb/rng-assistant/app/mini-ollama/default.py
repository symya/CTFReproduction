from mini_ollama import *

HOST = '127.0.0.1'
PORT = 50051

WORD_LIST = [
    "Python", "Socket", "Ollama", "is", "are", 
    "MINI", "Smart", "socket", "Happy", "Nice", 
    "Welcome", "Awesome", "Great", "LLM", "R1", 
]


if __name__ == "__main__":
    start_server(HOST, PORT, WORD_LIST)
