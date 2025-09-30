from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'troque_esta_chave_para_producao')
DB_PATH = 'gastos.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with sqlite3.connect('gastos.db') as conn:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
              )
            ''')
        c.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            data TEXT NOT NULL,
            valor REAL NOT NULL,
            automatico INTEGER DEFAULT 0,
            irrelevante INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()


@app.before_request
def startup():
    init_db()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        if not username or not password:
            flash('Preencha usuário e senha', 'error')
            return redirect(url_for('register'))

        hashed = generate_password_hash(password)
        try:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed))
            conn.commit()
            conn.close()
            flash('Cadastro realizado. Faça login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Usuário já existe', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Bem-vindo, ' + user['username'], 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciais inválidas', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Desconectado', 'info')
    return redirect(url_for('home'))


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    c = conn.cursor()
    gastos = [dict(row) for row in c.execute('SELECT * FROM gastos WHERE user_id = ? ORDER BY data DESC, created_at DESC', (session['user_id'],)).fetchall()]
    automaticos = [dict(row) for row in c.execute('SELECT * FROM gastos WHERE user_id = ? AND automatico = 1 ORDER BY data DESC', (session['user_id'],)).fetchall()]
    irrelevantes = [dict(row) for row in c.execute('SELECT * FROM gastos WHERE user_id = ? AND irrelevante = 1 ORDER BY data DESC', (session['user_id'],)).fetchall()]

    conn.close()
    return render_template('dashboard.html', gastos=gastos, automaticos=automaticos, irrelevantes=irrelevantes)


@app.route('/adicionar-gasto', methods=['POST'])
def adicionar_gasto():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    titulo = request.form.get('titulo', '').strip()
    data = request.form.get('data')
    valor = request.form.get('valor', '0').replace(',', '.')
    automatico = 1 if request.form.get('automatico') == 'on' else 0

    if not titulo or not data or not valor:
        flash('Preencha todos os campos', 'error')
        return redirect(url_for('dashboard'))

    try:
        valor_f = float(valor)
    except ValueError:
        flash('Valor inválido', 'error')
        return redirect(url_for('dashboard'))

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO gastos (user_id, titulo, data, valor, automatico) VALUES (?, ?, ?, ?, ?)',
              (session['user_id'], titulo, data, valor_f, automatico))
    conn.commit()
    conn.close()
    flash('Gasto adicionado', 'success')
    return redirect(url_for('dashboard'))


@app.route('/editar-gasto/<int:id>', methods=['GET', 'POST'])
def editar_gasto(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM gastos WHERE id = ? AND user_id = ?', (id, session['user_id']))
    gasto = c.fetchone()
    if not gasto:
        conn.close()
        flash('Gasto não encontrado', 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        data = request.form.get('data')
        valor = request.form.get('valor', '0').replace(',', '.')
        automatico = 1 if request.form.get('automatico') == 'on' else 0

        try:
            valor_f = float(valor)
        except ValueError:
            flash('Valor inválido', 'error')
            conn.close()
            return redirect(url_for('editar_gasto', id=id))

        c.execute('UPDATE gastos SET titulo = ?, data = ?, valor = ?, automatico = ? WHERE id = ? AND user_id = ?',
                  (titulo, data, valor_f, automatico, id, session['user_id']))
        conn.commit()
        conn.close()
        flash('Gasto atualizado', 'success')
        return redirect(url_for('dashboard'))

    conn.close()
    return render_template('editgasto.html', gasto=gasto)


@app.route('/excluir-gasto/<int:id>', methods=['POST'])
def excluir_gasto(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM gastos WHERE id = ? AND user_id = ?', (id, session['user_id']))
    conn.commit()
    conn.close()
    flash('Gasto excluído', 'info')
    return redirect(url_for('dashboard'))


@app.route('/marcar-irrelevante/<int:id>', methods=['POST'])
def marcar_irrelevante(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    c = conn.cursor()
    # Toggle irrelevante
    c.execute('SELECT irrelevante FROM gastos WHERE id = ? AND user_id = ?', (id, session['user_id']))
    row = c.fetchone()
    if row:
        novo = 0 if row['irrelevante'] == 1 else 1
        c.execute('UPDATE gastos SET irrelevante = ? WHERE id = ? AND user_id = ?', (novo, id, session['user_id']))
        conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))


@app.route('/toggle-automatico/<int:id>', methods=['POST'])
def toggle_automatico(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT automatico FROM gastos WHERE id = ? AND user_id = ?', (id, session['user_id']))
    row = c.fetchone()
    if row:
        novo = 0 if row['automatico'] == 1 else 1
        c.execute('UPDATE gastos SET automatico = ? WHERE id = ? AND user_id = ?', (novo, id, session['user_id']))
        conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)