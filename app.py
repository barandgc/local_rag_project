import time

from flask import Flask, jsonify, render_template, request

from chat import get_chat_client
from embeddings import get_embedding_client
from qa import answer_query

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = (data.get("question") or "").strip()

    start = time.perf_counter()
    answer = answer_query(question)
    elapsed = time.perf_counter() - start

    return jsonify({"answer": answer, "elapsed": round(elapsed, 2)})


def warm_up() -> None:
    print("Modeller yukleniyor, lutfen bekleyin...")
    get_embedding_client()
    get_chat_client()
    print("Modeller hazir. Sunucu baslatiliyor...")


if __name__ == "__main__":
    warm_up()
    app.run(host="127.0.0.1", port=5000, debug=False)
