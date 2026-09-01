from flask import Flask, render_template, request, redirect, url_for

# O parâmetro template_folder='.' faz o Flask buscar o HTML na mesma pasta do main.py
app = Flask(__name__, template_folder='.')

usuarios = []
proximo_id = 1

@app.route('/')
def index():
    return render_template('crud_usuarios.html', usuarios=usuarios)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    global proximo_id
    nome = request.form.get('nome')
    idade = request.form.get('idade')
    email = request.form.get('email')
    
    if nome and idade and email:
        usuarios.append({
            'id': proximo_id,
            'nome': nome,
            'idade': idade,
            'email': email
        })
        proximo_id += 1
        
    return redirect(url_for('index'))

@app.route('/deletar/<int:id_usuario>')
def deletar(id_usuario):
    global usuarios
    usuarios = [u for u in usuarios if u['id'] != id_usuario]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)