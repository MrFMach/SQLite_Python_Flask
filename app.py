from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para criar o banco de dados
def criar_banco_de_dados():
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pessoas (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        idade INTEGER
    )
    ''')

    conn.commit()
    conn.close()

# Rota para a página inicial
@app.route('/')
def index():
    criar_banco_de_dados()
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM pessoas')
    pessoas = cursor.fetchall()

    conn.close()

    return render_template('index.html', pessoas=pessoas)

# Rota para criar uma pessoa
@app.route('/criar', methods=['POST'])
def criar_pessoa():
    nome = request.form['nome']
    idade = request.form['idade']

    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO pessoas (nome, idade) VALUES (?, ?)', (nome, idade))

    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Rota para atualizar uma pessoa
@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar_pessoa(id):
    novo_nome = request.form['novo_nome']
    nova_idade = request.form['nova_idade']

    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()

    cursor.execute('UPDATE pessoas SET nome=?, idade=? WHERE id=?', (novo_nome, nova_idade, id))

    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Rota para excluir uma pessoa
@app.route('/excluir/<int:id>')
def excluir_pessoa(id):
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM pessoas WHERE id=?', (id,))

    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
