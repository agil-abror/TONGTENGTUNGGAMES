"""TongTengTungGames - website game sederhana dengan Python (Flask).

Cara menjalankan:
    pip install -r requirements.txt
    python app.py
Lalu buka http://127.0.0.1:5000 di browser.
"""
import json
import os
from threading import Lock

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

FILE_SKOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skor.json")
kunci = Lock()
DEFAULT = {"memory": None, "mole": 0}


def baca_skor():
    try:
        with open(FILE_SKOR, encoding="utf-8") as f:
            return {**DEFAULT, **json.load(f)}
    except (FileNotFoundError, json.JSONDecodeError):
        return dict(DEFAULT)


def tulis_skor(data):
    with open(FILE_SKOR, "w", encoding="utf-8") as f:
        json.dump(data, f)


@app.route("/")
def beranda():
    return render_template("index.html")


@app.route("/api/skor", methods=["GET"])
def ambil_skor():
    return jsonify(baca_skor())


@app.route("/api/skor", methods=["POST"])
def simpan_skor():
    isi = request.get_json(silent=True) or {}
    game, nilai = isi.get("game"), isi.get("nilai")
    if game not in DEFAULT or not isinstance(nilai, int) or nilai < 0:
        return jsonify({"error": "data tidak valid"}), 400

    with kunci:
        data = baca_skor()
        # Pasang Kartu: makin sedikit langkah makin baik. Tangkap Tikus: makin besar makin baik.
        if game == "memory":
            lebih_baik = data["memory"] is None or nilai < data["memory"]
        else:
            lebih_baik = nilai > data["mole"]
        if lebih_baik:
            data[game] = nilai
            tulis_skor(data)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
