from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='.')

usuarios = [
    {"id": 1, "nome": "Ana", "idade": 25},
    {"id": 2, "nome": "Carlos", "idade": 30},
    {"id": 3, "nome": "Maria", "idade": 22},
    {"id": 4, "nome": "João", "idade": 28}
]

@app.route('/')
def index():
    usuario_editando = None
    id_editar = request.args.get('editar_id', type=int)
    
    if id_editar:
        usuario_editando = next((u for u in usuarios if u["id"] == id_editar), None)

    return render_template('crud_usuarios.html', usuarios=usuarios, usuario_editando=usuario_editando)

@app.route('/cadastrar')
def cadastrar_usuario():
    nome = request.args.get("nome", "").strip()
    idade = request.args.get("idade", "").strip()
    
    if not nome:
        return redirect(url_for("index", erro="Nome do usuário não pode ser vazio."))
    if not idade or not idade.isdigit():
        return redirect(url_for("index", erro="Informe uma idade válida."))
    
    proximo_id = max([u["id"] for u in usuarios], default=0) + 1
    usuarios.append({"id": proximo_id, "nome": nome, "idade": int(idade)})
    
    return redirect(url_for("index", sucesso="Usuário cadastrado com sucesso!"))

@app.route('/excluir/<int:id>')
def excluir_usuario(id):
    global usuarios
    usuarios = [u for u in usuarios if u["id"] != id]
    return redirect(url_for("index", sucesso="Usuário excluído com sucesso!"))

@app.route('/salvar_edicao')
def salvar_edicao():
    id_usuario = request.args.get("id", type=int)
    novo_nome = request.args.get("nome", "").strip()
    nova_idade = request.args.get("idade", "").strip()

    if not novo_nome:
        return redirect(url_for("index", erro="O nome não pode ficar vazio."))
    if not nova_idade or not nova_idade.isdigit():
        return redirect(url_for("index", erro="Informe uma idade válida."))

    for usuario in usuarios:
        if usuario["id"] == id_usuario:
            usuario["nome"] = novo_nome
            usuario["idade"] = int(nova_idade)
            break

    return redirect(url_for("index", sucesso="Usuário atualizado com sucesso!"))

if __name__ == '__main__':
    app.run(debug=True)