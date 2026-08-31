from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='.')

usuarios = [
    {"id": 1, "nome": "Ana"},
    {"id": 2, "nome": "Carlos"},
    {"id": 3, "nome": "Maria"},
    {"id": 4, "nome": "João"}
]

@app.route('/')
def index():
    # Verifica se há um usuário sendo editado no momento
    usuario_editando = None
    id_editar = request.args.get('editar_id', type=int)
    
    if id_editar:
        usuario_editando = next((u for u in usuarios if u["id"] == id_editar), None)

    return render_template('crud_usuarios.html', usuarios=usuarios, usuario_editando=usuario_editando)

@app.route('/cadastrar')
def cadastrar_usuario():
    nome = request.args.get("nome", "").strip()
    
    if not nome:
        return redirect(url_for("index", erro="Nome do usuário não pode ser vazio."))
    
    proximo_id = max([u["id"] for u in usuarios], default=0) + 1
    usuarios.append({"id": proximo_id, "nome": nome})
    
    return redirect(url_for("index", sucesso="Usuário cadastrado com sucesso!"))

# --- ROTA DE EXCLUIR ---
@app.route('/excluir/<int:id>')
def excluir_usuario(id):
    global usuarios
    # Mantém apenas os usuários que NÃO possuem o ID informado
    usuarios = [u for u in usuarios if u["id"] != id]
    return redirect(url_for("index", sucesso="Usuário excluído com sucesso!"))

# --- ROTA PARA SALVAR A EDIÇÃO ---
@app.route('/salvar_edicao')
def salvar_edicao():
    id_usuario = request.args.get("id", type=int)
    novo_nome = request.args.get("nome", "").strip()

    if not novo_nome:
        return redirect(url_for("index", erro="O nome não pode ficar vazio."))

    # Procura o usuário e atualiza o nome
    for usuario in usuarios:
        if usuario["id"] == id_usuario:
            usuario["nome"] = novo_nome
            break

    return redirect(url_for("index", sucesso="Usuário atualizado com sucesso!"))

if __name__ == '__main__':
    app.run(debug=True)