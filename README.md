# 📝 Sistema de Tarefas (To-Do List) - Avaliação Prática

Este repositório contém a entrega da questão prática do Sistema de Tarefas. 
A aplicação foi desenvolvida utilizando **Python com FastAPI** e banco de dados **SQLite**, cumprindo rigorosamente todas as regras de negócio, layouts e funcionalidades exigidas no enunciado da prova.

## 🚀 Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Framework Web:** FastAPI
* **Renderização de HTML:** Jinja2
* **Banco de Dados:** SQLite3
* **Framework de Layout Obrigatório:** Bootstrap 5 (via CDN)
* **Segurança:** Hash MD5 para senhas e controle de Sessões de Usuário

## 📋 Critérios de Avaliação Atendidos

- [x] Conexão correta com o banco de dados (SQLite).
- [x] Login validando usuário e senha (criptografada em MD5) e criação de Sessão.
- [x] Logout com destruição de sessão e redirecionamento.
- [x] Listagem de tarefas protegida por sessão, exibindo título, status (badges coloridos) e data.
- [x] Inserção de nova tarefa vinculada ao usuário logado.
- [x] Edição de tarefa com formulário pré-preenchido e `<select>` de status.
- [x] Conclusão rápida da tarefa atualizando o status para "concluída".
- [x] Exclusão da tarefa com redirecionamento silencioso.
- [x] Layout padronizado utilizando componentes do **Bootstrap 5** (Cards, Tabelas, Navbar, Badges e Botões), implementado de forma dinâmica em todas as telas (via herança de templates no Jinja2).

---

## ⚙️ Como executar o projeto localmente

Siga o passo a passo abaixo para rodar a aplicação em sua máquina:

### 1. Clonar o repositório
Abra o seu terminal e clone o projeto:
```bash
git clone https://github.com/carloskesley/AVA-2
cd AVA-2
```

### 2. Instalar as dependências necessárias
Certifique-se de ter o Python instalado. Instale as bibliotecas do FastAPI e Jinja2 executando:
```bash
pip install fastapi uvicorn jinja2 python-multipart itsdangerous
```

### 3. Inicializar o Banco de Dados
Antes de rodar o servidor, é necessário criar o banco de dados e o usuário padrão exigido na prova. Execute o script abaixo:
```bash
python database.py
```
*Isso criará o arquivo `tarefas.db` na raiz do projeto com as tabelas `usuarios` e `tarefas`.*

### 4. Rodar o Servidor
Inicie a aplicação utilizando o Uvicorn através do módulo do Python:
```bash
python -m uvicorn main:app --reload
```

### 5. Acessar no Navegador
Abra o seu navegador web e acesse:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🔐 Credenciais de Acesso (Teste)

Conforme solicitado no enunciado, utilize as credenciais abaixo para testar o sistema:

* **Usuário:** `admin`
* **Senha:** `123456` *(Armazenada como MD5 no banco de dados)*

---
*Desenvolvido para a avaliação prática de Sistema de Tarefas.*
