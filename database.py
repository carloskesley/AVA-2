import sqlite3
import hashlib

def init_db():
    conn = sqlite3.connect("tarefas.db")
    cursor = conn.cursor()

    # Criação das tabelas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL,
        senha TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        titulo TEXT NOT NULL,
        descricao TEXT,
        status TEXT DEFAULT 'pendente',
        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
    )
    """)

    # Inserção do usuário de teste (se não existir)
    cursor.execute("SELECT * FROM usuarios WHERE usuario = 'admin'")
    if not cursor.fetchone():
        senha_md5 = hashlib.md5(b"123456").hexdigest()
        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", ('admin', senha_md5))

    conn.commit()
    conn.close()
    print("Banco de dados SQLite 'tarefas.db' inicializado com sucesso!")

if __name__ == "__main__":
    init_db()