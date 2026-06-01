from flask import Flask, request, session, redirect
import unicodedata
import os

app = Flask(__name__)
app.secret_key = "8Y#qP4!nLm2@xZ7"

STATUS_FILE = "status.txt"

# ===================================
# FUNÇÃO PARA IGNORAR ACENTOS
# ===================================

def normalizar(texto):
    texto = texto.strip().lower()

    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

# ===================================
# PERGUNTAS
# ===================================

perguntas = [
    ("nome completo do anime que estavamos assistindo no último dia com 32 letras e 7 espaços", "That Time I Got Reincarnated as a Slime"),
    ("Última bebida diferente que tomamos pela primeira vez juntos", "Ballena"),
    ("Nome da garota que eu e você pegamos na mesma noite responda com apenas três letras", "Isa"),
    ("Garota que eu mais gostei desde que nos conhecemos com apenas três letras", "Mel"),
    ("Apenas as letras da senha do seu PC", "lcs"),
    ("Minha bebida favorita com 4 letras", "Coca"),
    ("O que comemos na última janta que estivemos juntos", "Miojo"),
    ("Nome do seu cachorro se não tem apenas digite ( Não )", "Não"),
    ("Qual o apelido que demos para o MKS com 8 letras", "Quagmire"),
    ("Onde comemos no meu aniversário apenas três números", "922")
]

# ===================================
# MENSAGEM FINAL
# ===================================

MENSAGEM_FINAL = """
<h1>Obrigado LK 😎</h1>

<p>
Mande uma mensagem no telegram para o Philps Five
respondendo como se eu te falasse que ainda amo a Melany T. kkkkkkk
</p>

<p>
Parabéns por acertar todas as perguntas.
</p>
"""

# ===================================
# ROTA PRINCIPAL
# ===================================

@app.route("/", methods=["GET", "POST"])
def desafio():

    # Verifica se já houve derrota anteriormente
    if os.path.exists(STATUS_FILE):

        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            status = f.read().strip()

        if status == "PERDEU":
            return """
            <h1>❌ Desafio encerrado</h1>

            <p>
            Uma tentativa já foi utilizada.
            </p>
            """

        elif status == "VENCEU":
            return MENSAGEM_FINAL

    if "indice" not in session:
        session["indice"] = 0

    indice = session["indice"]

    if indice >= len(perguntas):
        return MENSAGEM_FINAL

    pergunta, resposta_correta = perguntas[indice]

    if request.method == "POST":

        resposta_usuario = request.form.get("resposta", "")

        if normalizar(resposta_usuario) == normalizar(resposta_correta):

            session["indice"] += 1

            if session["indice"] >= len(perguntas):

                with open(STATUS_FILE, "w", encoding="utf-8") as f:
                    f.write("VENCEU")

                return MENSAGEM_FINAL

            return redirect("/")

        else:

            with open(STATUS_FILE, "w", encoding="utf-8") as f:
                f.write("PERDEU")

            session.clear()

            return """
            <h1>❌ Você errou.</h1>

            <p>
            O desafio foi encerrado permanentemente.
            </p>
            """

    return f"""
    <h1>Teste, me confirme que é o LK</h1>

    <p>
    Sem chances para erros. Tentativa única.
    </p>

    <h2>Pergunta {indice + 1} de {len(perguntas)}</h2>

    <p>{pergunta}</p>

    <form method="POST">
        <input name="resposta" autocomplete="off" autofocus>
        <button type="submit">Responder</button>
    </form>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)