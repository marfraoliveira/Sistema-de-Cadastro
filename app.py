from flask import Flask, render_template, request, jsonify
import sqlite3


app = Flask(__name__,static_folder='static', template_folder='Template')

def mensagem():
    return "Bem-vindo ao meu site em flask!"    


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
    app.run(debug=True, port=5001, host='127.0.0.1')
    
    