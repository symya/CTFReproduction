from mini_ollama import *

HOST = '127.0.0.1'
PORT = 54321

WORD_LIST = [
    "Equation", "Function", "Integral", "Derivative", 
    "Mathematics", "Algebra", "Geometry", "Trigonometry", 
    "Statistics", "Probability", "Calculus", "Number Theory", 
    "Linear Algebra", "Differential Equations", "Set Theory", 
]


if __name__ == "__main__":
    start_server(HOST, PORT, WORD_LIST)
