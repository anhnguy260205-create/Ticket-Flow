from flask import Flask
from flask_cors import CORS

from db import get_connection

app = Flask(__name__)
CORS(app)


@app.route("/")
def health():
    return {"status": "ok"}


@app.route("/tickets")
def list_tickets():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tickets")
            return cursor.fetchall()
    finally:
        conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
