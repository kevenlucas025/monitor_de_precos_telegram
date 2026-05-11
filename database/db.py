import sqlite3
from datetime import date,datetime,timedelta

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
    # CONTROLE DE PRODUTOS JÁ ENVIADOS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos_enviados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT UNIQUE
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS configuracoes(
        chave TEXT PRIMARY KEY,
        valor TEXT
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



MAX_ENVIO_DIA = 100


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
    
def produto_ja_enviado(url):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id FROM produtos_enviados
    WHERE url = ?
    """, (url,))

    resultado = cursor.fetchone()

    conn.close()

    return resultado is not None

def registrar_produto_enviado(url):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO produtos_enviados(url)
    VALUES (?)
    """, (url,))

    conn.commit()
    conn.close()
    
def pode_enviar_intervalo(db, minutos=30):

    cursor = db.cursor()

    cursor.execute("""
    SELECT valor FROM configuracoes
    WHERE chave = 'ultimo_envio'
    """)

    resultado = cursor.fetchone()

    # nunca enviou
    if not resultado:
        return True

    ultimo_envio = datetime.fromisoformat(resultado[0])

    agora = datetime.now()

    diferenca = agora - ultimo_envio

    return diferenca >= timedelta(minutes=minutos)


def registrar_horario_envio(db):

    agora = datetime.now().isoformat()

    cursor = db.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO configuracoes(chave, valor)
    VALUES('ultimo_envio', ?)
    """, (agora,))

    db.commit()