import sqlite3

NOME_BANCO = "monitor_precos.db"


def conectar():
    return sqlite3.connect(NOME_BANCO)


def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # Tabela de produtos monitorados
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        url TEXT NOT NULL,
        preco_alvo REAL NOT NULL
    )
    """)

    # Histórico de preços
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historico_precos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER,
        preco REAL,
        data_consulta DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(produto_id) REFERENCES produtos(id)
    )
    """)

    conn.commit()
    conn.close()
    
def adicionar_produto(nome, url, preco_alvo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO produtos (nome, url, preco_alvo)
    VALUES (?, ?, ?)
    """, (nome, url, preco_alvo))

    conn.commit()
    conn.close()
    
def listar_produtos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()

    conn.close()
    return produtos

def salvar_preco(produto_id, preco):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO historico_precos (produto_id, preco)
    VALUES (?, ?)
    """, (produto_id, preco))

    conn.commit()
    conn.close()

from datetime import date

MAX_ENVIO_DIA = 10


def pode_enviar(db):
    hoje = str(date.today())

    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS controle_envio (
            data TEXT,
            total INTEGER
        )
    """)

    cursor.execute("SELECT total FROM controle_envio WHERE data = ?", (hoje,))
    resultado = cursor.fetchone()

    if not resultado:
        cursor.execute("INSERT INTO controle_envio VALUES (?, ?)", (hoje, 0))
        db.commit()
        return True

    return resultado[0] < MAX_ENVIO_DIA


def registrar_envio(db):
    hoje = str(date.today())

    cursor = db.cursor()

    cursor.execute("SELECT total FROM controle_envio WHERE data = ?", (hoje,))
    total = cursor.fetchone()[0]

    cursor.execute("UPDATE controle_envio SET total = ? WHERE data = ?", (total + 1, hoje))

    db.commit()