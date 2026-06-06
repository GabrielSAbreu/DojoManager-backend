# DojoManager - Back-end

Este repositório contém a API do **DojoManager**, um MVP de sistema web desenvolvido para a disciplina de Desenvolvimento Full Stack Básico da PUC. A aplicação resolve o problema de gestão de matrículas e controle de treinos em academias de artes marciais (Dojos), permitindo o gerenciamento de usuários (alunos/professores), modalidades e o vínculo histórico de práticas.

---

## 🛠️ Tecnologias Utilizadas

* **Python** (Linguagem base)
* **FastAPI** (Framework web de alta performance)
* **SQLAlchemy** (ORM para mapeamento de dados)
* **SQLite** (Banco de dados relacional embarcado)
* **Pydantic** (Validação de schemas de dados)

---

## Como Rodar o Projeto Localmente

Siga os passos abaixo para configurar e executar o servidor de desenvolvimento em sua máquina:

1. Clonar o repositório:
```
$git clone https://github.com/seu-usuario/DojoManager-backend.git$ cd DojoManager-backend

```

2. Criar e ativar o ambiente virtual (venv):
# No Linux/Mac:
```
$python3 -m venv .venv$ source .venv/bin/activate

```

# No Windows (PowerShell):
```
$python -m venv .venv$ .venv\Scripts\Activate.ps1

```
3. Instalar as dependências:
```
(.venv)$ pip install -r requirements.txt
```
4. Executar o servidor de desenvolvimento:
```
(.venv)$ uvicorn app:app --reload
```

O servidor iniciará em http://127.0.0.1:8000. 
Acesse http://127.0.0.1:8000/docs para visualizar a documentação interativa (Swagger).