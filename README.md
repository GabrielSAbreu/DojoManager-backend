# DojoManager-backend

### Explicação do projeto
Em construção

#### Como Rodar o Projeto Localmente

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