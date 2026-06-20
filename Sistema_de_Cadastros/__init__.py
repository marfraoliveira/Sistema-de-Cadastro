# inicialização da aplicação Flask
from flask import Flask



app = Flask(__name__, static_folder='static', template_folder='Template')


from Sistema_de_Cadastros import routes
