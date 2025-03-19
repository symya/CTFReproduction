import socket
import redis
import json
import os

from hashlib import md5, sha256
from os.path import join
from flask import Flask, request, jsonify, session # type: ignore
from flag import FLAG

app = Flask(__name__)
app.secret_key = os.urandom(0x10)

redis_conn = redis.Redis(host="localhost", port=6379, db=0)

model_ports = {"math-v1": 54321, "default": 50051}

# Port to Database at v1.0.
users = {"test": {"password": "098f6bcd4621d373cade4e832627b4f6"}}


# ======== Utilities ========
class PromptTemplate:
    PROMPT_DIR = "static/prompts"

    def __init__(self, question, user_level="primary"):
        self.user_level = user_level
        self.question = question

    @staticmethod
    def get_template(template_id):
        prompt_key = f"prompt:{template_id}"
        prompt = redis_conn.get(prompt_key)
        if not prompt:
            template_path = join(PromptTemplate.PROMPT_DIR, f"{template_id}.txt")
            with open(template_path, "rb") as file:
                prompt = file.read()
            redis_conn.set(prompt_key, prompt)
        prompt = prompt.decode(errors="ignore")
        return prompt

    def get_prompt(self, template_id):
        return PromptTemplate.get_template(template_id).format(t=self)


def get_model_port(model_id):
    return model_ports.get(model_id, model_ports["default"])


def generate_prompt(user_question, prompt_id="math-v1"):
    return PromptTemplate(user_question).get_prompt(prompt_id)


def query_model(prompt, model_id="default"):
    cache_key = f"{md5(prompt.encode()).hexdigest()}:{model_id}"
    cached = redis_conn.get(cache_key)
    if cached:
        return cached.decode()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("127.0.0.1", get_model_port(model_id)))
            s.sendall(prompt.encode("utf-8"))
            response = s.recv(4096).decode("utf-8")

            redis_conn.setex(cache_key, 3600, response)  # Cache for 1 hour
            return response
    except Exception as e:
        return f"Model service error: {str(e)}"


def generate_salt():
    return os.urandom(0x10)


def hash_password(password, salt):
    return sha256(salt + password.encode()).hexdigest()


# ================

def whoami(username):
    role = request.headers.get("X-User-Role")
    if username is None:
        r = role
    else:
        r = username + ":" + role
    return r

@app.route("/")
def index():
    return f"Welcome to the RNG Assistant, {whoami(session['user'])}!"


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    if username in users:
        return jsonify({"error": "Username already exists"}), 400

    salt = generate_salt()
    hashed_password = hash_password(password, salt)
    users[username] = {"password": hashed_password, "salt": salt}
    return jsonify({"message": "Registration successful"})


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = users.get(username)
    if not user or user["password"] != hash_password(password, user["salt"]):
        return jsonify({"error": "Invalid credentials"}), 401

    session["user"] = username
    return jsonify({"message": f"Login successful", "user": whoami(session['user'])})


@app.route("/ask", methods=["POST"])
def ask_question():
    if "user" not in session:
        return jsonify({"error": "Login required"}), 401

    data = request.json
    question = data.get("question")
    model_id = data.get("model_id", "default")

    final_prompt = generate_prompt(question)

    response = query_model(final_prompt, model_id)
    res = {"answer": response, "prompt": final_prompt, "model_id": model_id, "user": whoami(session['user'])}
    return jsonify(res)


@app.route("/admin/raw_ask", methods=["POST", "PUT", "DELETE"])
def manage_ask():
    if (
        "user" not in session
        or request.headers.get("X-User-Role") != "admin"
        or request.headers.get("X-Secret") != "210317a2ee916063014c57d879b9d3bc"
    ):
        return jsonify({"error": "Access denied"}), 403

    data = request.json
    model_id = data.get("model_id", "default")
    custom_prompt = data.get("prompt")

    final_prompt = custom_prompt

    response = query_model(final_prompt, model_id)
    return jsonify({"answer": response, "user": whoami(session['user'])})


@app.route("/admin/model_ports", methods=["POST", "PUT", "DELETE"])
def manage_model_ports():
    if (
        "user" not in session
        or request.headers.get("X-User-Role") != "admin"
        or request.headers.get("X-Secret") != "210317a2ee916063014c57d879b9d3bc"
    ):
        return jsonify({"error": "Access denied"}), 403

    data = request.json
    model_id = data.get("model_id")
    port = data.get("port")

    if request.method in ["POST", "PUT"]:
        if not model_id or not port:
            return jsonify({"error": "Missing parameters"}), 400
        model_ports[model_id] = port
        return jsonify({"message": "Update successful", "user": whoami(session['user'])})

    elif request.method == "DELETE":
        if not model_id:
            return jsonify({"error": "Missing model_id"}), 400
        if model_id in model_ports:
            del model_ports[model_id]
        return jsonify({"message": "Delete successful", "user": whoami(session['user'])})


if __name__ == "__main__":
    app.run(port=8000)
