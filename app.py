from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import hmac


app = Flask(__name__,static_folder='static', template_folder='Template')

@app.route('/<usuario>', methods=['GET'])
def listarusuario(usuario):
    return f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    body {{
        font-family: 'Roboto', sans-serif;
        background-color: #f0f0f0;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        margin: 0;
    }}
    </style>
    <p class='message'>Olá, {usuario}! Seja bem-vindo ao meu site em flask!</p>
    '''

    
def mensagem():
    return "Bem-vindo ao meu site em flask!"    


def autenticacao():
    """
    Valida credenciais de forma simples e mais segura.

    Retorna True quando usuário e senha são válidos, caso contrário False.
    """
    usuario = request.form.get('usuario', '').strip()
    senha = request.form.get('senha', '')

    if not usuario or not senha:
        return False

    # Em produção, use variáveis de ambiente e hash de senha persistido em banco.
    usuario_esperado = os.getenv('AUTH_USER', 'admin')
    senha_esperada = os.getenv('AUTH_PASSWORD', 'admin123')

    usuario_valido = hmac.compare_digest(usuario, usuario_esperado)
    senha_valida = hmac.compare_digest(senha, senha_esperada)

    return usuario_valido and senha_valida


@app.route('/autenticacao', methods=['POST'])
def rota_autenticacao():
    usuario = request.form.get('usuario', '').strip()
    senha = request.form.get('senha', '')

    if not usuario or not senha:
        return jsonify({'message': 'Usuário e senha são obrigatórios.'}), 400

    if autenticacao():
        return jsonify({'message': 'Autenticação realizada com sucesso!'}), 200

    return jsonify({'message': 'Usuário ou senha inválidos.'}), 401


def init_tableClientes():
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            logradouro TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso!")   

@app.route('/listarclientes', methods = ['GET'])
def listar_clientes():
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT 
    id,
    nome,
    email,
    logradouro FROM clientes ORDER BY id ASC''')
    clientes = cursor.fetchall()
    conn.close()
    
    resultado = []
    for c in clientes:
        cliente = {
            'id': c[0],
            'nome': c[1],
            'email' : c[2],
            'logradouro' : c[3]
        }
        resultado.append(cliente)    
    return jsonify(resultado)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        logradouro = request.form.get('logradouro')
        conn = sqlite3.connect('clientes.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO clientes (nome, email, logradouro) VALUES (?, ?, ?)', (nome, email, logradouro))
        conn.commit()
        conn.close()
        return  jsonify({'message': f'Cliente {nome} com email {email} e logradouro: {logradouro} cadastrado com sucesso!'})
    return render_template('cadastro.html')


@app.route('/sobre', methods=['GET'])
def sobre():
    return render_template('sobre.html')



if __name__ == '__main__':
    init_tableClientes()
    print(mensagem())
    app.run(debug=True, port=5002, host='127.0.0.1')
    
    