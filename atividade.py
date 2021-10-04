from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

#Configuração do Banco de Dados
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "root"
app.config['MYSQL_DB'] = "atividade"
app.config['MYSQL_PORT'] = 3306

db = MySQL(app)

# Definição dos Comandos SQL para o Banco de Dados        
SQL_LISTA_DADOS = 'SELECT id, nome, sobrenome, senha, confirmasenha, telefone from dados'
SQL_CREATE_DADO = 'INSERT into dados (nome, sobrenome, senha, confirmasenha, telefone) values (%s, %s, %s, %s, %s)'

#Definicição das Classes que vai trabalhar
class Dado:
    def __init__(self, nome, sobrenome, senha, confirmasenha, telefone, id=None):
        self.id = id
        self.nome = nome
        self.sobrenome = sobrenome
        self.senha = senha
        self.confirmasenha = confirmasenha
        self.telefone = telefone

#Organiza os dados que recebe do Banco de Dados em lista de Tuplas
def traduz_dados(dados):
    def cria_dado_com_tupla(tupla):
        return Dado(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], id=tupla[0])
    return list(map(cria_dado_com_tupla, dados))

# Rotas que identificam as diferentes requisiçoes para o FLASK
@app.route('/')
def index():
    cursor = db.connection.cursor()
    cursor.execute(SQL_LISTA_DADOS)
    listaDados = traduz_dados(cursor.fetchall())
    tituloTabela =  "Lista de Dados"
    return render_template('lista.html', titulo = tituloTabela, dados=listaDados)

@app.route('/new')
def new():
    titulo = "Inserir Novo Dado"
    return render_template('create.html', titulo=titulo)

@app.route('/create', methods=['POST'])  
def create():
    nome = request. form['nome']
    sobrenome = request. form['sobrenome']
    senha = request. form['senha']
    confirmasenha = request. form['confirmasenha']
    telefone = request. form['telefone']
    dado = Dado(nome, sobrenome,senha,confirmasenha, telefone)
    cursor = db.connection.cursor()
    cursor.execute(SQL_CREATE_DADO, (dado.nome, dado.sobrenome, dado.senha, dado.confirmasenha, dado.telefone))
    db.connection.commit()
    return redirect(url_for('index'))

@app.route('/update')  
def update():
    return render_template('update.html')

@app.route('/delete')  
def delete():
    return render_template('delete.html')

app.run(debug=True)
