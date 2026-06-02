from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # Importado para resolver o CORS
import uuid

app = FastAPI(
    title="API Mobile - Biblioteca de Jogos",
    description="API CRUD para gerenciar uma biblioteca pessoal de jogos e suas respectivas avaliações.",
    version="1.0.0"
)

# ─── Configuração do CORS ───────────────────────────────────────────────────

# Configurado com "*" para que o Expo Snack consiga acessar livremente
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Dados em memória ────────────────────────────────────────────────────────

jogos = [
    {
        "id": 1,
        "nome": "The Legend of Zelda",
        "tipo": "Aventura",
        "nota": 10,
        "review": "Um clássico absoluto."
    },
    {
        "id": 2,
        "nome": "FIFA 23",
        "tipo": "Esporte",
        "nota": 7,
        "review": "Bom para jogar com amigos."
    }
]

# Ajustado para 3 para evitar duplicação com os IDs 1 e 2 já existentes
proximo_id = 3


# ─── POST /login ─────────────────────────────────────────────────────────────

@app.post("/login")
def login(dados: dict = Body(...)):
    """
    Realiza a autenticação básica para uso da API.
    Regra: Se email == "usuario@esoft.com" e password == "Abc123", retorne um UUID.
    """
    email = dados.get("email")
    password = dados.get("password")

    if email == "usuario@esoft.com" and password == "Abc123":
        return {"token": str(uuid.uuid4())}

    raise HTTPException(status_code=401, detail="Credenciais inválidas.")


# ─── GET /jogos ──────────────────────────────────────────────────────────────

@app.get("/jogos")
def listar_jogos():
    """
    Retorna a lista completa de jogos e reviews cadastrados.
    """
    return jogos


# ─── GET /jogos/{id} ─────────────────────────────────────────────────────────

@app.get("/jogos/{id}")
def buscar_jogo(id: int):
    """
    Busca os detalhes de um jogo específico pelo seu identificador único.
    """
    for jogo in jogos:
        if jogo["id"] == id:
            return jogo

    raise HTTPException(status_code=404, detail="Jogo não encontrado.")


# ─── POST /jogos ─────────────────────────────────────────────────────────────

@app.post("/jogos", status_code=201)
def cadastrar_jogo(dados: dict = Body(...)):
    """
    Cadastra uma nova review de jogo.
    """
    global proximo_id

    novo_jogo = {
        "id": proximo_id,
        "nome": dados.get("nome"),
        "tipo": dados.get("tipo"),
        "nota": dados.get("nota"),
        "review": dados.get("review")
    }

    proximo_id += 1
    jogos.append(novo_jogo)

    return novo_jogo


# ─── PUT /jogos/{id} ─────────────────────────────────────────────────────────

@app.put("/jogos/{id}")
def atualizar_jogo(id: int, dados: dict = Body(...)):
    """
    Atualiza todos os dados de um jogo existente.
    Obrigatório preencher todos os campos no request.
    """
    for jogo in jogos:
        if jogo["id"] == id:
            jogo["nome"] = dados.get("nome")
            jogo["tipo"] = dados.get("tipo")
            jogo["nota"] = dados.get("nota")
            jogo["review"] = dados.get("review")
            return jogo

    raise HTTPException(status_code=404, detail="Jogo não encontrado.")


# ─── DELETE /jogos/{id} ──────────────────────────────────────────────────────

@app.delete("/jogos/{id}", status_code=204)
def deletar_jogo(id: int):
    """
    Remove a review do sistema.
    Response: 204 No Content (sem corpo de resposta).
    """
    for i, jogo in enumerate(jogos):
        if jogo["id"] == id:
            jogos.pop(i)
            return

    raise HTTPException(status_code=404, detail="Jogo não encontrado.")


# ─── Inicialização ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
