from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import sqlite3
import hashlib

app = FastAPI()

# Middleware para habilitar o uso de sessões
app.add_middleware(SessionMiddleware, secret_key="chave_super_secreta")

# Configuração do Jinja2 para os templates HTML
templates = Jinja2Templates(directory="templates")

# Função para obter a conexão com o banco (Equivalente ao conexao.php)
def get_db():
    conn = sqlite3.connect("tarefas.db")
    conn.row_factory = sqlite3.Row # Retorna os resultados como dicionários
    return conn

# === ROTA DE LOGIN ===
@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    if "usuario_id" in request.session:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "erro": None})

@app.post("/login")
async def login_post(request: Request, usuario: str = Form(...), senha: str = Form(...)):
    senha_md5 = hashlib.md5(senha.encode('utf-8')).hexdigest()
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, usuario FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha_md5))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        request.session["usuario_id"] = user["id"]
        request.session["usuario"] = user["usuario"]
        return RedirectResponse(url="/", status_code=303)
    
    return templates.TemplateResponse("login.html", {"request": request, "erro": "Usuário ou senha incorretos!"})

# === ROTA DE LOGOUT ===
@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)

# === ROTA INDEX (Listagem) ===
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    if "usuario_id" not in request.session:
        return RedirectResponse(url="/login", status_code=303)
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tarefas WHERE usuario_id = ? ORDER BY data_criacao DESC", (request.session["usuario_id"],))
    tarefas = cursor.fetchall()
    conn.close()
    
    return templates.TemplateResponse("index.html", {"request": request, "tarefas": tarefas})

# === ROTA NOVA TAREFA ===
@app.get("/nova", response_class=HTMLResponse)
async def nova_get(request: Request):
    if "usuario_id" not in request.session:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("nova.html", {"request": request})

@app.post("/nova")
async def nova_post(request: Request, titulo: str = Form(...), descricao: str = Form("")):
    if "usuario_id" not in request.session:
        return RedirectResponse(url="/login", status_code=303)
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tarefas (usuario_id, titulo, descricao) VALUES (?, ?, ?)", 
                   (request.session["usuario_id"], titulo, descricao))
    conn.commit()
    conn.close()
    
    return RedirectResponse(url="/", status_code=303)

# === ROTA EDITAR ===
@app.get("/editar/{tarefa_id}", response_class=HTMLResponse)
async def editar_get(request: Request, tarefa_id: int):
    if "usuario_id" not in request.session:
        return RedirectResponse(url="/login", status_code=303)
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tarefas WHERE id = ? AND usuario_id = ?", (tarefa_id, request.session["usuario_id"]))
    tarefa = cursor.fetchone()
    conn.close()
    
    if not tarefa:
        return RedirectResponse(url="/", status_code=303)
        
    return templates.TemplateResponse("editar.html", {"request": request, "tarefa": tarefa})

@app.post("/editar/{tarefa_id}")
async def editar_post(request: Request, tarefa_id: int, titulo: str = Form(...), descricao: str = Form(""), status: str = Form(...)):
    if "usuario_id" not in request.session:
        return RedirectResponse(url="/login", status_code=303)
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tarefas SET titulo = ?, descricao = ?, status = ? WHERE id = ? AND usuario_id = ?", 
                   (titulo, descricao, status, tarefa_id, request.session["usuario_id"]))
    conn.commit()
    conn.close()
    
    return RedirectResponse(url="/", status_code=303)

# === ROTA CONCLUIR ===
@app.get("/concluir/{tarefa_id}")
async def concluir(request: Request, tarefa_id: int):
    if "usuario_id" not in request.session:
        return RedirectResponse(url="/login", status_code=303)
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tarefas SET status = 'concluida' WHERE id = ? AND usuario_id = ?", 
                   (tarefa_id, request.session["usuario_id"]))
    conn.commit()
    conn.close()
    
    return RedirectResponse(url="/", status_code=303)

# === ROTA EXCLUIR ===
@app.get("/excluir/{tarefa_id}")
async def excluir(request: Request, tarefa_id: int):
    if "usuario_id" not in request.session:
        return RedirectResponse(url="/login", status_code=303)
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tarefas WHERE id = ? AND usuario_id = ?", (tarefa_id, request.session["usuario_id"]))
    conn.commit()
    conn.close()
    
    return RedirectResponse(url="/", status_code=303)