from flask import Flask, request, jsonify, send_from_directory
import sqlite3

app = Flask(__name__, static_folder='.', static_url_path='')

# Função para conectar ao banco
def get_db():
    conn = sqlite3.connect("estacionamento.db")
    conn.row_factory = sqlite3.Row
    return conn

# Inicializa o banco de dados
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        telefone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS veiculos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT UNIQUE,
        cor TEXT,
        modelo TEXT,
        marca TEXT,
        tamanho TEXT,
        tipo TEXT, -- aqui guardamos hora/diária/mensal
        ano INTEGER,
        cliente_id INTEGER,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vagas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT, -- preferencial, normal
        ocupada INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

# Rota principal
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

# Rota para arquivos estáticos
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)

# Cadastro de clientes
@app.route("/clientes", methods=["POST"])
def add_cliente():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (nome, telefone) VALUES (?, ?)",
                   (data["nome"], data["telefone"]))
    conn.commit()
    conn.close()
    return jsonify({"status": "Cliente cadastrado!"})

# Cadastro de veículos
@app.route("/veiculos", methods=["POST"])
def add_veiculo():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO veiculos 
        (placa, cor, modelo, marca, tamanho, tipo, ano, cliente_id) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            data.get("placa"),
            data.get("cor"),
            data.get("modelo"),
            data.get("marca"),
            data.get("tamanho"),
            data.get("tipoPagamento"),  # salva hora/diária/mensal
            data.get("ano"),
            data.get("cliente_id")
        )
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "Veículo cadastrado!"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
