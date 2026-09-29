import os
from contextlib import closing

import psycopg2
from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)

# Toda a configuração vem de variável de ambiente (definida no docker-compose.yml)
DATABASE_URL = os.environ["DATABASE_URL"]

PAGE = """
<!doctype html>
<html lang="pt-br">
<head>
  <meta charset="utf-8">
  <title>Mural de Recados</title>
  <style>
    body { font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 0 16px; }
    input, textarea, button { width: 100%; margin-bottom: 8px; padding: 8px; box-sizing: border-box; }
    .recado { border-bottom: 1px solid #ddd; padding: 8px 0; }
    small { color: #777; }
  </style>
</head>
<body>
  <h1>Mural de Recados</h1>
  <form method="post">
    <input name="autor" placeholder="Seu nome" maxlength="50" required>
    <textarea name="mensagem" placeholder="Deixe seu recado" required></textarea>
    <button type="submit">Enviar</button>
  </form>
  {% for r in recados %}
    <div class="recado">
      <strong>{{ r[0] }}</strong> <small>{{ r[2].strftime("%d/%m/%Y %H:%M") }}</small>
      <p>{{ r[1] }}</p>
    </div>
  {% else %}
    <p>Nenhum recado ainda.</p>
  {% endfor %}
</body>
</html>
"""


def get_conn():
    return psycopg2.connect(DATABASE_URL)


def init_db():
    with closing(get_conn()) as conn, conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS recados (
                id SERIAL PRIMARY KEY,
                autor VARCHAR(50) NOT NULL,
                mensagem TEXT NOT NULL,
                criado_em TIMESTAMP DEFAULT NOW()
            )
            """
        )
        conn.commit()


@app.route("/", methods=["GET", "POST"])
def index():
    with closing(get_conn()) as conn, conn.cursor() as cur:
        if request.method == "POST":
            cur.execute(
                "INSERT INTO recados (autor, mensagem) VALUES (%s, %s)",
                (request.form["autor"], request.form["mensagem"]),
            )
            conn.commit()
            return redirect("/")
        cur.execute("SELECT autor, mensagem, criado_em FROM recados ORDER BY id DESC")
        recados = cur.fetchall()
    return render_template_string(PAGE, recados=recados)


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
