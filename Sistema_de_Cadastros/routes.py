# criação das rotas da aplicação
from flask import Flask, render_template, request, jsonify
from Sistema_de_Cadastros import app


@app.route('/', methods=['GET'])
def home():
    return '<h1>Bem-vindo ao Sistema de Cadastros</h1><p>Use as rotas /perfil/&lt;usuario&gt; e /sobre para acessar as páginas correspondentes.</p>'


@app.route('/perfil/<usuario>', methods=['GET'])
def perfil(usuario):
    return '<h1>Perfil do Usuário</h1><p>Nome: {usuario}</p>'.format(usuario=usuario)


@app.route('/sobre', methods=['GET'])
def sobre():
    return '<h1>Sobre o Sistema</h1><p>Esta é a página sobre o sistema de cadastros.</p>'
